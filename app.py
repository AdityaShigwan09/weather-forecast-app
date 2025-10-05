st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Remove Streamlit default styling */
    .stApp {
        background-color: #f8fafc !important;
    }
    
    /* Override Streamlit theme colors */
    .stApp [data-testid="stAppViewContainer"] {
        background-color: #f8fafc;
    }
    
    .stApp [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    .stApp [data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Reset all default colors */
    .stMarkdown, .stText, p, span, div {
        color: #1e293b !important;
    }
    
    /* Sidebar styling */
    .stApp [data-testid="stSidebar"] .stMarkdown {
        color: #334155 !important;
    }
    
    /* Button styling override */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div,
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox input,
    .stSelectbox [data-baseweb="select"] span {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border-color: #e2e8f0 !important;
    }
    
    /* Dropdown fix */
    [data-baseweb="popover"], [data-baseweb="menu"],
    [data-baseweb="menu"] ul, [data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }

    [data-baseweb="menu"] li:hover,
    li[role="option"]:hover {
        background-color: #f1f5f9 !important;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 500 !important;
    }
    
    [data-testid="metric-container"] {
        background: white !important;
        padding: 1.2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        border: 1px solid #f1f5f9 !important;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white !important;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        color: white !important;
    }

    /* Alert styles */
    .alert-critical {
        background: linear-gradient(135deg, #fee 0%, #fdd 100%);
        border-left: 5px solid #dc2626;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.2);
    }
    .alert-warning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    .alert-good {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }

    /* ✅ FIXED DATAFRAME STYLING */
    [data-testid="stDataFrame"] {
        border: none !important;
        box-shadow: none !important;
        background-color: #ffffff !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    [data-testid="stDataFrame"] table {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }

    [data-testid="stDataFrame"] thead th {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }

    [data-testid="stDataFrame"] td {
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
    }

    [data-testid="stDataFrame"] .row_heading,
    [data-testid="stDataFrame"] [data-testid="stIndexColumn"],
    [data-testid="stDataFrame"] thead th:first-child {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    [data-testid="stDataFrame"] tbody tr:hover {
        background-color: #f1f5f9 !important;
        transition: background-color 0.2s ease;
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }

</style>
""", unsafe_allow_html=True)
