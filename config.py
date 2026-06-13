# Configuration file - all constants here

CATEGORIES = ["Billing", "App Bug", "Delivery", "Staff/Support", "Other"]
SENTIMENTS = ["Positive", "Negative", "Neutral"]

AI_PROMPT = """
You are an AI Customer Feedback Analyst.

Return ONLY JSON.

Sentiment:
Positive, Negative, Neutral

Category:
Billing
App Bug
Delivery
Staff/Support
Other

Summary:
Maximum 15 words.
"""

# Meaningless text patterns
MEANINGLESS_PATTERNS = [
    "^ok$", "^good$", "^nice$", "^fine$", "^yes$", "^no$",
    "^....$", "^\\?+$", "^-+$", "^#+$", "^\\d+$"
]

# Timestamp formats to try
DATE_FORMATS = [
    "%d-%b-%y",          # 02-Feb-24
    "%m/%d/%Y",          # 02/14/2024
    "%d/%m/%Y",          # 14/02/2024
    "%B %d, %Y",         # March 18, 2024
    "%b %d %Y",          # Feb 24 2024
    "%d-%m-%Y",          # 25-03-2024
    "%Y-%m-%d",          # 2024-02-02
]