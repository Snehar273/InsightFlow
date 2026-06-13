import pandas as pd
import json
import logging
import os
import time
import re

from dotenv import load_dotenv
from config import CATEGORIES, SENTIMENTS

load_dotenv()

logger = logging.getLogger(__name__)


class AIProcessor:

    def __init__(self):
        """Initialize Gemini AI with retry logic"""
        try:
            import google.generativeai as genai
            self.genai = genai
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in .env")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-mini")  # Cheaper model
            logger.info("✅ Gemini API initialized")
            self.use_ai = True
            
        except Exception as e:
            logger.warning(f"⚠️ AI not available, using rule-based analysis: {e}")
            self.use_ai = False

    def rule_based_sentiment(self, text):
        """
        Rule-based sentiment detection (FAST, FREE, RELIABLE)
        This is the PRIMARY method - works even without API
        """
        text = str(text).lower()
        
        # Negative keywords
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst', 'hate', 'useless',
            'broken', 'crash', 'failed', 'error', 'issue', 'problem', 'complaint',
            'late', 'delayed', 'missing', 'wrong', 'refund', 'charged', 'deducted',
            'not working', 'doesn\'t work', 'won\'t work', 'broken', 'stuck',
            'frustrating', 'annoying', 'disappointed', 'angry', 'ridiculous',
            'unacceptable', 'unbelievable', 'disgusting', 'pathetic', 'rubbish'
        }
        
        # Positive keywords
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'awesome', 'fantastic',
            'love', 'liked', 'nice', 'wonderful', 'perfect', 'brilliant',
            'best', 'superb', 'outstanding', 'brilliant', 'impressed',
            'happy', 'satisfied', 'pleased', 'delighted', 'thankful',
            'smooth', 'easy', 'fast', 'quick', 'reliable', 'professional',
            'helpful', 'friendly', 'excellent service', 'thank you'
        }
        
        # Count sentiment markers
        neg_count = sum(1 for word in negative_words if word in text)
        pos_count = sum(1 for word in positive_words if word in text)
        
        # Detect sarcasm (positive words + negative context)
        if any(phrase in text for phrase in ['oh great', 'just love', 'exactly what i wanted', 'brilliant, charged']):
            return "Negative"
        
        # Determine sentiment
        if neg_count > pos_count and neg_count > 0:
            return "Negative"
        elif pos_count > neg_count and pos_count > 0:
            return "Positive"
        else:
            return "Neutral"

    def rule_based_category(self, text):
        """
        Rule-based category detection (FAST, FREE, RELIABLE)
        """
        text = str(text).lower()
        
        billing_keywords = {'refund', 'payment', 'bill', 'charged', 'coupon', 'price', 'fee', 'invoice', 'money', 'cost', 'rate', 'charge'}
        app_bug_keywords = {'crash', 'bug', 'login', 'address', 'checkout', 'app', 'save', 'button', 'load', 'freeze', 'error', 'glitch', 'login fails'}
        delivery_keywords = {'delivery', 'driver', 'late', 'order', 'cancelled', 'arrived', 'package', 'door', 'address', 'location', 'timing'}
        support_keywords = {'support', 'staff', 'agent', 'executive', 'response', 'replied', 'email', 'contact', 'help', 'customer service'}
        
        # Count keyword matches
        billing_score = sum(1 for word in billing_keywords if word in text)
        app_score = sum(1 for word in app_bug_keywords if word in text)
        delivery_score = sum(1 for word in delivery_keywords if word in text)
        support_score = sum(1 for word in support_keywords if word in text)
        
        # Return category with highest score
        scores = {
            'Billing': billing_score,
            'App Bug': app_score,
            'Delivery': delivery_score,
            'Staff/Support': support_score
        }
        
        max_category = max(scores, key=scores.get)
        return max_category if scores[max_category] > 0 else 'Other'

    def extract_summary(self, text):
        """Extract first sentence as summary"""
        text = str(text).strip()
        
        # Get first sentence
        sentences = re.split(r'[.!?]+', text)
        first_sentence = sentences[0].strip() if sentences else text
        
        # Limit to 15 words
        words = first_sentence.split()[:15]
        summary = ' '.join(words)
        
        return summary if summary else "Customer feedback recorded"

    def ai_enrich_feedback(self, feedback_text, retry_count=0):
        """
        Try to use AI for enrichment
        Falls back to rule-based if quota exceeded
        """
        if not self.use_ai or retry_count > 2:
            return None  # Use fallback
        
        try:
            prompt = f"""Analyze this customer feedback. Return ONLY JSON.

Feedback: "{feedback_text}"

Return exactly:
{{"sentiment":"Positive" or "Negative" or "Neutral", "category":"Billing" or "App Bug" or "Delivery" or "Staff/Support" or "Other", "summary":"one line under 15 words"}}"""
            
            response = self.model.generate_content(prompt, safety_settings=[])
            response_text = response.text.strip()
            
            # Extract JSON
            match = re.search(r'\{.*?\}', response_text, re.DOTALL)
            if not match:
                return None
            
            json_text = match.group()
            result = json.loads(json_text)
            
            # Validate
            sentiment = result.get('sentiment', 'Neutral')
            if sentiment not in SENTIMENTS:
                sentiment = 'Neutral'
            
            category = result.get('category', 'Other')
            if category not in CATEGORIES:
                category = 'Other'
            
            summary = str(result.get('summary', '')).strip()[:80]
            if not summary:
                summary = self.extract_summary(feedback_text)
            
            return {
                'sentiment': sentiment,
                'category': category,
                'summary': summary,
                'source': 'AI'
            }
        
        except Exception as e:
            # Check if it's a quota error
            if '429' in str(e) or 'quota' in str(e).lower():
                logger.warning(f"⚠️ API Quota exceeded, switching to rule-based analysis")
                self.use_ai = False
                return None
            
            logger.warning(f"AI error (will retry): {str(e)}")
            
            # Retry with backoff
            if retry_count < 2:
                time.sleep(2 ** retry_count)  # Exponential backoff
                return self.ai_enrich_feedback(feedback_text, retry_count + 1)
            
            return None

    def enrich_feedback(self, feedback_text):
        """
        Main method: Try AI first, fallback to rules
        """
        if pd.isna(feedback_text) or str(feedback_text).strip() == "":
            return {
                'sentiment': 'Neutral',
                'category': 'Other',
                'summary': 'Empty feedback',
                'source': 'Rule-Based'
            }
        
        # Try AI first
        if self.use_ai:
            ai_result = self.ai_enrich_feedback(feedback_text)
            if ai_result:
                return ai_result
        
        # Fallback to rule-based (ALWAYS WORKS)
        sentiment = self.rule_based_sentiment(feedback_text)
        category = self.rule_based_category(feedback_text)
        summary = self.extract_summary(feedback_text)
        
        return {
            'sentiment': sentiment,
            'category': category,
            'summary': summary,
            'source': 'Rule-Based'
        }

    def process_batch(self, df, progress_callback=None):
        """
        Process entire dataframe with smart batching
        """
        results = []
        total = len(df)
        
        logger.info(f"Processing {total} feedback items...")
        
        for index, row in df.iterrows():
            feedback = row['feedback_text']
            
            # Enrich with fallback
            result = self.enrich_feedback(feedback)
            results.append(result)
            
            if progress_callback:
                progress_callback(index + 1, total)
            
            # Smart rate limiting (slower for AI, faster for rules)
            if self.use_ai:
                time.sleep(1)  # Be nice to API
            else:
                time.sleep(0.1)  # Rule-based is fast
        
        # Add to dataframe
        df = df.copy()
        df['sentiment'] = [r['sentiment'] for r in results]
        df['category'] = [r['category'] for r in results]
        df['summary'] = [r['summary'] for r in results]
        
        # Log source info
        ai_count = sum(1 for r in results if r.get('source') == 'AI')
        rule_count = sum(1 for r in results if r.get('source') == 'Rule-Based')
        
        logger.info(f"✅ Processing complete!")
        logger.info(f"   AI-enriched: {ai_count}")
        logger.info(f"   Rule-based: {rule_count}")
        
        return df