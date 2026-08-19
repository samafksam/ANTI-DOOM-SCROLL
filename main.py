import streamlit as st
import time
import random

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="DopeFlow - Micro-Learning Engine",
    page_icon="⚡",
    layout="centered"
)

# Custom Gen-Z Neon Dark Mode CSS
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #000000;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px rgba(0, 242, 254, 0.6);
    }
    .badge-card {
        background: rgba(22, 27, 34, 0.8);
        border: 2px solid #00f2fe;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.2);
    }
    .stat-box {
        background-color: #161b22;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# STATE MANAGEMENT
# ==========================================
if "xp" not in st.session_state:
    st.session_state.xp = 1420
if "streak" not in st.session_state:
    st.session_state.streak = 7
if "vibe_check_active" not in st.session_state:
    st.session_state.vibe_check_active = False

# ==========================================
# HEADER & DASHBOARD METRICS
# ==========================================
st.title("⚡ DopeFlow")
st.caption("Ditch Doomscrolling. Master Micro-Skills in 60 Seconds.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='stat-box'>🔥 <b>Streak</b><br><h3>{st.session_state.streak} Days</h3></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='stat-box'>⚡ <b>Skill XP</b><br><h3>{st.session_state.xp} XP</h3></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='stat-box'>🏆 <b>Rank</b><br><h3>Byte Hustler</h3></div>", unsafe_allow_html=True)

st.divider()

# ==========================================
# VIBE CHECK TRIGGER BUTTON
# ==========================================
if st.button("🚨 Simulate Social App Interruption (Vibe Check)"):
    st.session_state.vibe_check_active = True

# ==========================================
# OVERRIDE UI IF VIBE CHECK IS ACTIVE
# ==========================================
if st.session_state.vibe_check_active:
    st.warning("⚠️ **VIBE CHECK ACTIVATED!** You tried to open TikTok/Instagram. Clear this 60-second challenge to unlock your brain!")
    
    st.subheader("🎯 60-Second Rapid Challenge")
    st.write("Which flexbox CSS property centers items along the main axis?")
    
    choice = st.radio("Select the correct CSS line:", [
        "align-items: center;",
        "justify-content: center;",
        "text-align: center;",
        "float: center;"
    ])
    
    if st.button("Submit Vibe Check Solution"):
        if choice == "justify-content: center;":
            st.success("🔥 BOOM! Correct! +50 XP. Dopamine restored cleanly.")
            st.session_state.xp += 50
            st.session_state.vibe_check_active = False
            st.balloons()
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("❌ Not quite. Try again!")

else:
    # ==========================================
    # MAIN APP TABS
    # ==========================================
    tab_feed, tab_badge = st.tabs(["📱 Interactive Feed", "🏆 Proof-of-Skill Badge"])

    # ------------------------------------------
    # TAB 1: FEED LOOPS
    # ------------------------------------------
    with tab_feed:
        st.subheader("⚡ 60-Second Interactive Skill Feed")
        
        # Challenge 1: Code Fix
        with st.expander("💻 Challenge #1: React State Bug (Tap-to-Fix)", expanded=True):
            st.write("Identify the bug in this state updater:")
            st.code("const [count, setCount] = useState(0);\n// Incorrect increment:\nsetCount(count + 1);", language="javascript")
            
            option = st.selectbox(
                "How do you fix race conditions in state updates?",
                ["setCount(count + 1)", "setCount((prev) => prev + 1)", "count = count + 1"]
            )
            
            if st.button("Run Code & Test"):
                if option == "setCount((prev) => prev + 1)":
                    st.success("✅ Clean code! AI Evaluator: Correct use of functional state updater (+30 XP)")
                    st.session_state.xp += 30
                else:
                    st.error("❌ Bug detected! Relying on current state in async calls leads to stale state errors.")

        # Challenge 2: Voice Pronunciation
        with st.expander("🎙️ Challenge #2: Japanese Audio Check"):
            st.write("Target Phrase: **「こんにちは」 (Konnichiwa)**")
            
            audio_val = st.audio_input("Record your pronunciation")
            if audio_val:
                with st.spinner("AI Evaluating Pitch & Cadence..."):
                    time.sleep(1.5)
                    st.success("🎯 94% Pitch Match! Pitch contour matched native speakers (+20 XP)")

    # ------------------------------------------
    # TAB 2: PROOF-OF-SKILL BADGE
    # ------------------------------------------
    with tab_badge:
        st.subheader("🎨 Flex-Worthy Portfolio Card")
        st.caption("Ready to export and share directly to Instagram Stories or LinkedIn.")
        
        st.markdown(f"""
            <div class="badge-card">
                <h1 style="color: #00f2fe; margin-bottom: 0;">DopeFlow</h1>
                <p style="color: #8b949e;">OFFICIAL PROOF OF SKILL</p>
                <hr style="border-color: #30363d;">
                <h2>🏆 BYTE HUSTLER</h2>
                <p>Level 4 Skilled Creator</p>
                <p>🔥 <b>{st.session_state.streak} Day Streak</b> | ⚡ <b>{st.session_state.xp} Total XP</b></p>
                <p style="font-size: 0.8rem; color: #8b949e;">Verified by DopeFlow AI Engine</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("📋 Copy Portfolio Share Link"):
            st.toast("Link copied to clipboard! Ready to flex on Instagram/LinkedIn 🔥")
