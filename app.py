import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from modules.cleaner import DataCleaner
from modules.ai_processor import AIProcessor
from modules.report_generator import ReportGenerator

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="InsightFlow - Customer Feedback Analytics",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PROFESSIONAL CSS THEME ====================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        html, body, [class*="css"] {
            background-color: #F8FAFC;
        }
        
        .stApp {
            background-color: #F8FAFC;
        }
        
        /* Typography */
        h1 {
            color: #0F172A;
            font-weight: 700;
            font-size: 2.5em;
            margin-bottom: 8px;
        }
        
        h2 {
            color: #1E293B;
            font-weight: 600;
            font-size: 1.8em;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        
        h3 {
            color: #1E293B;
            font-weight: 600;
            font-size: 1.2em;
            margin-bottom: 12px;
        }
        
        p {
            color: #475569;
            font-weight: 400;
            font-size: 1em;
            line-height: 1.6;
        }
        
        /* Main container */
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* KPI Cards */
        .kpi-card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid #E2E8F0;
            transition: all 0.3s ease;
        }
        
        .kpi-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .kpi-label {
            color: #64748B;
            font-size: 0.85em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .kpi-value {
            color: #2563EB;
            font-size: 2.2em;
            font-weight: 700;
            margin: 12px 0;
        }
        
        .kpi-value.negative {
            color: #EF4444;
        }
        
        .kpi-value.positive {
            color: #22C55E;
        }
        
        .kpi-value.neutral {
            color: #F59E0B;
        }
        
        /* Sidebar */
        .sidebar-header {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 16px 0;
            border-bottom: 2px solid #E2E8F0;
            margin-bottom: 24px;
        }
        
        .sidebar-header h1 {
            font-size: 1.4em;
            margin: 0;
            color: #2563EB;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 1em;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Success/Warning/Error boxes */
        .success-box {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(74, 222, 128, 0.05) 100%);
            border-left: 4px solid #22C55E;
            padding: 16px;
            border-radius: 8px;
            color: #166534;
            margin: 16px 0;
        }
        
        .warning-box {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(253, 224, 71, 0.05) 100%);
            border-left: 4px solid #F59E0B;
            padding: 16px;
            border-radius: 8px;
            color: #92400E;
            margin: 16px 0;
        }
        
        .error-box {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(248, 113, 113, 0.05) 100%);
            border-left: 4px solid #EF4444;
            padding: 16px;
            border-radius: 8px;
            color: #991B1B;
            margin: 16px 0;
        }
        
        /* Progress indicator */
        .progress-flow {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 32px 0;
            gap: 12px;
        }
        
        .progress-step {
            flex: 1;
            background: white;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            border: 2px solid #E2E8F0;
            transition: all 0.3s ease;
        }
        
        .progress-step.active {
            border-color: #2563EB;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(59, 130, 246, 0.05) 100%);
        }
        
        .progress-step.completed {
            border-color: #22C55E;
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.05) 0%, rgba(74, 222, 128, 0.05) 100%);
        }
        
        .progress-step-label {
            font-weight: 600;
            color: #1E293B;
            font-size: 0.95em;
        }
        
        .progress-step.completed .progress-step-label {
            color: #22C55E;
        }
        
        .progress-step.active .progress-step-label {
            color: #2563EB;
        }
        
        /* Charts */
        .chart-container {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        
        /* Data table */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            background: white;
            border: 1px solid #E2E8F0;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: white;
            border-bottom: 2px solid #E2E8F0;
            border-radius: 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #64748B;
            font-weight: 500;
            border-radius: 0;
            padding: 16px 24px;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: transparent;
            color: #2563EB;
            border-bottom-color: #2563EB;
        }
        
        /* Expander */
        .stExpander {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 10px 12px;
            color: #1E293B;
            font-weight: 400;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #2563EB;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        /* Divider */
        .stDivider {
            margin: 24px 0;
            border-color: #E2E8F0;
        }
        
        /* Info box */
        .stInfo, [data-testid="stInfo"] {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
            border: 1px solid #BFDBFE;
            border-radius: 8px;
            padding: 16px;
            color: #1E40AF;
        }
        
        /* Warning */
        .stWarning, [data-testid="stWarning"] {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(253, 224, 71, 0.05) 100%);
            border: 1px solid #FCD34D;
            border-radius: 8px;
            padding: 16px;
            color: #78350F;
        }
        
        /* Success */
        .stSuccess, [data-testid="stSuccess"] {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(74, 222, 128, 0.05) 100%);
            border: 1px solid #86EFAC;
            border-radius: 8px;
            padding: 16px;
            color: #166534;
        }
        
        /* Error */
        .stError, [data-testid="stError"] {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(248, 113, 113, 0.05) 100%);
            border: 1px solid #FECACA;
            border-radius: 8px;
            padding: 16px;
            color: #991B1B;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #94A3B8;
            font-size: 0.9em;
            padding: 32px 0;
            border-top: 1px solid #E2E8F0;
            margin-top: 48px;
        }
        
        /* Metric cards in row */
        .metric-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 24px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'df_enriched' not in st.session_state:
    st.session_state.df_enriched = None
