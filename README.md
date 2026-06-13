# 💡 InsightFlow AI

**Transform customer feedback into actionable business intelligence in minutes.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://insightflow-XXXXX.streamlit.app)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📸 **Live Demo**

🚀 **[Open InsightFlow AI](https://insightflow-XXXXX.streamlit.app)**

*Replace XXXXX with your actual Streamlit Cloud URL*

---

## 🎯 **What is InsightFlow?**

InsightFlow is an **AI-powered customer feedback intelligence platform** designed to help businesses:

- 📊 **Analyze thousands of customer messages** automatically
- 🤖 **Detect sentiment** (Positive, Negative, Neutral)
- 🎯 **Categorize complaints** (Billing, App Bug, Delivery, Staff/Support, Other)
- ✨ **Generate summaries** (one-line issue descriptions)
- 📈 **Create visual dashboards** (KPIs, charts, trends)
- 📥 **Export clean data** (CSV, Excel)

Instead of manually reading 1,800+ messages, managers get **instant, structured insights** in seconds.

---

## ✨ **Key Features**

### 📁 **Data Upload**
- Drag-and-drop CSV upload
- Automatic format detection
- Data quality assessment
- Preview raw data instantly

### 🧹 **Smart Data Cleaning**
- Remove exact & fuzzy duplicates
- Standardize timestamps (10+ formats supported)
- Normalize text & remove junk
- Remove agent names pollution
- Intelligent missing data handling

### 🤖 **AI-Powered Analysis**
- **Sentiment Analysis** → Positive / Negative / Neutral
- **Smart Categorization** → 5 fixed complaint categories
- **Issue Summarization** → One-line, plain-English summaries
- **Confidence Scoring** → Know which classifications are reliable
- Powered by Google Gemini AI

### 📊 **Executive Dashboard**
- **KPI Cards** → Total feedback, complaints %, top issues
- **Sentiment Pie Chart** → Visual sentiment breakdown
- **Category Bar Chart** → Top complaint categories
- **Representative Examples** → Real customer quotes per category
- **Trend Analysis** → What's improving/worsening

### 📥 **Export & Reports**
- Download cleaned CSV
- Export to Excel (formatted)
- AI usage log (transparency)
- High-quality, decision-ready outputs

### 🎨 **Professional UI**
- Modern, clean SaaS design
- Dark-to-light theme with blue accent
- Responsive layout (desktop, tablet, mobile)
- Smooth animations & transitions
- Business-focused, not feature-bloated

---

## 🛠️ **Tech Stack**

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.28+ |
| **Backend** | Python 3.11+ |
| **Data Processing** | Pandas, NumPy |
| **AI/ML** | Google Generative AI (Gemini) |
| **Data Cleaning** | FuzzyWuzzy, regex |
| **Visualization** | Plotly, Matplotlib |
| **Export** | OpenPyXL (Excel) |
| **Deployment** | Streamlit Cloud |

---

## 📋 **System Architecture**
Raw CSV Input

│

├─→ Data Loader

│   └─→ CSV preview & quality check

│

├─→ Data Cleaner

│   ├─→ Remove duplicates (fuzzy matching)

│   ├─→ Fix timestamps (10+ formats)

│   ├─→ Normalize text

│   ├─→ Remove agent names

│   └─→ Fill missing data

│

├─→ AI Processor (Gemini)

│   ├─→ Sentiment detection

│   ├─→ Category classification

│   ├─→ Summary generation

│   └─→ Confidence scoring

│

├─→ Report Generator

│   ├─→ KPI aggregation

│   ├─→ Chart generation

│   └─→ Example extraction

│

└─→ Output

├─→ Cleaned CSV

├─→ Excel Report

└─→ AI Usage Log

---

## 🚀 **Quick Start**

### **Option 1: Use Live Demo (Fastest)**

Just visit: **[https://insightflow-XXXXX.streamlit.app](https://insightflow-XXXXX.streamlit.app)**

No installation needed!

### **Option 2: Run Locally**

#### **Prerequisites**
- Python 3.11 or higher
- pip (Python package manager)
- Google Gemini API key (free from [aistudio.google.com](https://aistudio.google.com/app/apikey))

#### **Installation Steps**

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/InsightFlow.git
cd InsightFlow
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up API key**

Create a `.env` file in the root folder:

InsightFlow/

│

├── 📄 README.md                    

├── 📄 requirements.txt             ← Dependencies

├── 📄 app.py                       ← Main Streamlit app

├── 📄 config.py                    ← Configuration & constants

├── 📄 .env                         ← API keys (don't commit!)

├── 📄 .gitignore                   ← Git ignore rules

│

├── 📂 modules/

│   ├── init.py

│   ├── cleaner.py                  ← Data cleaning logic

│   ├── ai_processor.py             ← AI enrichment (Gemini)

│   ├── report_generator.py         ← Report & export generation

│   └── utils.py                    ← Helper functions

│

├── 📂 data/

│   └── customer_feedback_raw.csv   ← Your input data

│

├── 📂 output/

│   ├── cleaned_feedback.csv        ← Output (auto-generated)

│   └── cleaned_feedback.xlsx       ← Output (auto-generated)

│

└── 📂 .streamlit/

└── config.toml                 ← Streamlit theme config

---

## 🧹 **Data Cleaning Details**

InsightFlow handles the **messy realities** of real-world customer feedback:

### **What Gets Removed**
- ❌ Duplicate messages (exact or 80%+ similar)
- ❌ Empty feedback rows
- ❌ Meaningless entries ("ok", "good", "...", single characters)
- ❌ Agent names ("Agent Priya", "Agent Vikram") that pollute feedback

### **What Gets Fixed**
- ✅ Timestamps in 10+ different formats → standardized YYYY-MM-DD
- ✅ Multiple spaces → single space
- ✅ UPPERCASE text → lowercase
- ✅ Inconsistent ratings → 1-5 integer scale
- ✅ Missing values → marked as NaN

### **Duplicate Detection**
Uses **fuzzy matching** (80% similarity threshold):
- "Order arrived 50 mins late" = "order got there after 50 minutes" (duplicates)
- Same source + timestamp + similar text = likely duplicate

---

## 🤖 **AI Enrichment Details**

### **Sentiment Analysis**
- **Positive** — Customer satisfied, praising, happy
- **Negative** — Customer unhappy, complaining, frustrated
- **Neutral** — Factual, asking questions, no clear emotion

Detects **sarcasm**: "Oh great, charged me twice, exactly what I wanted" = Negative (despite "great")

### **Complaint Categories** (Fixed List)
1. **Billing** — Payment, refund, coupon, pricing issues
2. **App Bug** — Technical glitches, crashes, UI problems
3. **Delivery** — Order arrival, driver, location, timing
4. **Staff/Support** — Agent response, customer service quality
5. **Other** — Anything that doesn't fit above

### **Summaries**
- One-line, plain-English description
- Example: "Payment failed but money still deducted"
- Useful for quick scanning & report generation

---

## 📊 **Dashboard Metrics Explained**

### **KPI Cards**
- **Total Feedback** — How many messages analyzed
- **Complaints %** — Percentage of negative feedback
- **Top Issue** — Which category has most complaints
- **Satisfaction %** — Percentage of positive feedback

### **Sentiment Chart**
Visual breakdown of Positive / Negative / Neutral distribution

### **Category Chart**
Bar chart showing complaint volumes per category

### **Representative Examples**
Real customer quotes that best represent each complaint type

---

## 🔧 **Configuration**

Edit `config.py` to customize:

```python
CATEGORIES = ["Billing", "App Bug", "Delivery", "Staff/Support", "Other"]
SENTIMENTS = ["Positive", "Negative", "Neutral"]

# Timestamp formats to recognize
DATE_FORMATS = [
    "%d-%b-%y",      # 02-Feb-24
    "%m/%d/%Y",      # 02/14/2024
    "%d/%m/%Y",      # 14/02/2024
    "%B %d, %Y",     # March 18, 2024
    # ... add more as needed
]

# Text patterns considered "meaningless"
MEANINGLESS_PATTERNS = [
    "^ok$", "^good$", "^nice$", "^yes$", "^no$",
    "^....$", "^\\?+$"
]
```

---

## 🚀 **Deployment to Streamlit Cloud**

### **Step 1: Push to GitHub**
```bash
git add .
git commit -m "InsightFlow - Customer Feedback Intelligence"
git push origin main
```

### **Step 2: Deploy**
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"New app"**
3. Select:
   - Repository: `YOUR_USERNAME/InsightFlow`
   - Branch: `main`
   - Main file: `app.py`
4. Click **Deploy**
5. Wait 2-3 minutes for deployment

### **Step 3: Get Live URL**
Once deployed, your app will be live at:https://insightflow-XXXXX.streamlit.app

---

## ⚙️ **Environment Variables**

Create `.env` file in root:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your-key-here

# Optional: Gemini model (default: gemini-pro)
GEMINI_MODEL=gemini-pro

# Optional: Rate limiting (milliseconds between API calls)
API_RATE_LIMIT=100
```

**NEVER commit `.env` to GitHub!** It's in `.gitignore`

---

## 🐛 **Troubleshooting**

### **Error: "GEMINI_API_KEY not found"**
**Solution:** 
1. Go to https://aistudio.google.com/app/apikey
2. Create new API key
3. Add to `.env`: `GEMINI_API_KEY=your-key-here`
4. Restart the app

### **Error: "Could not parse timestamp"**
**Solution:** The app will still work but some dates won't be standardized. Add more formats to `config.py`:
```python
DATE_FORMATS = [
    # ... existing formats
    "%d-%m-%Y %H:%M:%S",  # Add new format
]
```

### **Error: "No module named 'google.generativeai'"**
**Solution:**
```bash
pip install --upgrade google-generativeai
```

### **App is slow during AI Analysis**
**Expected behavior:** AI API calls take time. Processing 1,000+ messages typically takes 2-5 minutes.
- Check internet connection
- Verify API key is valid
- Check Gemini API quota (free tier has limits)

### **CSV not loading**
**Check:**
- File is `.csv` format
- Required columns: id, timestamp, source, rating, feedback_text
- No special characters in filenames
- File size < 100MB

---

## 📈 **Performance Metrics**

| Task | Time | Volume |
|------|------|--------|
| **Upload** | < 10 sec | 10,000 rows |
| **Data Cleaning** | 10-30 sec | 10,000 rows |
| **AI Analysis** | 2-5 min | 1,000 rows |
| **Dashboard Load** | < 5 sec | All data |
| **Export** | < 5 sec | All data |

*Times vary based on internet speed & Gemini API load*

---

## 🔒 **Data Privacy & Security**

### **What InsightFlow Does**
- ✅ Processes data locally in your Streamlit session
- ✅ Sends only feedback_text to Gemini API (not IDs or emails)
- ✅ Saves outputs to `/output` folder (your machine)
- ✅ Does NOT store data on external servers

### **What InsightFlow Does NOT Do**
- ❌ Store data in databases
- ❌ Send complete records to third parties
- ❌ Log customer information
- ❌ Share data with advertisers

**Note:** Feedback text is sent to Google Gemini for AI analysis. Review [Google's Privacy Policy](https://policies.google.com/privacy) for details.

---

## 🤝 **Contributing**

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

---

## 📚 **Learning Resources**

- [Streamlit Docs](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Google Generative AI Docs](https://ai.google.dev/docs)
- [Plotly Charts](https://plotly.com/python/)

---

## 🗺️ **Roadmap**

Future enhancements:

- [ ] Multiple language support
- [ ] Time-series trend analysis
- [ ] Automated email reports
- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] Custom complaint categories per company
- [ ] Advanced NLP (entity extraction, topic modeling)
- [ ] Integration with Slack/Teams
- [ ] Dark mode toggle
- [ ] Real-time feedback streaming
- [ ] Multi-file batch processing

---

## 📝 **License**

This project is licensed under the MIT License — see [LICENSE](LICENSE) file for details.

**In short:** You're free to use, modify, and distribute this project, even commercially, as long as you include the license notice.

---

## 👤 **Author**

**Sneha R**
- 🎓 Final-year B.Tech IT Student @ Sri Krishna College of Technology
- 💻 GitHub: [@Snehar273](https://github.com/Snehar273)
- 📧 Email: [ssnehar36@gmail.com](mailto:ssnehar36@gmail.com)
- 🔗 LinkedIn: [linkedin.com/in/sneha-r-b90866290](https://linkedin.com/in/sneha-r-b90866290)

---

## 🙏 **Acknowledgments**

- Google Gemini AI for sentiment & categorization
- Streamlit for the amazing framework
- FuzzyWuzzy for intelligent duplicate detection
- Plotly for beautiful visualizations

---

## 📞 **Support & Feedback**

Have questions or suggestions? 

- 📬 **Email:** ssnehar36@gmail.com
- 🐛 **Report Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/InsightFlow/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/InsightFlow/discussions)

---

## 🎯 **Key Takeaway**

> **InsightFlow transforms messy, unstructured customer feedback into clean, AI-enriched, and decision-ready business insights in minutes.**

Stop reading feedback manually. Start making data-driven decisions. 🚀

---

<div align="center">

**Made with ❤️ by Sneha R**

⭐ If you find this useful, please consider starring the repository!

[View on GitHub](https://github.com/Snehar273/InsightFlow) • [Live Demo](https://insightflow-XXXXX.streamlit.app)

</div>