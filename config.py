# Configuration file

CATEGORIES = ["Billing", "App Bug", "Delivery", "Staff/Support", "Other"]
SENTIMENTS = ["Positive", "Negative", "Neutral"]

# Meaningless text patterns
MEANINGLESS_PATTERNS = [
    "^ok$", "^good$", "^nice$", "^fine$", "^yes$", "^no$",
    "^....$", "^\\?+$", "^-+$", "^#+$", "^\\d+$"
]

# Timestamp formats to try
DATE_FORMATS = [
    "%d-%b-%y",
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%B %d, %Y",
    "%b %d %Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
]