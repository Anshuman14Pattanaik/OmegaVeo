# main.py
import streamlit as st
from core import answer_query  # your logic file

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="OmegaVeo",
    page_icon="logo.png",
    layout="wide",
)

# ----------------- CUSTOM STYLING -----------------
custom_css = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: radial-gradient(circle at top, #10131b 0, #05060a 55%);
        color: #f5f5f5;
    }

    /* Make sidebar dark and NARROWER */
    [data-testid="stSidebar"] > div:first-child {
        background-color: #05060a;
        color: #f5f5f5;
    }

    /* Sidebar width (adjust these numbers if you want even narrower/wider) */
    [data-testid="stSidebar"] {
        width: 210px !important;
        min-width: 210px !important;
        max-width: 210px !important;
        border-right: 1px solid #27293a;
    }

    /* Hide the sidebar collapse/expand arrow so it feels permanent */
    [data-testid="collapsedControl"] {
        display: none;
    }

    .omega-main {
        max-width: 900px;
        margin: 0 auto;
        padding-top: 8vh;
        padding-bottom: 4vh;
    }

    .omega-hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e5e9ff;
        margin-left: 0.4rem;
    }

    .omega-hero-subtitle {
        font-size: 0.95rem;
        color: #9ca3c7;
        margin-top: 0.4rem;
        text-align: center;
    }

    /* ... keep the rest of your CSS here (omega-search-card, omega-send-btn, etc.) ... */
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------- STATE / RESET -----------------
def reset_chat():
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

messages = st.session_state.messages

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.markdown("### OmegaVeo")
    st.caption("Gemini‑powered assistant")

    st.markdown("#### ✏️ New Chat")
    if st.button("Start", use_container_width=True, key="sidebar_new_chat"):
        reset_chat()
        st.rerun()

    st.markdown("---")
    st.caption("Try: `What is the weather in Bhubaneswar?`")

# ----------------- MAIN AREA -----------------
st.markdown('<div class="omega-main">', unsafe_allow_html=True)

# ---------- STATE 1: NO MESSAGES YET ----------
if len(messages) == 0:
    hero_col1, hero_col2, hero_col3 = st.columns([1, 2, 1])
    with hero_col2:
        top_cols = st.columns([0.2, 1.8])
        with top_cols[0]:
            st.image("logo.png", width=48)
        with top_cols[1]:
            st.markdown(
                '<div class="omega-hero-title">How can I help you today?</div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            '<div class="omega-hero-subtitle">'
            'Message OmegaVeo with any question, or ask about the weather in a city.'
            '</div>',
            unsafe_allow_html=True,
        )

        # DeepSeek‑style search card for the FIRST question
        st.markdown('<div class="omega-search-card">', unsafe_allow_html=True)
        with st.form("first_query_form", clear_on_submit=True):
            first_query = st.text_input(
                "",
                "",
                placeholder="Message OmegaVeo",
                label_visibility="collapsed",
            )
            cols = st.columns([8, 1])
            with cols[1]:
                st.markdown('<div class="omega-send-btn">', unsafe_allow_html=True)
                submitted_first = st.form_submit_button("➤")
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted_first and first_query.strip():
        q = first_query.strip()
        messages.append({"role": "user", "content": q})
        answer = answer_query(q)
        messages.append({"role": "assistant", "content": answer})
        st.session_state.messages = messages
        st.rerun()

# ---------- STATE 2: AFTER FIRST MESSAGE ----------
else:
    st.markdown("### New chat")
    st.write("")

    # Show full chat history
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Bottom DeepSeek‑style input (for follow‑up questions)
    st.markdown('<div class="omega-search-card">', unsafe_allow_html=True)
    with st.form("followup_form", clear_on_submit=True):
        follow_query = st.text_input(
            "",
            "",
            placeholder="Message OmegaVeo",
            label_visibility="collapsed",
        )
        cols = st.columns([8, 1])
        with cols[1]:
            st.markdown('<div class="omega-send-btn">', unsafe_allow_html=True)
            submitted_follow = st.form_submit_button("➤")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted_follow and follow_query.strip():
        q = follow_query.strip()
        messages.append({"role": "user", "content": q})
        answer = answer_query(q)
        messages.append({"role": "assistant", "content": answer})
        st.session_state.messages = messages
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
