import pandas as pd
import json
import logging
import os
import time
from config import CATEGORIES, SENTIMENTS, AI_PROMPT
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class AIProcessor:
    def __init__(self):
        """Initialize Gemini AI client"""
        try:
            import google.generativeai as genai
            self.genai = genai
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in .env file")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("✅ Gemini API initialized")
        except ImportError:
            logger.error("Google Generative AI not installed. Run: pip install google-generativeai")
            raise
        except Exception as e:
            logger.error(f"Gemini initialization error: {e}")
            raise
    
    def enrich_feedback(self, feedback_text):
        """Call AI to get sentiment, category, and summary"""
        try:
            prompt = f"""Analyze this customer feedback and return ONLY a valid JSON object (no markdown, no explanation):

Feedback: "{feedback_text}"

Return exactly this format:
{{"sentiment": "Positive" or "Negative" or "Neutral", "category": "Billing" or "App Bug" or "Delivery" or "Staff/Support" or "Other", "summary": "one line description (max 12 words)"}}"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.split("```")[0]
            
            response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Validate and fix
            result['sentiment'] = result.get('sentiment', 'Neutral')
            if result['sentiment'] not in SENTIMENTS:
                result['sentiment'] = 'Neutral'
            
            result['category'] = result.get('category', 'Other')
            if result['category'] not in CATEGORIES:
                result['category'] = 'Other'
            
            result['summary'] = str(result.get('summary', 'No summary'))[:80]
            
            return result
        
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing error: {e}")
            return {
                'sentiment': 'Neutral',
                'category': 'Other',
                'summary': 'Unable to parse'
            }
        except Exception as e:
            logger.error(f"AI processing error: {e}")
            return {
                'sentiment': 'Neutral',
                'category': 'Other',
                'summary': 'Error processing'
            }
    
    def process_batch(self, df, progress_callback=None):
        """Process all feedbacks in dataframe with rate limiting"""
        results = []
        
        for idx, row in df.iterrows():
            feedback = row['feedback_text']
            
            enriched = self.enrich_feedback(feedback)
            results.append(enriched)
            
            if progress_callback:
                progress_callback(idx + 1, len(df))
            
            # Rate limiting for Gemini
            time.sleep(0.1)
        
        # Add to dataframe
        df['sentiment'] = [r['sentiment'] for r in results]
        df['category'] = [r['category'] for r in results]
        df['summary'] = [r['summary'] for r in results]
        
        return df