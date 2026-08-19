import streamlit as st
import time

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="JEE CBT Mock Test Portal",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM NTA CBT EXAM STYLING (CSS)
# ==========================================
st.markdown("""
    <style>
    /* Dark Theme Exam Portal Styles */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* CBT Header Bar */
    .cbt-header {
        background-color: #1e293b;
        border-bottom: 2px solid #3b82f6;
        padding: 12px 20px;
        margin-bottom: 20px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Status Legends */
    .palette-legend {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        font-size: 12px;
        margin-bottom: 15px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .badge-icon {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        display: inline-block;
    }
    
    /* Question Box */
    .q-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }

    /* Score Summary Card */
    .score-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# QUESTION BANK (JEE MAIN & ADVANCED PYQs)
# ==========================================
QUESTIONS = [
    {
        "id": 1,
        "subject": "Physics",
        "exam": "JEE Main PYQ",
        "question": "Two point charges $q_1 = +2\\,\\mu\\text{C}$ and $q_2 = -2\\,\\mu\\text{C}$ are placed at a distance $r = 3\\,\\text{cm}$ apart in vacuum. What is the magnitude of the electrostatic force between them?",
        "options": ["20 N", "40 N", "80 N", "160 N"],
        "correct": 1,
        "solution": "Coulomb's Law: $F = k \\frac{|q_1 q_2|}{r^2} = \\frac{(9 \\times 10^9) \\times (2 \\times 10^{-6})^2}{(3 \\times 10^{-2})^2} = 40\\,\\text{N}$"
    },
    {
        "id": 2,
        "subject": "Mathematics",
        "exam": "JEE Advanced PYQ",
        "question": "Evaluate the definite integral: $$I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(x)}{\\sin^n(x) + \\cos^n(x)} \\, dx$$",
        "options": ["$\\pi/4$", "$\\pi/2$", "0", "1"],
        "correct": 0,
        "solution": "Using King's Property $\\int_{a}^{b} f(x)dx = \\int_{a}^{b} f(a+b-x)dx$, adding $I + I$ yields $2I = \\int_0^{\\pi/2} 1 \\, dx = \\pi/2 \\implies I = \\pi/4$."
    },
    {
        "id": 3,
        "subject": "Chemistry",
        "exam": "JEE Main PYQ",
        "question": "Which of the following complex ions is paramagnetic?",
        "options": ["$[Ni(CN)_4]^{2-}$", "$[Fe(CN)_6]^{4-}$", "$[Fe(H_2O)_6]^{3+}$", "$[Zn(NH_3)_4]^{2+}$"],
        "correct": 2,
        "solution": "$[Fe(H_2O)_6]^{3+}$ has $\\text{Fe}^{3+}$ ($d^5$ configuration). Since $\\text{H}_2\\text{O}$ is a weak field ligand, it forms a high-spin complex with 5 unpaired electrons, making it paramagnetic."
    },
    {
        "id": 4,
        "subject": "Physics",
        "exam": "JEE Advanced PYQ",
        "question": "A particle moves in a circle of radius $R$ with constant angular acceleration $\\alpha$. If the particle starts from rest, after what time $t$ will its tangential acceleration equal its radial acceleration?",
        "options": ["$t = 1/\\alpha$", "$t = 1/\\sqrt{\\alpha}$", "$t = \\sqrt{\\alpha}$", "$t = \\alpha$"],
        "correct": 1,
        "solution": "Tangential acceleration $a_t = \\alpha R$. Radial acceleration $a_r = \\omega^2 R = (\\alpha t)^2 R$. Setting $a_t = a_r \\implies \\alpha R = \\alpha^2 t^2 R \\implies t = 1/\\sqrt{\\alpha}$."
    },
    {
        "id": 5,
        "subject": "Chemistry",
        "exam": "JEE Main PYQ",
        "question": "The correct order of increasing first ionization enthalpy for $\\text{Li, Be, B, C}$ is:",
        "options": ["$\\text{Li} < \\text{B} < \\text{Be} < \\text{C}$", "$\\text{Li} < \\text{Be} < \\text{B} < \\text{C}$", "$\\text{B} < \\text{Li} < \\text{Be} < \\text{C}$", "$\\text{Li} < \\text{C} < \\text{B} < \\text{Be}$"],
        "correct": 0,
        "solution": "Beryllium ($1s^2 2s^2$) has a fully filled stable subshell, making its ionization enthalpy higher than Boron ($1s^2 2s^2 2p^1$). Order: $\\text{Li} < \\text{B} < \\text{Be} < \\text{C}$."
    }
]

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {i: None for i in range(len(QUESTIONS))}
if "q_status" not in st.session_state:
    # Statuses: "not_visited", "not_answered", "answered", "review"
    st.session_state.q_status = {i: "not_visited" for i in range(len(QUESTIONS))}
    st.session_state.q_status[0] = "not_answered"
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ==========================================
# HEADER: EXAM PORTAL BAR
# ==========================================
st.markdown("""
<div class="cbt-header">
    <div>
        <h3 style="margin:0; color:#3b82f6;">📝 NATIONAL TESTING AGENCY (SIMULATOR)</h3>
        <small style="color:#94a3b8;">JEE Main & Advanced Full-Length Mock Series</small>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SCREEN 1: SCORECARD (AFTER SUBMISSION)
# ==========================================
if st.session_state.submitted:
    st.balloons()
    st.header("📊 Test Performance Analysis")
    
    # Calculate Scores (+4 for correct, -1 for wrong, 0 for unattempted)
    correct_cnt = 0
    wrong_cnt = 0
    unattempted_cnt = 0
    total_marks = 0

    for i, q in enumerate(QUESTIONS):
        ans = st.session_state.user_answers[i]
        if ans is None:
            unattempted_cnt += 1
        elif ans == q["correct"]:
            correct_cnt += 1
            total_marks += 4
        else:
            wrong_cnt += 1
            total_marks -= 1

    max_marks = len(QUESTIONS) * 4
    accuracy = (correct_cnt / (correct_cnt + wrong_cnt) * 100) if (correct_cnt + wrong_cnt) > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Score", f"{total_marks} / {max_marks}")
    with col2:
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col3:
        st.metric("Correct Answers", f"{correct_cnt} (+{correct_cnt*4})")
    with col4:
        st.metric("Incorrect Answers", f"{wrong_cnt} (-{wrong_cnt})")

    st.divider()
    st.subheader("📖 Detailed Solutions & Question Breakdown")

    for i, q in enumerate(QUESTIONS):
        user_ans = st.session_state.user_answers[i]
        is_correct = user_ans == q["correct"]
        
        status_label = "⭕ Unattempted"
        status_color = "gray"
        if user_ans is not None:
            if is_correct:
                status_label = "✅ Correct (+4)"
                status_color = "green"
            else:
                status_label = "❌ Incorrect (-1)"
                status_color = "red"

        with st.expander(f"Q{i+1} [{q['subject']}] - {status_label}"):
            st.markdown(f"**Question:** {q['question']}")
            
            for idx, opt in enumerate(q["options"]):
                prefix = ""
                if idx == q["correct"]:
                    prefix = "✔️ **(Correct Answer)** "
                if user_ans == idx and not is_correct:
                    prefix = "❌ **(Your Answer)** "
                st.write(f"- {prefix}{opt}")
            
            st.markdown(f"<div style='background-color:#0f172a; padding:10px; border-radius:6px; border-left: 3px solid #3b82f6;'><b>Solution:</b><br>{q['solution']}</div>", unsafe_allow_html=True)

    if st.button("🔄 Retake Mock Test"):
        st.session_state.current_q = 0
        st.session_state.user_answers = {i: None for i in range(len(QUESTIONS))}
        st.session_state.q_status = {i: "not_visited" for i in range(len(QUESTIONS))}
        st.session_state.q_status[0] = "not_answered"
        st.session_state.submitted = False
        st.rerun()

# ==========================================
# SCREEN 2: ACTIVE CBT EXAM PORTAL
# ==========================================
else:
    # Layout: Left side (Question View), Right side (Palette + Timer)
    left_col, right_col = st.columns([3, 1])

    # ------------------------------------------
    # RIGHT SIDEBAR: TIMER & PALETTE
    # ------------------------------------------
    with right_col:
        st.markdown("### ⏱️ Time Remaining")
        # Simulate 180 min timer
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 180*60 - elapsed)
        mins, secs = divmod(remaining, 60)
        st.markdown(f"<h2 style='color:#f59e0b; margin:0;'>{mins:02d}:{secs:02d}</h2>", unsafe_allow_html=True)
        st.caption("Standard Marking Scheme: **+4 / -1**")

        st.divider()
        st.markdown("### 🎨 Question Palette")
        
        # Legend
        st.markdown("""
            <div class="palette-legend">
                <div class="legend-item"><span class="badge-icon" style="background:#22c55e;"></span> Answered</div>
                <div class="legend-item"><span class="badge-icon" style="background:#ef4444;"></span> Not Answered</div>
                <div class="legend-item"><span class="badge-icon" style="background:#a855f7;"></span> Review</div>
                <div class="legend-item"><span class="badge-icon" style="background:#475569;"></span> Not Visited</div>
            </div>
        """, unsafe_allow_html=True)

        # Grid Buttons for Question Numbers
        grid_cols = st.columns(4)
        for i in range(len(QUESTIONS)):
            col = grid_cols[i % 4]
            status = st.session_state.q_status[i]
            
            # Button Emoji indicator
            label_icon = str(i + 1)
            if status == "answered":
                label_icon = f"🟩 {i+1}"
            elif status == "not_answered":
                label_icon = f"🟥 {i+1}"
            elif status == "review":
                label_icon = f"🟪 {i+1}"
            else:
                label_icon = f"⬜ {i+1}"

            if col.button(label_icon, key=f"nav_btn_{i}", use_container_width=True):
                st.session_state.current_q = i
                if st.session_state.q_status[i] == "not_visited":
                    st.session_state.q_status[i] = "not_answered"
                st.rerun()

        st.divider()
        if st.button("🚀 SUBMIT TEST", type="primary", use_container_width=True):
            st.session_state.submitted = True
            st.rerun()

    # ------------------------------------------
    # LEFT PANEL: QUESTION VIEW & CONTROLS
    # ------------------------------------------
    with left_col:
        q_idx = st.session_state.current_q
        q_data = QUESTIONS[q_idx]

        st.markdown(f"#### **Question No. {q_idx + 1}** — <span style='color:#3b82f6;'>{q_data['subject']}</span> ({q_data['exam']})", unsafe_allow_html=True)
        
        st.markdown(f"<div class='q-box'>{q_data['question']}</div>", unsafe_allow_html=True)

        # Radio button selection
        current_selection = st.session_state.user_answers[q_idx]
        selected_option = st.radio(
            "Select Your Option:",
            options=range(len(q_data["options"])),
            format_func=lambda x: q_data["options"][x],
            index=current_selection if current_selection is not None else None,
            key=f"radio_q_{q_idx}"
        )

        st.write("")
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

        # Button 1: Save & Next
        with col_btn1:
            if st.button("💾 Save & Next", type="primary", use_container_width=True):
                if selected_option is not None:
                    st.session_state.user_answers[q_idx] = selected_option
                    st.session_state.q_status[q_idx] = "answered"
                else:
                    st.session_state.q_status[q_idx] = "not_answered"

                if q_idx < len(QUESTIONS) - 1:
                    st.session_state.current_q += 1
                    if st.session_state.q_status[st.session_state.current_q] == "not_visited":
                        st.session_state.q_status[st.session_state.current_q] = "not_answered"
                st.rerun()

        # Button 2: Mark for Review
        with col_btn2:
            if st.button("🟪 Mark for Review", use_container_width=True):
                if selected_option is not None:
                    st.session_state.user_answers[q_idx] = selected_option
                st.session_state.q_status[q_idx] = "review"
                if q_idx < len(QUESTIONS) - 1:
                    st.session_state.current_q += 1
                st.rerun()

        # Button 3: Clear Response
        with col_btn3:
            if st.button("🧹 Clear Response", use_container_width=True):
                st.session_state.user_answers[q_idx] = None
                st.session_state.q_status[q_idx] = "not_answered"
                st.rerun()

        # Button 4: Previous
        with col_btn4:
            if st.button("⬅️ Previous", use_container_width=True):
                if q_idx > 0:
                    st.session_state.current_q -= 1
                    st.rerun()
