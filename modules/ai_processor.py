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
        """Initialize Gemini AI"""

        try:
            import google.generativeai as genai

            self.genai = genai

            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                raise ValueError("GEMINI_API_KEY not found")

            genai.configure(api_key=api_key)

            # Latest stable model
            self.model = genai.GenerativeModel("gemini-2.0-flash")

            logger.info("Gemini initialized successfully")

        except Exception as e:
            logger.error(f"AI Initialization Error : {e}")
            raise

    def enrich_feedback(self, feedback_text):
        """
        Analyze one feedback message
        """

        if pd.isna(feedback_text) or str(feedback_text).strip() == "":
            return {
                "sentiment": "Neutral",
                "category": "Other",
                "summary": "Empty feedback"
            }

        prompt = f"""
You are an AI Customer Feedback Analyst.

Analyze the customer feedback.

Customer Feedback:

{feedback_text}

Choose ONLY these sentiments:

Positive
Negative
Neutral

Choose ONLY these categories:

Billing
App Bug
Delivery
Staff/Support
Other

Generate a one-line summary under 15 words.

Return ONLY valid JSON.

Example:

{{
    "sentiment":"Negative",
    "category":"Billing",
    "summary":"Customer reports delayed refund."
}}
"""

        try:

            response = self.model.generate_content(prompt)

            response_text = response.text.strip()

            match = re.search(r"\{.*\}", response_text, re.DOTALL)

            if not match:
                raise Exception("No JSON returned")

            json_text = match.group()

            result = json.loads(json_text)

            sentiment = result.get("sentiment", "Neutral")

            if sentiment not in SENTIMENTS:
                sentiment = "Neutral"

            category = result.get("category", "Other")

            if category not in CATEGORIES:
                category = "Other"

            summary = str(result.get("summary", "")).strip()

            if summary == "":
                summary = "No summary generated"

            return {
                "sentiment": sentiment,
                "category": category,
                "summary": summary
            }

        except Exception as e:

            logger.error(f"AI Processing Error : {e}")

            # Rule-based fallback

            text = str(feedback_text).lower()

            category = "Other"
            sentiment = "Neutral"

            if any(word in text for word in [
                "refund",
                "payment",
                "bill",
                "charged",
                "coupon",
                "price",
                "fee"
            ]):
                category = "Billing"

            elif any(word in text for word in [
                "crash",
                "bug",
                "login",
                "address",
                "checkout",
                "app",
                "save"
            ]):
                category = "App Bug"

            elif any(word in text for word in [
                "delivery",
                "driver",
                "late",
                "order",
                "cancelled"
            ]):
                category = "Delivery"

            elif any(word in text for word in [
                "support",
                "staff",
                "agent",
                "executive"
            ]):
                category = "Staff/Support"

            if any(word in text for word in [
                "bad",
                "terrible",
                "late",
                "refund",
                "failed",
                "issue",
                "problem",
                "ridiculous",
                "crash",
                "cancelled"
            ]):
                sentiment = "Negative"

            elif any(word in text for word in [
                "great",
                "good",
                "awesome",
                "excellent",
                "fantastic",
                "love",
                "wonderful",
                "thank"
            ]):
                sentiment = "Positive"

            return {
                "sentiment": sentiment,
                "category": category,
                "summary": "Generated using fallback logic"
            }

    def process_batch(self, df, progress_callback=None):
        """
        Process entire dataframe
        """

        results = []

        total = len(df)

        for index, row in df.iterrows():

            feedback = row["feedback_text"]

            result = self.enrich_feedback(feedback)

            results.append(result)

            if progress_callback:
                progress_callback(index + 1, total)

            # Prevent API rate limit
            time.sleep(1)

        df = df.copy()

        df["sentiment"] = [x["sentiment"] for x in results]
        df["category"] = [x["category"] for x in results]
        df["summary"] = [x["summary"] for x in results]

        logger.info("AI enrichment completed")

        return df