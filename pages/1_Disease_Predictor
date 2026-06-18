import streamlit as st
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import plotly.graph_objects as go
from model import predict_disease, get_symptom_importance
from utils.preprocess import load_and_preprocess, load_precautions

st.set_page_config(
    page_title="MediScan — Disease Predictor",
    page_icon="assets/Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def get_data():
    _, _, all_symptoms = load_and_preprocess()
    precautions = load_precautions()
    return all_symptoms, precautions

all_symptoms, precautions = get_data()

severity_map = {
    "Fungal infection ":  "Low ",  "Allergy ":  "Low ",  "GERD ":  "Low ",
    "Chronic cholestasis ":  "Medium ",  "Drug Reaction ":  "Medium ",
    "Peptic ulcer diseae ":  "Medium ",  "AIDS ":  "High ",
    "Diabetes ":  "Medium ",  "Gastroenteritis ":  "Low ",
    "Bronchial Asthma ":  "Medium ",  "Hypertension ":  "High ",
    "Migraine ":  "Low ",  "Cervical spondylosis ":  "Low ",
    "Paralysis (brain hemorrhage) ":  "High ",  "Jaundice ":  "Medium ",
    "Malaria ":  "High ",  "Chicken pox ":  "Low ",  "Dengue ":  "High ",
    "Typhoid ":  "High ",  "hepatitis A ":  "Medium ",  "Hepatitis B ":  "High ",
    "Hepatitis C ":  "High ",  "Hepatitis D ":  "High ",  "Hepatitis E ":  "Medium ",
    "Alcoholic hepatitis ":  "High ",  "Tuberculosis ":  "High ",
    "Common Cold ":  "Low ",  "Pneumonia ":  "High ",
    "Dimorphic hemmorhoids(piles) ":  "Low ",  "Heart attack ":  "High ",
    "Varicose veins ":  "Low ",  "Hypothyroidism ":  "Medium ",
    "Hyperthyroidism ":  "Medium ",  "Hypoglycemia ":  "High ",
    "Osteoarthristis ":  "Low ",  "Arthritis ":  "Low ",
    "(vertigo) Paroymsal  Positional Vertigo ":  "Low ",
    "Acne ":  "Low ",  "Urinary tract infection ":  "Medium ",
    "Psoriasis ":  "Low ",  "Impetigo ":  "Low "
}
severity_map = {k.strip(): v.strip() for k, v in severity_map.items()}

# ─────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
    max-width: 1080px !important;
}

.stApp { background-color: #F8FAFC; color: #1E293B; }

/* ── Animations ─────────────────────────────────────────── */
@keyframes fadeInUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideInRight { from { opacity: 0; transform: translateX(30px); } to { opacity: 1; transform: translateX(0); } }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.92); } to { opacity: 1; transform: scale(1); } }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
@keyframes pulseGlow { 0%, 100% { box-shadow: 0 8px 24px rgba(13,148,136,0.18); } 50% { box-shadow: 0 12px 36px rgba(13,148,136,0.35); } }
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes chipPop { 0% { opacity: 0; transform: scale(0.6); } 70% { transform: scale(1.08); } 100% { opacity: 1; transform: scale(1); } }
@keyframes progressFill { from { width: 0%; } }

.anim-fade-up { animation: fadeInUp 0.6s ease-out both; }
.anim-fade { animation: fadeIn 0.7s ease-out both; }
.anim-slide-right { animation: slideInRight 0.6s ease-out both; }
.anim-scale { animation: scaleIn 0.5s ease-out both; }
.anim-delay-1 { animation-delay: 0.1s; }
.anim-delay-2 { animation-delay: 0.25s; }
.anim-delay-3 { animation-delay: 0.4s; }
.anim-delay-4 { animation-delay: 0.55s; }