if 'cleaning_report' not in st.session_state:
    st.session_state.cleaning_report = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 💡 InsightFlow")
    st.caption("Customer Feedback Analytics Platform")
    st.divider()
    
    pages = {
        "Overview": 0,
        "Upload Data": 1,
        "Data Pipeline": 2,
        "AI Analysis": 3,
        "Insights": 4,
        "Exports": 5
    }
    
    selected = st.radio("Navigation", list(pages.keys()), label_visibility="collapsed")
    current_page = pages[selected]
    
    st.divider()
    
    # Progress
    if st.session_state.df_enriched is not None:
        st.markdown("### ✅ Progress")
        st.progress(1.0)
        st.caption("🎉 All steps completed!")
    elif st.session_state.df_cleaned is not None:
        st.markdown("### 📊 Progress")
        st.progress(0.75)
        st.caption("75% — Ready for AI Analysis")
    elif st.session_state.df_raw is not None:
        st.markdown("### 📊 Progress")
        st.progress(0.5)
        st.caption("50% — Ready for cleaning")
    else:
        st.markdown("### 📊 Progress")
        st.progress(0.0)
        st.caption("0% — Upload data to begin")

# ==================== PAGE 0: OVERVIEW ====================
if current_page == 0:
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 40px 0;'>
            <h1 style='margin: 0; color: #0F172A;'>InsightFlow</h1>
            <p style='color: #64748B; font-size: 1.1em; margin: 8px 0;'>Transform customer feedback into actionable business intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Main stats
    if st.session_state.df_enriched is not None:
        df = st.session_state.df_enriched
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class='kpi-card'>
                    <div class='kpi-label'>Total Feedback</div>
                    <div class='kpi-value'>""" + str(len(df)) + """</div>
                    <p style='margin: 0; color: #94A3B8; font-size: 0.85em;'>Analyzed</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            neg_count = (df['sentiment'] == 'Negative').sum()
            neg_pct = round(100 * neg_count / len(df), 1)
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Complaints</div>
                    <div class='kpi-value negative'>{neg_count}</div>
                    <p style='margin: 0; color: #94A3B8; font-size: 0.85em;'>{neg_pct}% negative</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            top_cat = df['category'].value_counts().index[0]
            top_count = df['category'].value_counts().values[0]
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Top Issue</div>
                    <div class='kpi-value' style='color: #2563EB; font-size: 1.8em;'>{top_cat}</div>
                    <p style='margin: 0; color: #94A3B8; font-size: 0.85em;'>{top_count} complaints</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            pos_count = (df['sentiment'] == 'Positive').sum()
            pos_pct = round(100 * pos_count / len(df), 1)
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Positive</div>
                    <div class='kpi-value positive'>{pos_count}</div>
                    <p style='margin: 0; color: #94A3B8; font-size: 0.85em;'>{pos_pct}% satisfied</p>
                </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("👋 Start by uploading your customer feedback CSV to begin analysis")
    
    st.divider()
    
    # Workflow
    st.markdown("### 📋 Workflow")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    steps = [
        ("Upload", "📂", 0),
        ("Clean", "🧹", 1),
        ("Analyze", "🤖", 2),
        ("Visualize", "📊", 3),
        ("Export", "📥", 4),
    ]
    
    with col1:
        status = (
    "✅"
    if (
        "df_raw" in st.session_state
        and st.session_state.df_raw is not None
        and not st.session_state.df_raw.empty
    )
    else "○"
)
        st.markdown(f"<div style='text-align: center; padding: 12px; background: white; border-radius: 8px; border: 1px solid #E2E8F0;'><p style='margin: 0; font-size: 1.5em;'>{steps[0][1]}</p><p style='margin: 4px 0 0 0; font-size: 0.85em; color: #64748B;'>{steps[0][0]}</p><p style='margin: 4px 0 0 0; font-size: 1.2em;'>{status}</p></div>", unsafe_allow_html=True)
    
    with col2:
        status = "✅" if st.session_state.df_cleaned is not None else "○"
        st.markdown(f"<div style='text-align: center; padding: 12px; background: white; border-radius: 8px; border: 1px solid #E2E8F0;'><p style='margin: 0; font-size: 1.5em;'>{steps[1][1]}</p><p style='margin: 4px 0 0 0; font-size: 0.85em; color: #64748B;'>{steps[1][0]}</p><p style='margin: 4px 0 0 0; font-size: 1.2em;'>{status}</p></div>", unsafe_allow_html=True)
    
    with col3:
        status = "✅" if st.session_state.df_enriched is not None else "○"
        st.markdown(f"<div style='text-align: center; padding: 12px; background: white; border-radius: 8px; border: 1px solid #E2E8F0;'><p style='margin: 0; font-size: 1.5em;'>{steps[2][1]}</p><p style='margin: 4px 0 0 0; font-size: 0.85em; color: #64748B;'>{steps[2][0]}</p><p style='margin: 4px 0 0 0; font-size: 1.2em;'>{status}</p></div>", unsafe_allow_html=True)
    
    with col4:
        status = "✅" if st.session_state.df_enriched is not None else "○"
        st.markdown(f"<div style='text-align: center; padding: 12px; background: white; border-radius: 8px; border: 1px solid #E2E8F0;'><p style='margin: 0; font-size: 1.5em;'>{steps[3][1]}</p><p style='margin: 4px 0 0 0; font-size: 0.85em; color: #64748B;'>{steps[3][0]}</p><p style='margin: 4px 0 0 0; font-size: 1.2em;'>{status}</p></div>", unsafe_allow_html=True)
    
    with col5:
        status = "✅" if st.session_state.df_enriched is not None else "○"
        st.markdown(f"<div style='text-align: center; padding: 12px; background: white; border-radius: 8px; border: 1px solid #E2E8F0;'><p style='margin: 0; font-size: 1.5em;'>{steps[4][1]}</p><p style='margin: 4px 0 0 0; font-size: 0.85em; color: #64748B;'>{steps[4][0]}</p><p style='margin: 4px 0 0 0; font-size: 1.2em;'>{status}</p></div>", unsafe_allow_html=True)

