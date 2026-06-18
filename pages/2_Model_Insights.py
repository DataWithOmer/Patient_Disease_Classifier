import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
from model import get_model_accuracies

st.set_page_config(
    page_title="MediScan — Model Insights",
    page_icon="assets/Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

accuracies = get_model_accuracies()

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

/* ── Animations ── */
@keyframes fadeInUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes pulseGlow { 0%, 100% { box-shadow: 0 8px 24px rgba(13,148,136,0.18); } 50% { box-shadow: 0 12px 36px rgba(13,148,136,0.35); } }
@keyframes progressFill { from { width: 0%; } }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.92); } to { opacity: 1; transform: scale(1); } }

.anim-fade-up { animation: fadeInUp 0.6s ease-out both; }
.anim-scale { animation: scaleIn 0.5s ease-out both; }
.anim-delay-1 { animation-delay: 0.1s; }
.anim-delay-2 { animation-delay: 0.25s; }
.anim-delay-3 { animation-delay: 0.4s; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
[data-testid="stSidebarHeader"] { display: none !important; height: 0 !important; padding: 0 !important; margin: 0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarUserContent"] { padding-top: 0 !important; margin-top: 0 !important; padding-left: 1rem !important; padding-right: 1rem !important; }

.nav-item { display: block; padding: 0.48rem 1rem; border-radius: 8px; color: #64748B; font-size: 1.05rem; font-weight: 500; text-decoration: none !important; transition: all 0.2s ease; margin-bottom: 0.15rem; }
.nav-item:hover { background-color: #F0FDF9; color: #0D9488; text-decoration: none !important; }
.nav-item-active { background-color: #CCFBF1 !important; color: #0F766E !important; font-weight: 600 !important; border-left: 3px solid #0D9488 !important; text-decoration: none !important; }

/* ── Cards ── */
.medi-card { background: linear-gradient(145deg, #FFFFFF 0%, #FAFFFE 100%); border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(15,23,42,0.04); transition: all 0.3s ease; position: relative; overflow: hidden; }
.medi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #0D9488, #5EEAD4, #0D9488); background-size: 200% 100%; animation: shimmer 3s linear infinite; opacity: 0.6; }
.medi-card:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(13,148,136,0.12); border-color: #99F6E4; }

/* ── Section label ── */
.section-label { font-size: 1.25rem; font-weight: 800; color: #0F766E; text-transform: uppercase; letter-spacing: 0.13em; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.5rem; }
.section-label::before { content: ''; width: 4px; height: 18px; border-radius: 2px; background: linear-gradient(180deg, #0D9488, #5EEAD4); }

/* ── Algo card ── */
.algo-card { background: linear-gradient(145deg, #FFFFFF 0%, #FAFFFE 100%); border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.8rem; height: 100%; box-shadow: 0 2px 8px rgba(15,23,42,0.04); transition: all 0.3s ease; position: relative; overflow: hidden; }
.algo-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #0D9488, #5EEAD4, #0D9488); background-size: 200% 100%; animation: shimmer 3s linear infinite; opacity: 0.6; }
.algo-card:hover { transform: translateY(-3px); box-shadow: 0 14px 32px rgba(13,148,136,0.14); border-color: #5EEAD4; }

/* ── Mode badge ── */
.mode-badge { display: inline-flex; align-items: center; gap: 0.4rem; background: linear-gradient(135deg, #CCFBF1, #99F6E4); color: #0F766E; font-size: 0.78rem; font-weight: 700; padding: 0.25rem 0.8rem; border-radius: 999px; border: 1px solid #5EEAD4; margin-bottom: 0.9rem; }

/* ── Accuracy badge ── */
.accuracy-badge { display: inline-flex; align-items: center; gap: 0.4rem; background: linear-gradient(135deg, #0D9488, #0F766E); color: white; font-size: 0.82rem; font-weight: 700; padding: 0.3rem 0.9rem; border-radius: 999px; box-shadow: 0 3px 8px rgba(13,148,136,0.3); }

/* ── Step item ── */
.step-item { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.55rem 0; border-bottom: 1px solid #F0FDFA; }
.step-num { width: 24px; height: 24px; min-width: 24px; border-radius: 50%; background: linear-gradient(135deg, #CCFBF1, #99F6E4); border: 1.5px solid #0D9488; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 800; color: #0F766E; margin-top: 1px; }

/* ── Stat card ── */
.stat-card { background: linear-gradient(145deg, #FFFFFF 0%, #F0FDFA 100%); border: 1px solid #E2E8F0; border-radius: 14px; padding: 1.1rem 1.2rem; position: relative; overflow: hidden; transition: all 0.3s ease; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(180deg, #0D9488, #5EEAD4); }
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(13,148,136,0.1); }

/* ── Pipeline step ── */
.pipeline-step { display: flex; align-items: flex-start; gap: 1rem; padding: 0.9rem 0; border-bottom: 1px solid #F1F5F9; transition: all 0.2s ease; }
.pipeline-step:hover { background: linear-gradient(135deg, #F0FDFA, #F8FAFC); border-radius: 8px; padding-left: 0.5rem; }
.pipeline-num { font-size: 1.1rem; font-weight: 800; color: #0D9488; min-width: 36px; opacity: 0.7; }

/* ── Progress bar ── */
.progress-bar-track { background: #E2E8F0; border-radius: 999px; height: 8px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #0D9488, #5EEAD4); animation: progressFill 1.2s ease-out both; }

/* ── Chart heading ── */
.chart-heading { font-size: 1.1rem; font-weight: 700; color: #0F766E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem; padding-bottom: 0.4rem; border-bottom: 2px solid #E2E8F0; }
.chart-heading::before { content: ''; width: 4px; height: 16px; border-radius: 2px; background: linear-gradient(180deg, #0D9488, #5EEAD4); }

hr { border-color: #E2E8F0 !important; margin: 0.6rem 0 1rem 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F8FAFC; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #0D9488; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='height:0px;margin-top:-20px;'></div>",
                unsafe_allow_html=True)
    st.image("assets/Logo.png", width=180)
    st.markdown("""
    <div style='padding: 0 0.3rem;'>
        <div style='color: #94A3B8; font-size: 0.92rem; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 0.12em;
                    padding: 0 0.7rem; margin-bottom: 0.5rem;'>Navigation</div>
        <a href='/' target='_self' class='nav-item'>Overview</a>
        <a href='/Disease_Predictor' target='_self' class='nav-item'>Disease Predictor</a>
        <a href='/Model_Insights' target='_self'
           class='nav-item nav-item-active'>Model Insights</a>
        <a href='/Health_Assistant' target='_self' class='nav-item'>Health Assistant</a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding: 0 0.3rem;'>
        <div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
                    padding: 0.85rem 1rem;'>
            <div style='color: #94A3B8; font-size: 0.92rem; font-weight: 700;
                        text-transform: uppercase; letter-spacing: 0.1em;
                        margin-bottom: 0.6rem;'>Dataset</div>
            <div style='display: flex; justify-content: space-between;
                        align-items: center; margin-bottom: 0.35rem;'>
                <span style='color: #64748B; font-size: 0.9rem;
                             font-weight: 500;'>Patient Records</span>
                <span style='color: #0D9488; font-weight: 700;
                             font-size: 0.92rem;'>4,921</span>
            </div>
            <div style='display: flex; justify-content: space-between;
                        align-items: center;'>
                <span style='color: #64748B; font-size: 0.9rem;
                             font-weight: 500;'>Diseases Covered</span>
                <span style='color: #0D9488; font-weight: 700;
                             font-size: 0.92rem;'>42</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────
st.markdown("""
<div class='anim-fade-up' style='padding: 0.5rem 0 0.6rem 0;'>
    <span style='background: linear-gradient(135deg, #CCFBF1, #99F6E4); color: #0F766E;
                 font-size: 0.90rem; font-weight: 700; text-transform: uppercase;
                 letter-spacing: 0.12em; padding: 0.35rem 0.9rem; border-radius: 999px;
                 display: inline-block;'>
        <i class="fa-solid fa-flask" style="margin-right: 0.35rem;"></i>
        Behind the Scenes
    </span>
    <h1 style='font-size: 2.4rem; font-weight: 800; margin: 0.6rem 0 0.3rem 0;
               line-height: 1.15; background: linear-gradient(135deg, #0F172A 0%, #0F766E 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               background-clip: text;'>Model Insights</h1>
    <p style='font-size: 1.1rem; color: #64748B; margin: 0; max-width: 620px;
              line-height: 1.6;'>
        A plain English breakdown of the three ML algorithms powering MediScan
        — how they think, how they work, and how accurate they are.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Accuracy Stat Cards ───────────────────────────────────────
nb_acc  = accuracies.get("Quick Check (Naive Bayes)", 0)
knn_acc = accuracies.get("Balanced Analysis (KNN)", 0)
rf_acc  = accuracies.get("Deep Analysis (Random Forest)", 0)

st.markdown("<div class='section-label'>Model Performance</div>",
            unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)
stat_data = [
    (s1, "fa-bolt", "Quick Check", "Naive Bayes", nb_acc,  "#3B82F6"),
    (s2, "fa-wave-square", "Balanced Analysis", "KNN", knn_acc, "#F59E0B"),
    (s3, "fa-microscope", "Deep Analysis", "Random Forest", rf_acc, "#0D9488"),
]
for col, icon, mode, algo, acc, color in stat_data:
    with col:
        st.markdown(f"""
        <div class='stat-card anim-fade-up'>
            <div style='display: flex; justify-content: space-between;
                        align-items: flex-start; margin-bottom: 0.6rem;'>
                <div>
                    <div style='color: #94A3B8; font-size: 0.75rem; font-weight: 700;
                                text-transform: uppercase; letter-spacing: 0.1em;'>
                        {mode}</div>
                    <div style='color: #0F172A; font-size: 0.95rem; font-weight: 700;
                                margin-top: 0.2rem;'>{algo}</div>
                </div>
                <i class="fa-solid {icon}" style="color: {color};
                   font-size: 1.4rem; opacity: 0.85;"></i>
            </div>
            <div style='font-size: 2rem; font-weight: 800; color: {color};
                        margin-bottom: 0.4rem;'>{acc}%</div>
            <div class='progress-bar-track'>
                <div class='progress-bar-fill'
                     style='width: {acc}%; background: {color};'></div>
            </div>
            <div style='color: #94A3B8; font-size: 0.75rem; margin-top: 0.4rem;'>
                Model Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Algorithm Cards ───────────────────────────────────────────
st.markdown("<div class='section-label'>The Three Algorithms</div>",
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

algorithms = [
    (
        col1,
        "fa-bolt", "#3B82F6",
        "Naive Bayes", "Quick Check", nb_acc,
        "A probability-based classifier that evaluates each symptom independently and calculates the statistical likelihood of each disease.",
        [
            "Looks at every entered symptom one by one",
            "Calculates how often each symptom co-occurs with each disease in training data",
            "Multiplies all individual probabilities together for a final score",
            "Returns the disease with the highest combined probability"
        ],
        "Best for fast lightweight predictions. Great accuracy on clean symptom data."
    ),
    (
        col2,
        "fa-wave-square", "#F59E0B",
        "K-Nearest Neighbors", "Balanced Analysis", knn_acc,
        "A similarity-based algorithm that finds the 5 most similar past patients and predicts based on their confirmed diagnoses.",
        [
            "Converts your symptoms into a binary vector pattern",
            "Scans all 4,921 patient records for the closest matches",
            "Identifies the 5 most similar patients — the nearest neighbors",
            "Returns the most common disease diagnosis among those 5 matches"
        ],
        "Best when your symptom combination closely matches existing patient records."
    ),
    (
        col3,
        "fa-microscope", "#0D9488",
        "Random Forest", "Deep Analysis", rf_acc,
        "An ensemble classifier that builds 100 independent decision trees and combines their votes for the most reliable prediction.",
        [
            "Builds 100 decision trees each trained on a random data subset",
            "Each tree independently analyzes your symptoms and predicts a disease",
            "All 100 trees cast a vote for their best prediction",
            "The disease with the most votes wins — ensemble majority rules"
        ],
        "Most accurate model. Recommended for all cases — especially complex symptom sets."
    ),
]

for col, icon, color, name, mode, acc, summary, steps, note in algorithms:
    with col:
        steps_html = "".join([
            f"""<div class='step-item'>
                <div class='step-num'>{i+1}</div>
                <div style='color:#475569; font-size:0.82rem;
                            line-height:1.5;'>{step}</div>
            </div>"""
            for i, step in enumerate(steps)
        ])
        st.markdown(f"""
        <div class='algo-card anim-fade-up'>
            <div style='width:48px; height:48px; border-radius:12px;
                        background: linear-gradient(135deg, {color}18, {color}30);
                        border: 1.5px solid {color}40;
                        display:flex; align-items:center; justify-content:center;
                        margin-bottom:1rem;'>
                <i class="fa-solid {icon}" style="color:{color}; font-size:1.4rem;"></i>
            </div>
            <div class='mode-badge'>
                <i class="fa-solid fa-tag" style="font-size:0.7rem;"></i>
                {mode}
            </div>
            <div style='font-size:1.08rem; font-weight:800; color:#0F172A;
                        margin-bottom:0.4rem;'>{name}</div>
            <div style='color:#64748B; font-size:0.95rem; line-height:1.6;
                        margin-bottom:1rem;'>{summary}</div>
            <div style='font-size:0.72rem; font-weight:700; color:#94A3B8;
                        text-transform:uppercase; letter-spacing:0.1em;
                        margin-bottom:0.5rem;'>Step by Step</div>
            {steps_html}
            <div style='margin-top:1rem; padding:0.65rem 0.9rem;
                        background: linear-gradient(135deg, #F0FDFA, #F8FAFC);
                        border-radius:10px; border-left:3px solid #0D9488;'>
                <div style='color:#0F766E; font-size:0.79rem;
                            line-height:1.5;'>{note}</div>
            </div>
            <div style='margin-top:1rem; display:flex; align-items:center;
                        justify-content:space-between;'>
                <span style='color:#94A3B8; font-size:0.88rem;
                             font-weight:600;'>Accuracy</span>
                <span class='accuracy-badge'>
                    <i class="fa-solid fa-chart-line" style="font-size:0.7rem;"></i>
                    {acc}%
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── ML Pipeline ───────────────────────────────────────────────
st.markdown("<div class='section-label'>The ML Pipeline</div>",
            unsafe_allow_html=True)

pipeline_steps = [
    ("01", "fa-database",    "Dataset Loaded",
     "4,921 patient records loaded from CSV with 17 symptom columns and disease labels"),
    ("02", "fa-wand-sparkles", "Preprocessing",
     "Empty symptom slots filled. All 132 unique symptoms encoded as binary 0/1 columns"),
    ("03", "fa-scissors",    "Train / Test Split",
     "80% of records used for training, 20% held back to evaluate accuracy"),
    ("04", "fa-gears",       "Model Training",
     "All three models trained simultaneously on the training set at app startup"),
    ("05", "fa-keyboard",    "User Input Encoded",
     "Your selected symptoms converted to the same binary format the models understand"),
    ("06", "fa-brain",       "Prediction Made",
     "Selected model runs inference and returns a probability score for every disease"),
    ("07", "fa-chart-bar",   "Results Displayed",
     "Top prediction, confidence score, charts, severity and precautions rendered instantly"),
]

p1, p2 = st.columns(2)
half = 4

for i, (num, icon, title, desc) in enumerate(pipeline_steps):
    col = p1 if i < half else p2
    with col:
        st.markdown(f"""
        <div class='pipeline-step'>
            <div style='display:flex; align-items:center; justify-content:center;
                        width:38px; height:38px; min-width:38px;
                        background: linear-gradient(135deg, #CCFBF1, #99F6E4);
                        border-radius:10px; border:1.5px solid #5EEAD4;'>
                <i class="fa-solid {icon}" style="color:#0D9488; font-size:0.9rem;"></i>
            </div>
            <div>
                <div style='display:flex; align-items:center; gap:0.5rem;
                            margin-bottom:0.2rem;'>
                    <span style='font-size:1rem; font-weight:800; color:#0D9488;
                                 opacity:0.7;'>{num}</span>
                    <span style='font-weight:700; color:#0F172A;
                                 font-size:0.9rem;'>{title}</span>
                </div>
                <div style='color:#64748B; font-size:1rem;
                            line-height:1.55;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='color:#94A3B8; font-size:0.92rem; text-align:center;
            padding-top:0.8rem; border-top:1px solid #E2E8F0;'>
    ⚠️ MediScan is not a substitute for professional medical advice.
    Always consult a qualified doctor for diagnosis and treatment.
</div>
""", unsafe_allow_html=True)