/* ── Sidebar ───────────────────────────────────────────── */
[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
[data-testid="stSidebarHeader"] { display: none !important; height: 0 !important; padding: 0 !important; margin: 0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarUserContent"] { padding-top: 0 !important; margin-top: 0 !important; padding-left: 1rem !important; padding-right: 1rem !important; }

.nav-item { display: block; padding: 0.48rem 1rem; border-radius: 8px; color: #64748B; font-size: 1.05rem; font-weight: 500; text-decoration: none !important; transition: all 0.2s ease; margin-bottom: 0.15rem; }
.nav-item:hover { background-color: #F0FDF9; color: #0D9488; text-decoration: none !important; }
.nav-item-active { background-color: #CCFBF1 !important; color: #0F766E !important; font-weight: 600 !important; border-left: 3px solid #0D9488 !important; text-decoration: none !important; }

/* ── Cards ──────────────────────────────────────────────── */
.medi-card { background: linear-gradient(145deg, #FFFFFF 0%, #FAFFFE 100%); border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(15,23,42,0.04), 0 1px 2px rgba(15,23,42,0.03); transition: all 0.3s ease; position: relative; overflow: hidden; }
.medi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #0D9488, #5EEAD4, #0D9488); background-size: 200% 100%; animation: shimmer 3s linear infinite; opacity: 0.6; }
.medi-card:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(13,148,136,0.12), 0 4px 12px rgba(15,23,42,0.06); }

/* ── Section label ──────────────────────────────────────── */
.section-label { font-size: 1.25rem; font-weight: 800; color: #0F766E; text-transform: uppercase; letter-spacing: 0.13em; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.5rem; }
.section-label::before { content: ''; width: 4px; height: 18px; border-radius: 2px; background: linear-gradient(180deg, #0D9488, #5EEAD4); }

/* ── Chart section heading ─────────────────────────────── */
.chart-section-heading { font-size: 1.1rem; font-weight: 700; color: #0F766E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem; padding-bottom: 0.4rem; border-bottom: 2px solid #E2E8F0; }
.chart-section-heading::before { content: ''; width: 4px; height: 16px; border-radius: 2px; background: linear-gradient(180deg, #0D9488, #5EEAD4); }

/* ── Number input ───────────────────────────────────────── */
[data-testid="stNumberInput"] input { background-color: #FFFFFF !important; color: #0D9488 !important; font-weight: 600 !important; font-size: 1.05rem !important; border: 1.5px solid #E2E8F0 !important; border-radius: 10px !important; padding: 0.6rem !important; }
[data-testid="stNumberInput"] button { background-color: #F0FDF9 !important; color: #0D9488 !important; border: 1px solid #E2E8F0 !important; border-radius: 6px !important; font-weight: 700 !important; }
[data-testid="stNumberInput"] button:hover { background-color: #0D9488 !important; color: white !important; }

/* ─ Selectbox ──────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div { background-color: #FFFFFF !important; border: 1.5px solid #E2E8F0 !important; border-radius: 10px !important; color: #1E293B !important; }
[data-testid="stSelectbox"] span { color: #0D9488 !important; font-weight: 600 !important; font-size: 1rem !important; }

/* ── Multiselect ────────────────────────────────────────── */
[data-testid="stMultiSelect"] > div > div { background-color: #FFFFFF !important; border: 1.5px solid #E2E8F0 !important; border-radius: 10px !important; color: #1E293B !important; min-height: 52px !important; }
div[data-testid="stMultiSelect"] > label, div[data-testid="stMultiSelect"] label[data-testid="stWidgetLabel"] p, div[data-testid="stNumberInput"] > label, div[data-testid="stSelectbox"] > label { font-size: 1.55rem !important; font-weight: 800 !important; color: #0F172A !important; margin-bottom: 0.6rem !important; letter-spacing: -0.01em !important; }
[data-testid="stMultiSelect"] input { color: #1E293B !important; font-size: 0.95rem !important; }
[data-testid="stMultiSelect"] input::placeholder { color: #94A3B8 !important; }
.stMultiSelect span[data-baseweb="tag"] { background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%) !important; color: white !important; font-size: 1rem !important; font-weight: 600 !important; border-radius: 8px !important; padding: 0.25rem 0.7rem !important; border: none !important; box-shadow: 0 2px 6px rgba(13,148,136,0.25); animation: chipPop 0.35s ease-out both; }
.stMultiSelect span[data-baseweb="tag"]:hover { transform: translateY(-1px); box-shadow: 0 4px 10px rgba(13,148,136,0.35); }

/* ── Radio buttons ─────────────────────────────────────── */
[data-testid="stRadio"] > div { display: flex !important; gap: 0.8rem !important; flex-wrap: wrap !important; }
[data-testid="stRadio"] label { display: flex !important; align-items: center !important; gap: 0.5rem !important; background: #FFFFFF !important; border: 1.5px solid #E2E8F0 !important; border-radius: 10px !important; padding: 0.65rem 1.2rem !important; font-size: 0.92rem !important; font-weight: 500 !important; color: #475569 !important; cursor: pointer !important; transition: all 0.2s ease !important; min-width: 180px !important; }
[data-testid="stRadio"] label:hover { border-color: #0D9488 !important; color: #0D9488 !important; background: #F0FDF9 !important; }
[data-testid="stRadio"] label:has(input:checked) { background: #CCFBF1 !important; border-color: #0D9488 !important; color: #0F766E !important; font-weight: 600 !important; }
[data-testid="stRadio"] input[type="radio"] { display: none !important; }

/* ── Predict button ────────────────────────────────────── */
.stButton > button { background: linear-gradient(135deg, #0D9488 0%, #0F766E 50%, #115E59 100%) !important; background-size: 200% 200% !important; color: white !important; border: none !important; border-radius: 14px !important; padding: 1.1rem 3rem !important; font-size: 1.85rem !important; font-weight: 800 !important; letter-spacing: 0.02em !important; width: 100% !important; transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important; box-shadow: 0 6px 18px rgba(13,148,136,0.25) !important; position: relative; overflow: hidden; text-transform: uppercase; }
.stButton > button::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent); transition: left 0.6s ease; }
.stButton > button:hover { transform: translateY(-3px) !important; background-position: 100% 0 !important; box-shadow: 0 14px 32px rgba(13,148,136,0.4) !important; }
.stButton > button:hover::before { left: 100%; }
.stButton > button:active { transform: translateY(-1px) !important; }

/* ── Prediction hero card ──────────────────────────────── */
.prediction-hero { background: linear-gradient(135deg, #0D9488 0%, #0F766E 45%, #115E59 100%); background-size: 200% 200%; animation: gradientShift 6s ease infinite; border-radius: 20px; padding: 2rem; margin-bottom: 1.2rem; color: white; position: relative; overflow: hidden; box-shadow: 0 20px 40px rgba(13,148,136,0.25); }
.prediction-hero::before { content: ''; position: absolute; top: -50%; right: -20%; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%); pointer-events: none; }
.prediction-hero::after { content: ''; position: absolute; bottom: -30%; left: -10%; width: 300px; height: 300px; border-radius: 50%; background: radial-gradient(circle, rgba(94,234,212,0.15) 0%, transparent 70%); pointer-events: none; }

/* ── Animated symptom chips ────────────────────────────── */
.symptom-chip { background: linear-gradient(135deg, #F0FDF9 0%, #CCFBF1 100%); color: #0F766E; font-size: 0.88rem; font-weight: 600; padding: 0.45rem 0.95rem; border-radius: 999px; border: 1px solid #99F6E4; display: inline-block; margin: 0.2rem; box-shadow: 0 2px 6px rgba(13,148,136,0.08); animation: chipPop 0.4s ease-out both; transition: all 0.25s ease; }
.symptom-chip:hover { background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%); color: white; transform: translateY(-2px) scale(1.05); box-shadow: 0 6px 14px rgba(13,148,136,0.3); }

/* ── Dashboard stat cards ──────────────────────────────── */
.stat-card { background: linear-gradient(145deg, #FFFFFF 0%, #F0FDFA 100%); border: 1px solid #E2E8F0; border-radius: 14px; padding: 1.1rem 1.2rem; position: relative; overflow: hidden; transition: all 0.3s ease; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(180deg, #0D9488, #5EEAD4); }
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(13,148,136,0.1); }

/* ── Animated progress bar ─────────────────────────────── */
.progress-bar-track { background: #E2E8F0; border-radius: 999px; height: 10px; overflow: hidden; position: relative; }
.progress-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #0D9488, #5EEAD4); animation: progressFill 1.2s ease-out both; position: relative; }
.progress-bar-fill::after { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); animation: shimmer 2s linear infinite; background-size: 200% 100%; }

/* ── Loading spinner ───────────────────────────────────── */
.analyzing-box { background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%); border: 2px solid #5EEAD4; border-radius: 16px; padding: 2.5rem 1.5rem; text-align: center; animation: pulseGlow 1.8s ease-in-out infinite; }
.analyzing-box i { font-size: 2.5rem; color: #0D9488; animation: pulseGlow 1.5s ease-in-out infinite; }

/* ── Health summary info row ───────────────────────────── */
.info-pill { background: linear-gradient(135deg, #F0FDFA 0%, #F8FAFC 100%); border: 1px solid #E2E8F0; border-radius: 12px; padding: 0.9rem 1.1rem; display: flex; align-items: center; gap: 0.8rem; transition: all 0.25s ease; }
.info-pill:hover { border-color: #99F6E4; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(13,148,136,0.08); }
.info-pill-icon { width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, #0D9488, #5EEAD4); display: flex; align-items: center; justify-content: center; color: white; font-size: 1rem; flex-shrink: 0; }
.info-pill-label { color: #94A3B8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; }
.info-pill-value { color: #0F766E; font-size: 1.05rem; font-weight: 700; margin-top: 0.15rem; }

hr { border-color: #E2E8F0 !important; margin: 0.6rem 0 1rem 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F8FAFC; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #0D9488; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='height:0px;margin-top:-20px;'></div>", unsafe_allow_html=True)
    st.image("assets/Logo.png", width=180)
    st.markdown("""
    <div style='padding: 0 0.3rem;'>
        <div style='color: #94A3B8; font-size: 0.92rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; padding: 0 0.7rem; margin-bottom: 0.5rem;'>Navigation</div>
        <a href='/' target='_self' class='nav-item'>Overview</a>
        <a href='/Disease_Predictor' target='_self' class='nav-item nav-item-active'>Disease Predictor</a>
        <a href='/Model_Insights' target='_self' class='nav-item'>How It Works</a>
        <a href='/Health_Assistant' target='_self' class='nav-item'>Health Assistant</a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding: 0 0.3rem;'>
        <div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem 1rem;'>
            <div style='color: #94A3B8; font-size: 0.92rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem;'>Dataset</div>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;'>
                <span style='color: #64748B; font-size: 0.90rem; font-weight: 500;'>Patient Records</span>
                <span style='color: #0D9488; font-weight: 700; font-size: 0.92rem;'>4,921</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #64748B; font-size: 0.90rem; font-weight: 500;'>Diseases Covered</span>
                <span style='color: #0D9488; font-weight: 700; font-size: 0.92rem;'>42</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE HEADER
# ────────────────────────────────────────────────────────────
st.markdown("""
<div class='anim-fade-up' style='padding: 0.5rem 0 0.6rem 0;'>
    <span style='background: linear-gradient(135deg, #CCFBF1, #99F6E4); color: #0F766E; font-size: 0.90rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; padding: 0.35rem 0.9rem; border-radius: 999px; display: inline-block;'>
        <i class="fa-solid fa-wand-magic-sparkles" style="margin-right: 0.35rem;"></i> ML-Powered Prediction
    </span>
    <h1 style='font-size: 2.4rem; font-weight: 800; color: #0F172A; margin: 0.6rem 0 0.3rem 0; line-height: 1.15; background: linear-gradient(135deg, #0F172A 0%, #0F766E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>Disease Predictor</h1>
    <p style='font-size: 1.1rem; color: #64748B; margin: 0; max-width: 650px; line-height: 1.6;'>Select your symptoms below and let MediScan predict the most likely condition.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PATIENT DETAILS & SYMPTOMS
# ─────────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>Patient Details</div>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a: age = st.number_input("Age", min_value=1, max_value=120, value=25)
with col_b: gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])

st.markdown("<div class='section-label' style='margin-top:1.2rem;'>Symptoms</div>", unsafe_allow_html=True)
display_symptoms = [s.replace("_", " ").title() for s in all_symptoms]
symptom_map = {d: a for d, a in zip(display_symptoms, all_symptoms)}
selected_display = st.multiselect("Search and select all symptoms you are experiencing", options=display_symptoms, placeholder="Type to search symptoms...")
selected_symptoms = [symptom_map[s] for s in selected_display]

# ─────────────────────────────────────────────────────────────
# ANALYSIS MODE
# ─────────────────────────────────────────────────────────────
st.markdown("<div class='section-label' style='margin-top:1.2rem;'>Analysis Mode</div>", unsafe_allow_html=True)
mode_col1, mode_col2, mode_col3 = st.columns(3)
icon_quick = '<i class="fa-solid fa-bolt"></i>'
icon_balanced = '<i class="fa-solid fa-scale-balanced"></i>'
icon_deep = '<i class="fa-solid fa-microscope"></i>'

if "selected_mode" not in st.session_state: st.session_state.selected_mode = "Deep Analysis"

def mode_card(icon, title, desc, mode_name, btn_key):
    is_active = st.session_state.selected_mode == mode_name
    style = ("border: 2px solid #0D9488; background: linear-gradient(145deg, #F0FDF9 0%, #CCFBF1 100%);" if is_active else "border: 1.5px solid #E2E8F0; background: #FFFFFF;")
    st.markdown(f"""
    <div style='{style} border-radius: 14px; padding: 1.1rem 1.2rem; cursor: pointer; transition: all 0.25s ease;'>
        <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;'>
            <span style='color: #0D9488; font-size: 1.1rem;'>{icon}</span>
            <span style='font-weight: 700; color: #0F172A; font-size: 0.95rem;'>{title}</span>
        </div>
        <div style='color: #64748B; font-size: 0.88rem; line-height: 1.4;'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"Select {mode_name}", key=btn_key, use_container_width=True):
        st.session_state.selected_mode = mode_name
        st.rerun()

with mode_col1: mode_card(icon_quick, "Quick Check", "Fast probability-based result", "Quick Check", "btn_quick")
with mode_col2: mode_card(icon_balanced, "Balanced Analysis", "Similarity-based patient matching", "Balanced Analysis", "btn_balanced")
with mode_col3: mode_card(icon_deep, "Deep Analysis", "Most accurate — recommended", "Deep Analysis", "btn_deep")

st.markdown(f"""
<div style='background: linear-gradient(135deg, #F0FDFA 0%, #F8FAFC 100%); border: 1px solid #CCFBF1; border-radius: 12px; padding: 0.75rem 1.1rem; margin: 0.8rem 0 1.2rem 0; font-size: 1rem; color: #475569; display: flex; align-items: center; gap: 0.6rem;'>
    <i class="fa-solid fa-circle-check" style="color: #0D9488; font-size: 1.1rem;"></i>
    <span>Currently selected: <strong style='color: #0F766E; font-weight: 700;'>{st.session_state.selected_mode}</strong></span>
</div>
""", unsafe_allow_html=True)

predict_btn = st.button(" Predict Disease", use_container_width=True)

# ────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────
if predict_btn:
    if len(selected_symptoms) < 2:
        st.warning("Please select at least 2 symptoms for an accurate prediction.")
    else:
        loading_slot = st.empty()
        with loading_slot:
            st.markdown("""
            <div class='analyzing-box anim-scale'>
                <i class="fa-solid fa-dna"></i>
                <div style='margin-top: 0.8rem; font-size: 1.2rem; font-weight: 700; color: #0F766E;'>Analyzing symptoms...</div>
                <div style='margin-top: 0.4rem; font-size: 0.92rem; color: #64748B;'>Running ML model across 42 conditions</div>
                <div style='margin-top: 1rem; display: flex; justify-content: center; gap: 0.5rem;'>
                    <span style='width: 10px; height: 10px; border-radius: 50%; background: #0D9488; animation: pulseGlow 1.2s ease-in-out infinite;'></span>
                    <span style='width: 10px; height: 10px; border-radius: 50%; background: #0D9488; animation: pulseGlow 1.2s ease-in-out infinite 0.2s;'></span>
                    <span style='width: 10px; height: 10px; border-radius: 50%; background: #0D9488; animation: pulseGlow 1.2s ease-in-out infinite 0.4s;'></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1.3)
        loading_slot.empty()

        prediction, top_3 = predict_disease(selected_symptoms, st.session_state.selected_mode)
        symptom_importance = get_symptom_importance(selected_symptoms)
        severity = severity_map.get(prediction, "Medium ").strip()
        precs = precautions.get(prediction, [])
        confidence = round(top_3[0][1] * 100, 1)

        # ─ NEW LOGIC: Clinical Recommendation & Confidence Interpretation ──
        if severity == "High":
            clinical_rec, rec_color, rec_bg = "Urgent care required", "#EF4444", "#FEF2F2"
        elif severity == "Medium":
            clinical_rec, rec_color, rec_bg = "Consult doctor", "#F59E0B", "#FFFBEB"
        elif confidence >= 60:
            clinical_rec, rec_color, rec_bg = "Monitor symptoms", "#3B82F6", "#EFF6FF"
        else:
            clinical_rec, rec_color, rec_bg = "Self-care advised", "#10B981", "#ECFDF5"

        if confidence >= 75: conf_interp, interp_color = "Very Confident", "#0D9488"
        elif confidence >= 50: conf_interp, interp_color = "Moderate", "#F59E0B"
        else: conf_interp, interp_color = "Uncertain", "#EF4444"

        # ── NEW LOGIC: Risk Breakdown Calculation ──
        low_risk = med_risk = high_risk = 0.0
        for dis, prob in top_3:
            sev = severity_map.get(dis.strip(), "Medium").strip()
            if sev == "Low": low_risk += prob
            elif sev == "Medium": med_risk += prob
            elif sev == "High": high_risk += prob
        low_pct, med_pct, high_pct = round(low_risk * 100, 1), round(med_risk * 100, 1), round(high_risk * 100, 1)

        severity_color = {"Low": "#22C55E", "Medium": "#F59E0B", "High": "#EF4444"}
        severity_bg = {"Low": "#F0FFF4", "Medium": "#FFFBEB", "High": "#FFF1F1"}
        sev_col = severity_color.get(severity, "#F59E0B")
        sev_bg = severity_bg.get(severity, "#FFFBEB")

        st.markdown("<hr style='margin: 0 0 1.2rem 0;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Your Results</div>", unsafe_allow_html=True)

        # ── Hero prediction card ───────────────────────────
        st.markdown(f"""
        <div class='prediction-hero anim-fade-up'>
            <div style='position: relative; z-index: 2;'>
                <div style='font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; opacity: 0.85; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;'>
                    <i class="fa-solid fa-stethoscope"></i> Predicted Condition
                </div>
                <div style='font-size: 2.4rem; font-weight: 800; margin-bottom: 0.8rem; line-height: 1.1;'>{prediction}</div>
                <div style='display: flex; align-items: center; gap: 0.7rem; flex-wrap: wrap;'>
                    <div style='background: {sev_bg}; color: {sev_col}; border-radius: 10px; padding: 0.4rem 1rem; font-size: 0.88rem; font-weight: 700; border: 1px solid {sev_col}33;'>
                        <i class="fa-solid fa-triangle-exclamation" style="margin-right: 0.35rem;"></i> {severity} Severity
                    </div>
                    <div style='background: {rec_bg}; color: {rec_color}; border-radius: 10px; padding: 0.4rem 1rem; font-size: 0.88rem; font-weight: 700; border: 1px solid {rec_color}33;'>
                        <i class="fa-solid fa-user-doctor" style="margin-right: 0.35rem;"></i> {clinical_rec}
                    </div>
                    <div style='background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.4rem 1rem; font-size: 0.88rem; font-weight: 600; border: 1px solid rgba(255,255,255,0.2);'>
                        <i class="fa-solid fa-gears" style="margin-right: 0.35rem;"></i> {st.session_state.selected_mode}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 3 Stat cards ───────────────────────────────────
        stat1, stat2, stat3 = st.columns(3)
        with stat1:
            st.markdown(f"""
            <div class='stat-card anim-fade-up anim-delay-1'>
                <div style='color: #94A3B8; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;'>Model Confidence</div>
                <div style='font-size: 1.6rem; font-weight: 800; color: {interp_color}; margin: 0.3rem 0; display: flex; align-items: center; gap: 0.5rem;'>
                    <i class="fa-solid fa-brain" style="font-size: 1.4rem;"></i> {conf_interp}
                </div>
                <div style='font-size: 0.82rem; color: #64748B;'>Interpretation</div>
            </div>
            """, unsafe_allow_html=True)
        with stat2:
            st.markdown(f"""
            <div class='stat-card anim-fade-up anim-delay-2'>
                <div style='color: #94A3B8; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;'>Risk Breakdown</div>
                <div style='margin: 0.5rem 0; display: flex; flex-direction: column; gap: 0.3rem;'>
                    <div style='display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569;'><span>Low</span><span style='font-weight:700; color:#10B981;'>{low_pct}%</span></div>
                    <div class='progress-bar-track' style='height: 6px;'><div class='progress-bar-fill' style='width: {low_pct}%; background: #10B981;'></div></div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569; margin-top:0.2rem;'><span>Medium</span><span style='font-weight:700; color:#F59E0B;'>{med_pct}%</span></div>
                    <div class='progress-bar-track' style='height: 6px;'><div class='progress-bar-fill' style='width: {med_pct}%; background: #F59E0B;'></div></div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569; margin-top:0.2rem;'><span>High</span><span style='font-weight:700; color:#EF4444;'>{high_pct}%</span></div>
                    <div class='progress-bar-track' style='height: 6px;'><div class='progress-bar-fill' style='width: {high_pct}%; background: #EF4444;'></div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with stat3:
            st.markdown(f"""
            <div class='stat-card anim-fade-up anim-delay-3'>
                <div style='color: #94A3B8; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;'>Symptoms</div>
                <div style='font-size: 1.8rem; font-weight: 800; color: #0D9488; margin: 0.3rem 0;'>{len(selected_symptoms)}</div>
                <div style='font-size: 0.82rem; color: #64748B;'>Analyzed</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Health Summary ─────────────────────────────────
        symptom_tags = " ".join([f"<span class='symptom-chip' style='animation-delay: {0.08*i}s;'><i class='fa-solid fa-virus' style='margin-right: 0.3rem; font-size: 0.75rem;'></i>{s.replace('_',' ').title()}</span>" for i, s in enumerate(selected_symptoms)])
        st.markdown(f"""
        <div class='medi-card anim-fade-up anim-delay-2'>
            <div style='font-size: 1.35rem; font-weight: 700; color: #0F766E; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.6rem;'>
                <i class="fa-solid fa-user-doctor" style="color: #0D9488; font-size: 1.4rem;"></i> Health Summary
            </div>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin-bottom: 1rem;'>
                <div class='info-pill'>
                    <div class='info-pill-icon'><i class="fa-solid fa-cake-candles"></i></div>
                    <div><div class='info-pill-label'>Age</div><div class='info-pill-value'>{age} years</div></div>
                </div>
                <div class='info-pill'>
                    <div class='info-pill-icon'><i class="fa-solid fa-venus-mars"></i></div>
                    <div><div class='info-pill-label'>Gender</div><div class='info-pill-value'>{gender}</div></div>
                </div>
            </div>
            <div style='background: linear-gradient(135deg, #F0FDFA 0%, #F8FAFC 100%); border: 1px solid #E2E8F0; border-radius: 12px; padding: 1rem 1.1rem;'>
                <div style='color: #94A3B8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.4rem;'>
                    <i class="fa-solid fa-stethoscope" style="color: #0D9488;"></i> Symptoms Entered ({len(selected_symptoms)})
                </div>
                <div style='line-height: 1.9;'>{symptom_tags}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Precautions ────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        prec_items = " ".join([f"<div class='anim-fade-up' style='animation-delay: {0.08*i}s; display: flex; align-items: flex-start; gap: 0.7rem; background: linear-gradient(135deg, #F0FDFA 0%, #F8FAFC 100%); border-radius: 10px; padding: 0.85rem; border: 1px solid #E2E8F0; transition: all 0.25s ease;'><div style='width: 26px; height: 26px; border-radius: 50%; background: linear-gradient(135deg, #0D9488, #5EEAD4); display: flex; align-items: center; justify-content: center; flex-shrink: 0;'><i class='fa-solid fa-check' style='color: white; font-size: 0.72rem;'></i></div><span style='color: #334155; font-size: 0.88rem; font-weight: 500; line-height: 1.5;'>{p.capitalize()}</span></div>" for i, p in enumerate(precs)])
        st.markdown(f"""
        <div class='medi-card anim-fade-up anim-delay-3'>
            <div style='font-size: 1.35rem; font-weight: 700; color: #0F766E; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.6rem;'>
                <i class="fa-solid fa-shield-heart" style="color: #0D9488; font-size: 1.4rem;"></i> Precautions & Next Steps
            </div>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;'>{prec_items}</div>
            <div style='margin-top: 1rem; padding: 0.7rem 1rem; border-radius: 10px; background: linear-gradient(135deg, #FEF3C7, #FFFBEB); border-left: 3px solid #F59E0B; color: #92400E; font-size: 0.82rem; font-weight: 500; display: flex; align-items: center; gap: 0.5rem;'>
                <i class="fa-solid fa-triangle-exclamation" style="font-size: 1rem;"></i> Always consult a qualified doctor for proper diagnosis and treatment.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Dashboard Charts (UNCHANGED) ───────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Visual Health Report</div>", unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            diseases = [d for d, _ in top_3]
            probs = [round(p * 100, 1) for _, p in top_3]

            st.markdown("<div class='chart-section-heading'>Confidence Score</div>", unsafe_allow_html=True)
            fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=confidence, number={'suffix': '%', 'font': {'size': 32, 'color': '#0F766E', 'family': 'Inter'}}, gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8", 'tickfont': {'size': 10, 'color': '#64748B'}}, 'bar': {'color': "#0D9488"}, 'bgcolor': "#F1F5F9", 'borderwidth': 2, 'bordercolor': "#E2E8F0", 'steps': [{'range': [0, 40], 'color': '#FEE2E2'}, {'range': [40, 70], 'color': '#FEF3C7'}, {'range': [70, 100],'color': '#D1FAE5'}], 'threshold': {'line': {'color': "#0F766E", 'width': 4}, 'thickness': 0.8, 'value': confidence}}))
            fig_gauge.update_layout(height=200, margin=dict(l=20, r=20, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'family': 'Inter'})
            st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

            st.markdown("<div class='chart-section-heading' style='margin-top: 0.5rem;'>Disease Probability Distribution</div>", unsafe_allow_html=True)
            bar_colors = ['#0D9488', '#5EEAD4', '#99F6E4']
            fig_bars = go.Figure(go.Bar(x=probs, y=diseases, orientation="h", marker=dict(color=bar_colors[:len(probs)], line=dict(color='#0F766E', width=1)), text=[f"{p}%" for p in probs], textposition="outside", textfont=dict(size=12, color="#0F766E", family="Inter")))
            fig_bars.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(l=10, r=60, t=10, b=10), xaxis=dict(showgrid=False, showticklabels=False, range=[0, max(probs) * 1.35]), yaxis=dict(showgrid=False, tickfont=dict(size=11, color="#475569", family="Inter")), showlegend=False)
            st.plotly_chart(fig_bars, use_container_width=True, config={"displayModeBar": False})

        with chart_col2:
            if symptom_importance:
                imp_symptoms = list(symptom_importance.keys())[:8]
                imp_scores = [round(v, 3) for v in list(symptom_importance.values())[:8]]
                imp_labels = [s.replace("_", " ").title() for s in imp_symptoms]

                st.markdown("<div class='chart-section-heading' style='text-align: center; justify-content: center;'>Prediction Confidence</div>", unsafe_allow_html=True)
                fig_radar = go.Figure(go.Scatterpolar(r=imp_scores + [imp_scores[0]], theta=imp_labels + [imp_labels[0]], fill='toself', fillcolor='rgba(13,148,136,0.28)', line=dict(color='#0D9488', width=2.5), marker=dict(size=10, color='#0F766E', line=dict(color='white', width=2.5), symbol='circle')))
                fig_radar.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, gridcolor='#E2E8F0', tickfont=dict(size=10, color='#94A3B8'), range=[0, max(imp_scores) * 1.25] if imp_scores else [0, 1]), angularaxis=dict(gridcolor='#E2E8F0', tickfont=dict(size=11, color='#475569', family='Inter', weight=600), tickvals=imp_labels, rotation=90)), showlegend=False, height=460, margin=dict(l=90, r=90, t=30, b=30), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
