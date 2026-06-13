import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, df):
        self.df = df
    
    def generate_summary(self):
        """Generate summary statistics"""
        summary = {
            'total_feedback': len(self.df),
            'sentiment_breakdown': self.df['sentiment'].value_counts().to_dict(),
            'sentiment_percentage': (self.df['sentiment'].value_counts() / len(self.df) * 100).round(1).to_dict(),
            'top_categories': self.df['category'].value_counts().head(5).to_dict(),
            'category_percentage': (self.df['category'].value_counts() / len(self.df) * 100).round(1).to_dict(),
            'sources': self.df['source'].value_counts().to_dict(),
        }
        return summary
    
    def get_top_category_examples(self, category, n=3):
        """Get representative examples for a category"""
        category_df = self.df[self.df['category'] == category]
        
        # Get most negative first (complaints)
        if category_df.empty:
            return []
        
        negative_first = category_df[category_df['sentiment'] == 'Negative']
        if len(negative_first) > 0:
            examples = negative_first.head(n)
        else:
            examples = category_df.head(n)
        
        result = []
        for _, row in examples.iterrows():
            result.append({
                'feedback': row['feedback_text'][:120],
                'sentiment': row['sentiment'],
                'summary': row['summary']
            })
        
        return result
    
    def generate_report_data(self):
        """Generate all report data"""
        summary = self.generate_summary()
        top_categories = list(summary['top_categories'].keys())
        
        report = {
            'summary': summary,
            'top_categories_examples': {}
        }
        
        for category in top_categories[:5]:
            report['top_categories_examples'][category] = self.get_top_category_examples(category, n=3)
        
        return report
    
    def save_outputs(self, df_enriched, output_dir='output'):
        """Save CSV and summary to output folder"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save cleaned CSV
        csv_path = os.path.join(output_dir, 'cleaned_feedback.csv')
        df_enriched.to_csv(csv_path, index=False)
        logger.info(f"✅ Saved: {csv_path}")
        
        # Save Excel
        excel_path = os.path.join(output_dir, 'cleaned_feedback.xlsx')
        df_enriched.to_excel(excel_path, index=False, sheet_name='Feedback')
        logger.info(f"✅ Saved: {excel_path}")
        
        return csv_path, excel_path