# ==================== PAGE 1: UPLOAD ====================
elif current_page == 1:
    st.markdown("## 📂 Upload Dataset")
    st.markdown("Upload your customer feedback CSV file to get started")
    
    uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], label_visibility="collapsed")
    
    if uploaded_file:
        try:
            st.session_state.df_raw = pd.read_csv(uploaded_file)
            
            st.markdown("""
                <div class='success-box'>
                ✅ File uploaded successfully! Ready to clean.
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Total Rows</div>
                        <div class='kpi-value'>{len(st.session_state.df_raw)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Columns</div>
                        <div class='kpi-value'>{len(st.session_state.df_raw.columns)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                missing = st.session_state.df_raw['feedback_text'].isna().sum()
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Missing Feedback</div>
                        <div class='kpi-value' style='color: #F59E0B;'>{missing}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                missing = st.session_state.df_raw['timestamp'].isna().sum()
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Missing Dates</div>
                        <div class='kpi-value' style='color: #F59E0B;'>{missing}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            st.markdown("### 👀 Data Preview")
            st.dataframe(st.session_state.df_raw.head(10), use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

# ==================== PAGE 2: DATA PIPELINE ====================
elif current_page == 2:
    st.markdown("## 🧹 Data Pipeline")
    st.markdown("Clean, standardize, and prepare your data")
    
    if st.session_state.df_raw is None:
        st.warning("⚠️ Upload a file first")
    else:
        if st.button("🔧 Run Cleaning", type="primary", use_container_width=True):
            with st.spinner("🔄 Cleaning data..."):
                try:
                    cleaner = DataCleaner(st.session_state.df_raw)
                    st.session_state.df_cleaned, st.session_state.cleaning_report = cleaner.clean()
                    st.success("✅ Cleaning complete!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        if st.session_state.df_cleaned is not None:
            st.markdown("""
                <div class='success-box'>
                ✅ Data cleaned successfully!
                </div>
            """, unsafe_allow_html=True)
            
            report = st.session_state.cleaning_report
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Before</div>
                        <div class='kpi-value'>{report.get('initial_rows', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>After</div>
                        <div class='kpi-value' style='color: #22C55E;'>{report.get('final_rows', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Removed</div>
                        <div class='kpi-value' style='color: #EF4444;'>{report.get('rows_removed', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                pct = report.get('rows_kept_percentage', 0)
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Quality</div>
                        <div class='kpi-value'>{pct}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            with st.expander("👀 Preview Cleaned Data"):
                st.dataframe(st.session_state.df_cleaned.head(15), use_container_width=True)

# ==================== PAGE 3: AI ANALYSIS ====================
elif current_page == 3:
    st.markdown("## 🤖 AI Analysis")
    st.markdown("Analyze sentiment, categorize issues, generate summaries")
    
    if st.session_state.df_cleaned is None:
        st.warning("⚠️ Clean data first")
    else:
        st.info(f"📊 Will process {len(st.session_state.df_cleaned)} feedback items")
        
        if st.button("🚀 Run AI Analysis", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your feedback..."):
                try:
                    processor = AIProcessor()
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def update_progress(current, total):
                        progress_bar.progress(min(current / total, 0.99))
                        status_text.text(f"Processing: {current}/{total} ({round(100*current/total)}%)")
                    
                    st.session_state.df_enriched = processor.process_batch(
                        st.session_state.df_cleaned.copy(),
                        progress_callback=update_progress
                    )
                    
                    progress_bar.progress(1.0)
                    status_text.text("✅ Complete!")
                    
                    # Save outputs
                    report_gen = ReportGenerator(st.session_state.df_enriched)
                    report_gen.save_outputs(st.session_state.df_enriched)
                    
                    st.success("✅ AI analysis complete!")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("💡 Check: GEMINI_API_KEY in .env file")
        
        if st.session_state.df_enriched is not None:
            st.markdown("""
                <div class='success-box'>
                ✅ All feedback analyzed with AI!
                </div>
            """, unsafe_allow_html=True)
            
            df = st.session_state.df_enriched
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Total</div>
                        <div class='kpi-value'>{len(df)}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                neg = (df['sentiment'] == 'Negative').sum()
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Negative</div>
                        <div class='kpi-value negative'>{neg}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                pos = (df['sentiment'] == 'Positive').sum()
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Positive</div>
                        <div class='kpi-value positive'>{pos}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                neu = (df['sentiment'] == 'Neutral').sum()
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>Neutral</div>
                        <div class='kpi-value' style='color: #F59E0B;'>{neu}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            with st.expander("👀 Preview Enriched Data"):
                st.dataframe(
                    st.session_state.df_enriched[['feedback_text', 'sentiment', 'category', 'summary']].head(15),
                    use_container_width=True
                )

# ==================== PAGE 4: INSIGHTS ====================
elif current_page == 4:
    st.markdown("## 📊 Business Insights")
    
    if st.session_state.df_enriched is None:
        st.warning("⚠️ Run AI Analysis first")
    else:
        df = st.session_state.df_enriched
        report_gen = ReportGenerator(df)
        report = report_gen.generate_report_data()
        summary = report['summary']
        
        # Top KPIs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            neg_pct = summary['sentiment_percentage'].get('Negative', 0)
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Customer Issues</div>
                    <div class='kpi-value negative'>{neg_pct}%</div>
                    <p style='margin: 0; color: #94A3B8; font-size: 0.85em;'>Need attention</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            top_cat = list(summary['top_categories'].keys())[0] if summary['top_categories'] else 'N/A'
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Top Complaint</div>
                    <div class='kpi-value' style='font-size: 1.5em;'>{top_cat}</div>
                    <p style='margin: 0; color: #94A3B8; font-size: 0.85em;'>{summary['top_categories'].get(top_cat, 0)} reports</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            pos_pct = summary['sentiment_percentage'].get('Positive', 0)
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Satisfied</div>
                    <div class='kpi-value positive'>{pos_pct}%</div>
                    <p style='margin: 0; color: #94A3B8; font-size: 0.85em;'>Happy customers</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 😊 Sentiment Distribution")
            sentiment_data = summary['sentiment_breakdown']
            fig = go.Figure(data=[go.Pie(
                labels=list(sentiment_data.keys()),
                values=list(sentiment_data.values()),
                marker=dict(colors=['#EF4444', '#22C55E', '#F59E0B']),
                textposition='inside',
                textinfo='percent+label'
            )])
            fig.update_layout(
                showlegend=True,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1E293B'),
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("### 🎯 Complaint Categories")
            category_data = summary['top_categories']
            fig = go.Figure(data=[go.Bar(
                x=list(category_data.keys()),
                y=list(category_data.values()),
                marker=dict(color=['#2563EB', '#06B6D4', '#A855F7', '#EF4444', '#F59E0B'][:len(category_data)])
            )])
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1E293B'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
                margin=dict(t=0, b=50, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.divider()
        
        # Examples
        st.markdown("### 📋 What Customers Are Saying")
        
        for category, examples in report['top_categories_examples'].items():
            count = summary['top_categories'].get(category, 0)
            with st.expander(f"**{category}** — {count} complaints"):
                for i, ex in enumerate(examples, 1):
                    sentiment_icon = "😞" if ex['sentiment'] == 'Negative' else "😊" if ex['sentiment'] == 'Positive' else "😐"
                    st.markdown(f"""
                        **{i}. "{ex['feedback'][:90]}..."**
                        
                        **📝 Summary:** {ex['summary']}
                        
                        **Sentiment:** {sentiment_icon} {ex['sentiment']}
                    """)
                    st.divider()

# ==================== PAGE 5: EXPORTS ====================
elif current_page == 5:
    st.markdown("## 📥 Export Results")
    
    if st.session_state.df_enriched is None:
        st.warning("⚠️ Run AI Analysis first")
    else:
        st.markdown("Download your cleaned data and analysis results:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = st.session_state.df_enriched.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"insightflow_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                st.session_state.df_enriched.to_excel(writer, index=False, sheet_name='Feedback')
            buffer.seek(0)
            
            st.download_button(
                label="📊 Download Excel",
                data=buffer.getvalue(),
                file_name=f"insightflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        st.divider()
        st.markdown("### 📋 Complete Dataset")
        st.dataframe(st.session_state.df_enriched, use_container_width=True, height=500)
        
        st.divider()
        st.markdown("### ✅ Files Saved")
        st.success("Output folder: `/output`")
        st.code("""
output/
├── cleaned_feedback.csv
└── cleaned_feedback.xlsx
        """)

# ==================== FOOTER ====================
st.divider()
st.markdown("""
    <div class='footer'>
        <p>💡 <strong>InsightFlow AI</strong> — Customer Feedback Intelligence Platform</p>
        <p>Transform messy feedback into actionable business insights in minutes</p>
    </div>
""", unsafe_allow_html=True)