import streamlit as st
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from groq import Groq

st.set_page_config(
    page_title="MediScan — Health Assistant",
    page_icon="assets/Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

@keyframes fadeInUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
@keyframes pulseGlow { 0%, 100% { box-shadow: 0 8px 24px rgba(13,148,136,0.18); } 50% { box-shadow: 0 12px 36px rgba(13,148,136,0.35); } }
@keyframes typing { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

.anim-fade-up { animation: fadeInUp 0.6s ease-out both; }
.anim-delay-1 { animation-delay: 0.1s; }
.anim-delay-2 { animation-delay: 0.25s; }

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

/* ── Section label ─ */
.section-label { font-size: 1.25rem; font-weight: 800; color: #0F766E; text-transform: uppercase; letter-spacing: 0.13em; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.5rem; }
.section-label::before { content: ''; width: 4px; height: 18px; border-radius: 2px; background: linear-gradient(180deg, #0D9488, #5EEAD4); }

/* ── Text area & Placeholder ── */
[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 12px !important;
    color: #1E293B !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.6 !important;
    resize: none !important;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: #94A3B8 !important;
    opacity: 1;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #0D9488 !important;
    box-shadow: 0 0 0 3px rgba(13,148,136,0.1) !important;
}
[data-testid="stTextArea"] label p {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #1E293B !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #0D9488 0%, #0F766E 50%, #115E59 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(13,148,136,0.25) !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(13,148,136,0.4) !important;
}

/* ─ Answer box ── */
.answer-box {
    background: linear-gradient(145deg, #FFFFFF 0%, #F0FDFA 100%);
    border: 1.5px solid #99F6E4;
    border-radius: 16px;
    padding: 1.2rem;
    margin-top: 0.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(13,148,136,0.08);
    animation: fadeInUp 0.5s ease-out both;
    position: relative;
    overflow: hidden;
}
.answer-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #0D9488, #5EEAD4, #0D9488);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}

/* ── Suggestion chips ── */
.suggestion-chip {
    display: inline-block;
    background: linear-gradient(135deg, #F0FDFA, #CCFBF1);
    color: #0F766E;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    border: 1px solid #99F6E4;
    margin: 0.2rem;
    box-shadow: 0 1px 4px rgba(13,148,136,0.08);
}

/* ── Typing dots ─ */
.typing-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #0D9488;
    animation: typing 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

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
    st.markdown("<div style='height:0px;margin-top:-20px;'></div>", unsafe_allow_html=True)
    st.image("assets/Logo.png", width=180)
    st.markdown("""
    <div style='padding: 0 0.3rem;'>
        <div style='color: #94A3B8; font-size: 0.92rem; font-weight: 700;
            text-transform: uppercase; letter-spacing: 0.12em;
            padding: 0 0.7rem; margin-bottom: 0.5rem;'>Navigation</div>
        <a href='/' target='_self' class='nav-item'>Overview</a>
        <a href='/Disease_Predictor' target='_self' class='nav-item'>Disease Predictor</a>
        <a href='/Model_Insights' target='_self' class='nav-item'>Model Insights</a>
        <a href='/Health_Assistant' target='_self'
            class='nav-item nav-item-active'>Health Assistant</a>
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
                <span style='color: #64748B; font-size: 0.9rem; font-weight: 500;'>Patient Records</span>
                <span style='color: #0D9488; font-weight: 700; font-size: 0.92rem;'>4,921</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #64748B; font-size: 0.9rem; font-weight: 500;'>Diseases Covered</span>
                <span style='color: #0D9488; font-weight: 700; font-size: 0.92rem;'>42</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Load API Key ──────────────────────────────────────────────
api_key = st.secrets["GROQ_API_KEY"]

# ── Page Header ───────────────────────────────────────────────
st.markdown("""
<div class='anim-fade-up' style='padding: 0.5rem 0 0.6rem 0;'>
    <span style='background: linear-gradient(135deg, #CCFBF1, #99F6E4); color: #0F766E;
        font-size: 0.90rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.12em; padding: 0.35rem 0.9rem; border-radius: 999px;
        display: inline-block;'>
        <i class="fa-solid fa-robot" style="margin-right: 0.35rem;"></i>
        AI Powered
    </span>
    <h1 style='font-size: 2.4rem; font-weight: 800; margin: 0.6rem 0 0.3rem 0;
        line-height: 1.15; background: linear-gradient(135deg, #0F172A 0%, #0F766E 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;'>Health Assistant</h1>
    <p style='font-size: 1.1rem; color: #64748B; margin: 0; max-width: 620px;
        line-height: 1.6;'>
        Ask any question about symptoms, diseases, or medications and get
        an instant AI-powered answer in plain English.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Question Input ───────────────────────────────────────────
st.markdown("<div class='section-label'>Ask a Health Question</div>", unsafe_allow_html=True)
st.markdown("""
<div style='margin-bottom: 0.8rem;'>
    <div style='color: #64748B; font-size: 0.88rem; font-weight: 500;
        margin-bottom: 0.5rem;'>Try asking:</div>
    <div>
        <span class='suggestion-chip'>What are symptoms of typhoid?</span>
        <span class='suggestion-chip'>Is paracetamol safe for fever?</span>
        <span class='suggestion-chip'>Foods to avoid with jaundice?</span>
        <span class='suggestion-chip'>How is dengue diagnosed?</span>
        <span class='suggestion-chip'>What causes high blood pressure?</span>
        <span class='suggestion-chip'>How to prevent malaria?</span>
    </div>
</div>
""", unsafe_allow_html=True)

question = st.text_area(
    "Your Question",
    placeholder="e.g. What are the early symptoms of diabetes? "
                "Is it safe to take ibuprofen with high blood pressure?",
    height=130
)
ask_btn = st.button("  Ask Health Assistant", use_container_width=True)

# ── Answer ───────────────────────────
if ask_btn:
    if not question.strip():
        st.warning("Please type a health question before submitting.")
    else:
        loading_slot = st.empty()
        loading_slot.markdown("""
        <div style='display: flex; align-items: center; gap: 0.8rem;
            padding: 1.2rem 1.5rem; margin-top: 1rem;
            background: linear-gradient(135deg, #F0FDFA, #CCFBF1);
            border-radius: 12px; border: 1px solid #5EEAD4;'>
            <i class="fa-solid fa-robot" style="color: #0D9488; font-size: 1.3rem;"></i>
            <div>
                <div style='color: #0F766E; font-size: 0.92rem; font-weight: 600;
                    margin-bottom: 0.3rem;'>Health Assistant is thinking...</div>
                <div style='display: flex; gap: 0.3rem;'>
                    <span class='typing-dot'></span>
                    <span class='typing-dot'></span>
                    <span class='typing-dot'></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        try:
            client = Groq(api_key=api_key)

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """You are MediScan Health Assistant, a professional medical information assistant. You ONLY answer questions related to:
- Human diseases and medical conditions
- Symptoms and their causes
- Medications, dosages, and drug interactions
- Preventive healthcare and lifestyle advice
- Medical tests and diagnoses
- First aid and emergency guidance

If the user asks anything unrelated to health, symptoms, diseases, or medications, respond with exactly:
"I'm only able to answer questions related to health, symptoms, diseases, and medications. Please ask a health-related question and I'll be happy to help!"

Always format your response clearly using:
- **Bold** for important terms and key points
- Bullet points for lists
- Clear section headings where needed

End every response with a note:
"⚠️ This is general health information only. Always consult a qualified doctor for personal medical advice."

Keep responses clear, accurate, and easy for non-medical users to understand."""
                    },
                    {
                        "role": "user",
                        "content": question.strip()
                    }
                ],
                temperature=0.4,
                max_tokens=1024
            )
            answer = response.choices[0].message.content
            loading_slot.empty()

            # Render answer header
            st.markdown("""
            <div class='answer-box' style='margin-bottom: 0.5rem;'>
                <div style='display: flex; align-items: center; gap: 0.6rem;
                            padding-bottom: 0.8rem; border-bottom: 1px solid #E2E8F0;'>
                    <div style='width: 38px; height: 38px; border-radius: 10px;
                                background: linear-gradient(135deg, #0D9488, #5EEAD4);
                                display: flex; align-items: center; justify-content: center;'>
                        <i class="fa-solid fa-robot" style="color: white;
                           font-size: 1rem;"></i>
                    </div>
                    <div>
                        <div style='font-weight: 700; color: #0F172A;
                                    font-size: 0.95rem;'>Health Assistant</div>
                        <div style='color: #94A3B8; font-size: 0.92rem;'>
                            Powered by Llama 3.1 via Groq</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Render answer using Streamlit native markdown
            st.markdown(answer)

        except Exception as e:
            loading_slot.empty()
            error_msg = str(e)
            if "invalid_api_key" in error_msg.lower() or "401" in error_msg:
                st.error("Invalid API key. Please check your Groq API key in secrets.toml")
            elif "rate_limit" in error_msg.lower() or "429" in error_msg:
                st.warning("Too many requests. Please wait 30 seconds and try again.")
            else:
                st.error(f"Something went wrong: {error_msg}")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='color: #94A3B8; font-size: 0.92rem; text-align: center;
    padding-top: 0.8rem; border-top: 1px solid #E2E8F0;'>
    ⚠️ MediScan Health Assistant provides general health information only.
    Always consult a qualified doctor for diagnosis and treatment.
</div>
""", unsafe_allow_html=True)
