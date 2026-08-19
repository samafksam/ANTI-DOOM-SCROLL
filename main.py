import streamlit as st
import time

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="JEE Prep Flow - PYQ Engine",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #e6edf3;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff8c00 100%);
        color: #ffffff;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 8px 20px;
    }
    .stat-box {
        background-color: #161b22;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        border: 1px solid #30363d;
    }
    .solution-box {
        background-color: #1c2128;
        border-left: 4px solid #2ea043;
        padding: 15px;
        border-radius: 6px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# STATE MANAGEMENT
# ==========================================
if "jee_score" not in st.session_state:
    st.session_state.jee_score = 0
if "attempted" not in st.session_state:
    st.session_state.attempted = 0

# ==========================================
# HEADER & DASHBOARD
# ==========================================
st.title("🎯 JEE Main & Advanced PYQ Engine")
st.caption("Master Previous Year Questions with Step-by-Step Interactive Solutions")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='stat-box'>📊 <b>Attempted</b><br><h3>{st.session_state.attempted}</h3></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='stat-box'>⚡ <b>Accuracy Score</b><br><h3>{st.session_state.jee_score} pts</h3></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='stat-box'>🎯 <b>Target</b><br><h3>JEE 2026/2027</h3></div>", unsafe_allow_html=True)

st.divider()

# ==========================================
# QUESTION DATABASE
# ==========================================
pyqs = [
    {
        "id": 1,
        "exam": "JEE Main (Physics)",
        "year": "2023",
        "topic": "Electrostatics",
        "question": "Two point charges $q_1 = +2\\,\\mu\\text{C}$ and $q_2 = -2\\,\\mu\\text{C}$ are placed at a distance $r = 3\\,\\text{cm}$ apart in vacuum. What is the magnitude of the electrostatic force between them?",
        "options": ["20 N", "40 N", "80 N", "160 N"],
        "answer": "40 N",
        "solution": """
        **Formula:** Coulomb's Law $F = k \\frac{|q_1 q_2|}{r^2}$
        
        **Given:**
        - $k = 9 \\times 10^9 \\,\\text{N}\\cdot\\text{m}^2/\\text{C}^2$
        - $q_1 = 2 \\times 10^{-6} \\,\\text{C}$, $q_2 = 2 \\times 10^{-6} \\,\\text{C}$
        - $r = 3 \\times 10^{-2} \\,\\text{m}$
        
        **Calculation:**
        $$F = \\frac{(9 \\times 10^9) \\times (2 \\times 10^{-6}) \\times (2 \\times 10^{-6})}{(3 \\times 10^{-2})^2} = \\frac{36 \\times 10^{-3}}{9 \\times 10^{-4}} = 40\\,\\text{N}$$
        """
    },
    {
        "id": 2,
        "exam": "JEE Advanced (Mathematics)",
        "year": "2022",
        "topic": "Calculus - Definite Integrals",
        "question": "Evaluate the integral: $I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(x)}{\\sin^n(x) + \\cos^n(x)} \\, dx$",
        "options": ["$\\pi/4$", "$\\pi/2$", "0", "1"],
        "answer": "$\\pi/4$",
        "solution": """
        **Using King's Property:** $\\int_{a}^{b} f(x)dx = \\int_{a}^{b} f(a+b-x)dx$
        
        1. $I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(x)}{\\sin^n(x) + \\cos^n(x)} dx$  --- (Equation 1)
        2. Replace $x \\to \\pi/2 - x$:  
           $I = \\int_{0}^{\\pi/2} \\frac{\\cos^n(x)}{\\cos^n(x) + \\sin^n(x)} dx$  --- (Equation 2)
        3. Adding (1) and (2):  
           $2I = \\int_{0}^{\\pi/2} 1 \\, dx = [x]_0^{\\pi/2} = \\frac{\\pi}{2}$
        4. $I = \\frac{\\pi}{4}$
        """
    },
    {
        "id": 3,
        "exam": "JEE Main (Chemistry)",
        "year": "2024",
        "topic": "Organic Chemistry - Coordination Compounds",
        "question": "Which of the following complex ions is paramagnetic?",
        "options": ["$[Ni(CN)_4]^{2-}$", "$[Fe(CN)_6]^{4-}$", "$[Fe(H_2O)_6]^{3+}$", "$[Zn(NH_3)_4]^{2+}$"],
        "answer": "$[Fe(H_2O)_6]^{3+}$",
        "solution": """
        - $\\text{CN}^-$ is a strong field ligand (pairs up electrons $\\to$ diamagnetic).
        - $\\text{H}_2\\text{O}$ is a weak field ligand.
        - $\\text{Fe}^{3+}$ has $d^5$ configuration. With weak field ligand $\\text{H}_2\\text{O}$, it remains high-spin with 5 unpaired electrons ($t_{2g}^3 e_g^2$), making it **paramagnetic**.
        """
    }
]

# ==========================================
# FILTER & TABS
# ==========================================
filter_exam = st.selectbox("Filter Subject / Level:", ["All PYQs", "JEE Main (Physics)", "JEE Advanced (Mathematics)", "JEE Main (Chemistry)"])

for q in pyqs:
    if filter_exam != "All PYQs" and q["exam"] != filter_exam:
        continue

    with st.container():
        st.subheader(f"📌 {q['exam']} — {q['year']}")
        st.caption(f"Topic: **{q['topic']}**")
        st.markdown(q["question"])

        user_choice = st.radio(
            "Select Option:",
            q["options"],
            key=f"q_{q['id']}"
        )

        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            if st.button("Check Answer", key=f"btn_{q['id']}"):
                st.session_state.attempted += 1
                if user_choice == q["answer"]:
                    st.success("🎉 Correct Answer! (+10 pts)")
                    st.session_state.jee_score += 10
                else:
                    st.error(f"❌ Incorrect. The right answer is **{q['answer']}**.")

        with st.expander("📖 View Step-by-Step Solution"):
            st.markdown(q["solution"])
        
        st.divider()
