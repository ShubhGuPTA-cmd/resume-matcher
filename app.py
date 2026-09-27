import streamlit as st
from extract import extract_text_from_pdf, clean_text
from matcher import compute_similarity, find_missing_skills

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Overall background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%);
    }

    /* Main title */
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Card container */
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        margin-bottom: 1.5rem;
    }

    /* Score circle */
    .score-box {
        text-align: center;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    .score-number {
        font-size: 3.2rem;
        font-weight: 800;
        margin: 0;
    }
    .score-label {
        font-size: 0.95rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Skill pills */
    .pill {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        margin: 0.2rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .pill-have {
        background: #DCFCE7;
        color: #166534;
    }
    .pill-missing {
        background: #FEE2E2;
        color: #991B1B;
    }

    /* Streamlit default button restyle */
    div.stButton > button {
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">📄 Resume Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">See how well your resume matches a job description — instantly.</div>', unsafe_allow_html=True)

# ---------- INPUT CARD ----------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📎 Your Resume**")
        uploaded_resume = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    with col2:
        st.markdown("**💼 Job Description**")
        jd_text_input = st.text_area("Paste JD", height=180, label_visibility="collapsed",
                                       placeholder="Paste the job description here...")
    check = st.button("✨ Check My Match")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RESULTS ----------
if check:
    if not uploaded_resume or not jd_text_input.strip():
        st.warning("Please upload a resume and paste a job description first.")
    else:
        with st.spinner("Analyzing your resume against the job description..."):
            with open("temp_resume.pdf", "wb") as f:
                f.write(uploaded_resume.read())

            resume_text = extract_text_from_pdf("temp_resume.pdf")
            jd_text = clean_text(jd_text_input)

            score = compute_similarity(resume_text, jd_text)
            jd_skills, missing_skills = find_missing_skills(resume_text, jd_text)
            have_skills = [s for s in jd_skills if s not in missing_skills]

        # Color logic
        if score >= 75:
            color, verdict = "#16A34A", "Strong Match 🎉"
        elif score >= 50:
            color, verdict = "#D97706", "Moderate Match — Room to Improve"
        else:
            color, verdict = "#DC2626", "Low Match — Needs Tailoring"

        st.markdown(f"""
        <div class="score-box" style="background:{color}15;">
            <p class="score-number" style="color:{color};">{score}%</p>
            <p class="score-label">{verdict}</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(int(score), 100))

        # Skills card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**✅ Skills you already have**")
        if have_skills:
            pills = "".join([f'<span class="pill pill-have">{s}</span>' for s in have_skills])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.caption("No tracked skills matched yet.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**⚠️ Skills missing from your resume**")
        if missing_skills:
            pills = "".join([f'<span class="pill pill-missing">{s}</span>' for s in missing_skills])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.caption("Nothing missing — great coverage!")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<p style="text-align:center; color:#9CA3AF; font-size:0.8rem; margin-top:2rem;">Built with sentence-transformers + Streamlit</p>',
    unsafe_allow_html=True
) 