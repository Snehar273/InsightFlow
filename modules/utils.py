import pandas as pd
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text):
    """Remove extra spaces, normalize case"""
    if pd.isna(text):
        return ""
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)
    return text.lower()

def is_meaningless(text, patterns):
    """Check if feedback is meaningless gibberish"""
    if pd.isna(text) or text == "":
        return True
    text = clean_text(text)
    if len(text) < 5:
        return True
    for pattern in patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True
    return False

def standardize_timestamp(timestamp_str, date_formats):
    """Try to parse timestamp in multiple formats - IMPROVED"""
    if pd.isna(timestamp_str) or timestamp_str == "":
        return None
    
    timestamp_str = str(timestamp_str).strip()
    
    # First try: extract just the date part if it has time
    if " " in timestamp_str:
        date_part = timestamp_str.split()[0]
    else:
        date_part = timestamp_str
    
    for fmt in date_formats:
        try:
            dt = datetime.strptime(date_part, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return None

def remove_agent_names(text):
    """Remove agent names like 'Agent Priya', 'Agent Vikram'"""
    if pd.isna(text):
        return text
    text = re.sub(r'\s*[Aa]gent\s+\w+\s*[.,]?', '', str(text))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_sarcasm_mismatch(rating, sentiment):
    """Detect when rating contradicts sentiment"""
    if pd.isna(rating):
        return False
    
    try:
        rating = int(rating)
    except:
        return False
    
    if rating >= 4 and sentiment == "Negative":
        return True
    if rating <= 2 and sentiment == "Positive":
        return True
    
    return False

def fuzzy_duplicate_check(text1, text2, threshold=0.85):
    """Check if two texts are likely duplicates using fuzzy matching"""
    from fuzzywuzzy import fuzz
    
    if pd.isna(text1) or pd.isna(text2):
        return False
    
    similarity = fuzz.token_set_ratio(str(text1).lower(), str(text2).lower()) / 100.0
    return similarity >= threshold