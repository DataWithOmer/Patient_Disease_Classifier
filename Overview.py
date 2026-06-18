import streamlit as st
import os

st.set_page_config(
    page_title="MediScan",
    page_icon="assets/Logo.png" if os.path.exists("assets/Logo.png") else "🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1080px !important;
    }

    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }

    /* ───────── SIDEBAR FIXES & NAVIGATION ───────── */

    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    [data-testid="stSidebarHeader"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="collapsedControl"] {
        display: none !important;
    }

    button[kind="header"] {
        display: none !important;
    }

    [data-testid="stSidebarContent"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stSidebarUserContent"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stSidebar"] .element-container:first-child {
        margin-top: -20px !important;
        padding-top: 0 !important;
    }

    [data-testid="stSidebar"] .stImage {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    [data-testid="stSidebar"] img {
        display: block !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Modern Navigation Links */
    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.6rem 1.1rem;
        border-radius: 8px;
        color: #64748B;
        font-size: 1.05rem; 
        font-weight: 500;
        text-decoration: none !important;
        transition: all 0.2s ease;
        margin-bottom: 0.25rem;
        cursor: pointer;
        line-height: 1.4;
    }

    .nav-item:hover {
        background-color: #F0FDF9;
        color: #0D9488;
        text-decoration: none !important;
    }

    .nav-item-active {
        background-color: #CCFBF1 !important;
        color: #0F766E !important;
        font-weight: 600 !important;
        border-left: 3px solid #0D9488 !important;
        text-decoration: none !important;
    }

    /* ───────── APP COMPONENTS ───────── */

    .medi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    .medi-card:hover {
        border-color: #0D9488;
        box-shadow: 0 4px 16px rgba(13,148,136,0.08);
        transform: translateY(-1px);
    }

    /* Enlarged globally by exactly 1 font increment scale */
    .section-label {
        font-size: 1.2rem !important;
        font-weight: 700;
        color: #0D9488;
        text-transform: uppercase;
        letter-spacing: 0.11em;
        margin-top: 0.5rem !important;
        margin-bottom: 1.2rem !important;
    }

    /* High readability description typography */
    .medi-card-desc {
        color: #64748B;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(13,148,136,0.3) !important;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        color: #1E293B !important;
    }

    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #0D9488 !important;
        color: white !important;
        border-radius: 6px !important;
    }

    hr {
        border-color: #E2E8F0 !important;
        margin: 0.8rem 0 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #F8FAFC; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #0D9488; }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown(
        "<div style='height:0px;margin-top:-20px;'></div>",
        unsafe_allow_html=True
    )
    if os.path.exists("assets/Logo.png"):
        st.image("assets/Logo.png", width=180)

    # Sidebar Page Navigation Links Layout (Enlarged "NAVIGATION" tag header)
    st.markdown("""
    <div style='padding: 0 0.3rem;'>
        <div style='color: #94A3B8; font-size: 0.92rem; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 0.12em;
                    padding: 0 0.7rem; margin-top: 1.2rem; margin-bottom: 0.6rem;'>Navigation</div>
        <a href='/' target='_self' class='nav-item nav-item-active'>Overview</a>
        <a href='/Disease_Predictor' target='_self' class='nav-item'>Disease Predictor</a>
        <a href='/Model_Insights' target='_self' class='nav-item'>How It Works</a>
        <a href='/Health_Assistant' target='_self' class='nav-item'>Health Assistant</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0.8rem 0;'>", unsafe_allow_html=True)

    # Dataset info block layout (Enlarged headers and entry labels)
    st.markdown("""
    <div style='padding: 0 0.3rem;'>
        <div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
                    padding: 0.95rem 1.1rem;'>
            <div style='color: #94A3B8; font-size: 0.92rem; font-weight: 700;
                        text-transform: uppercase; letter-spacing: 0.12em;
                        margin-bottom: 0.75rem;'>Dataset</div>
            <div style='display: flex; justify-content: space-between;
                        align-items: center; margin-bottom: 0.45rem;'>
                <span style='color: #64748B; font-size: 0.90rem; font-weight: 500;'>Patient Records</span>
                <span style='color: #0D9488; font-weight: 700; font-size: 0.95rem;'>4,921</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #64748B; font-size: 0.90rem; font-weight: 500;'>Diseases Covered</span>
                <span style='color: #0D9488; font-weight: 700; font-size: 0.95rem;'>42</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Compressed Title Header Layout ─────────────────────────────
st.markdown("""
<div style='padding: 0.2rem 0 0rem 0;'>
    <span style='background: #CCFBF1; color: #0F766E; font-size: 0.90rem; font-weight: 600;
                 text-transform: uppercase; letter-spacing: 0.12em; padding: 0.25rem 0.75rem;
                 border-radius: 999px;'>AI-Powered Health Tool</span>
    <h1 style='font-size: 2.3rem; font-weight: 700; color: #0F172A;
               margin: 0.2rem 0 0.1rem 0; line-height: 1.1;'>
        Medi<span style='color: #0D9488;'>Scan</span>
    </h1>
    <p style='font-size: 1.05rem; color: #64748B; margin: 0; padding-bottom: 0.2rem;
              max-width: 600px; line-height: 1.5;'>
        Enter your symptoms and get an instant ML-powered disease prediction
        with a full health report — no medical knowledge required.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 0.1rem 0 1rem 0;'>", unsafe_allow_html=True)

# ── Features Section (What MediScan Does) ──────────────────────
st.markdown("<div class='section-label'>What MediScan Does</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
features = [
    ('<i class="fa-solid fa-stethoscope"></i>', "Smart Diagnosis",
     "3 ML models analyze your symptoms and return the most likely disease with a confidence score."),
    ('<i class="fa-solid fa-chart-line"></i>', "Visual Health Report",
     "Charts showing disease probabilities and which of your symptoms influenced the result most."),
    ('<i class="fa-solid fa-robot"></i>', "AI Health Assistant",
     "Ask any health question — symptoms, medications, diseases — and get a clear formatted answer."),
]
for col, (icon, title, desc) in zip([col1, col2, col3], features):
    with col:
        st.markdown(f"""
        <div class='medi-card'>
            <div style='font-size: 1.8rem; margin-bottom: 0.6rem; color: #0D9488;'>{icon}</div>
            <div style='font-weight: 600; color: #0F172A; margin-bottom: 0.4rem;
                        font-size: 0.92rem;'>{title}</div>
            <div class='medi-card-desc'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── How to use Section ────────────────────────────────────────
st.markdown("<div class='section-label'>How to Use</div>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
steps = [
    ("1", "Select Symptoms", "Search and pick all symptoms you are currently experiencing"),
    ("2", "Choose Mode", "Pick Quick, Balanced, or Deep Analysis"),
    ("3", "Get Prediction", "See your predicted disease and confidence score instantly"),
    ("4", "Read Report", "Review severity, precautions, and visual health charts"),
]
for col, (num, title, desc) in zip([c1, c2, c3, c4], steps):
    with col:
        st.markdown(f"""
        <div class='medi-card' style='text-align: center; padding: 1.2rem; height: 220px;'>
            <div style='width: 30px; height: 30px; border-radius: 50%;
                        background: #CCFBF1; border: 1.5px solid #0D9488;
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto 0.65rem auto; font-size: 0.8rem;
                        font-weight: 700; color: #0F766E;'>{num}</div>
            <div style='font-weight: 600; color: #0F172A; font-size: 0.84rem;
                        margin-bottom: 0.4rem;'>{title}</div>
            <div class='medi-card-desc'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style='color: #475569; font-size: 0.92rem; text-align: center;
            padding-top: 0.8rem; border-top: 1px solid #E2E8F0;'>
    ⚠️ MediScan is not a substitute for professional medical advice.
    Always consult a qualified doctor for diagnosis and treatment.
</div>
""", unsafe_allow_html=True)