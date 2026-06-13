import pandas as pd
import logging
from config import MEANINGLESS_PATTERNS, DATE_FORMATS
from modules.utils import (
    clean_text, is_meaningless, standardize_timestamp,
    remove_agent_names, fuzzy_duplicate_check
)

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.cleaning_report = {}
    
    def clean(self):
        """Run full cleaning pipeline"""
        logger.info("🧹 Starting data cleaning...")
        
        initial_rows = len(self.df)
        
        # Step 1: Basic column validation
        self.validate_columns()
        
        # Step 2: Remove completely empty rows
        self.remove_empty_rows()
        
        # Step 3: Clean text fields
        self.clean_text_fields()
        
        # Step 4: Remove meaningless feedback
        self.remove_meaningless_feedback()
        
        # Step 5: Standardize timestamps
        self.standardize_timestamps()
        
        # Step 6: Standardize ratings
        self.standardize_ratings()
        
        # Step 7: Remove agent names from feedback
        self.remove_agent_names_from_text()
        
        # Step 8: Remove/flag duplicates
        self.remove_duplicates()
        
        final_rows = len(self.df)
        self.cleaning_report['initial_rows'] = initial_rows
        self.cleaning_report['final_rows'] = final_rows
        self.cleaning_report['rows_removed'] = initial_rows - final_rows
        self.cleaning_report['rows_kept_percentage'] = round(100 * final_rows / initial_rows, 1)
        
        logger.info(f"✅ Cleaning complete! {initial_rows} → {final_rows} rows")
        
        return self.df, self.cleaning_report
    
    def validate_columns(self):
        """Ensure required columns exist"""
        required = ['id', 'timestamp', 'source', 'rating', 'feedback_text']
        for col in required:
            if col not in self.df.columns:
                raise ValueError(f"Missing required column: {col}")
    
    def remove_empty_rows(self):
        """Remove rows with no feedback text"""
        before = len(self.df)
        self.df = self.df[self.df['feedback_text'].notna() & (self.df['feedback_text'] != '')]
        after = len(self.df)
        if before - after > 0:
            logger.info(f"Removed {before - after} rows with empty feedback")
    
    def clean_text_fields(self):
        """Normalize text: trim spaces, standardize case"""
        self.df['feedback_text'] = self.df['feedback_text'].apply(clean_text)
    
    def remove_meaningless_feedback(self):
        """Remove gibberish, single words, etc."""
        before = len(self.df)
        self.df = self.df[~self.df['feedback_text'].apply(
            lambda x: is_meaningless(x, MEANINGLESS_PATTERNS)
        )]
        after = len(self.df)
        if before - after > 0:
            logger.info(f"Removed {before - after} meaningless entries")
    
    def standardize_timestamps(self):
        """Convert all timestamps to YYYY-MM-DD format"""
        self.df['timestamp'] = self.df['timestamp'].apply(
            lambda x: standardize_timestamp(x, DATE_FORMATS)
        )
        missing = self.df['timestamp'].isna().sum()
        if missing > 0:
            logger.warning(f"⚠️  {missing} timestamps could not be parsed (using as-is)")
    
    def standardize_ratings(self):
        """Convert ratings to 1-5 int, fill NaN with 3 (neutral)"""
        self.df['rating'] = pd.to_numeric(self.df['rating'], errors='coerce')
        self.df['rating'] = self.df['rating'].apply(
            lambda x: int(x) if pd.notna(x) and 1 <= x <= 5 else None
        )
    
    def remove_agent_names_from_text(self):
        """Remove agent names that pollute the feedback"""
        self.df['feedback_text'] = self.df['feedback_text'].apply(remove_agent_names)
    
    def remove_duplicates(self):
        """Remove near-duplicates using fuzzy matching"""
        before = len(self.df)
        
        self.df = self.df.reset_index(drop=True)
        duplicates_to_remove = set()
        
        # Smarter duplicate detection
        for i in range(len(self.df)):
            if i in duplicates_to_remove:
                continue
            for j in range(i + 1, min(i + 50, len(self.df))):  # Only check next 50 rows
                if j in duplicates_to_remove:
                    continue
                
                # Check if same source
                if self.df.iloc[i]['source'] != self.df.iloc[j]['source']:
                    continue
                
                # Check if feedback is similar
                if fuzzy_duplicate_check(
                    self.df.iloc[i]['feedback_text'],
                    self.df.iloc[j]['feedback_text'],
                    threshold=0.8
                ):
                    duplicates_to_remove.add(j)
        
        self.df = self.df.drop(list(duplicates_to_remove)).reset_index(drop=True)
        after = len(self.df)
        if before - after > 0:
            logger.info(f"Removed {before - after} duplicates")