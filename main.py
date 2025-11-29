# app.py
import streamlit as st
from core import answer_query  # import your main logic

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="OmegaVeo",
    page_icon="logo.png",   # uses your logo
    layout="wide",
)

# ----------------- CUSTOM STYLING -----------------
custom_css = """
<style>
    /* Hide default Streamlit menu, header & footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: radial-gradient(circle at top, #10131b 0, #05060a 55%);
        color: #f5f5f5;
    }

    .omega-main {
        max-width: 900px;
        margin: 0 auto;
        padding-top: 8vh;
        padding-bottom: 4vh;
    }

    .omega-hero {
        text-align: center;
        margin-bottom: 2.5rem;
    }

    .omega-hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e5e9ff;
        margin-top: 0.75rem;
    }

    .omega-hero-subtitle {
        font-size: 0.95rem;
        color: #9ca3c7;
        margin-top: 0.4rem;
    }

    .omega-card {
        background: #14151b;
        border-radius: 24px;
        padding: 1.2rem 1.4rem;
        border: 1px solid #27293a;
        box-shadow: 0 0 30px rgba(0,0,0,0.65);
    }

    /* Slightly style the chat input area */
    .stChatInput textarea {
        background-color: #14151b !important;
        color: #f5f5f5 !important;
        border-radius: 16px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ----------------- SIDEBAR (LEFT PANEL) -----------------
def reset_chat():
    st.session_state.messages = []

with st.sidebar:
    st.image("logo.png", use_column_width=True)
    st.markdown("### OmegaVeo")
    st.caption("Gemini‑powered assistant")
    st.button("＋ New chat", use_container_width=True, on_click=reset_chat)
    st.markdown("---")
    st.caption("Ask anything, or try a weather question:\n\n`What is the weather in Bhubaneswar?`")


# ----------------- CHAT STATE -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------- MAIN LAYOUT -----------------
st.markdown('<div class="omega-main">', unsafe_allow_html=True)

# Hero section (like “How can I help you?”) when chat is empty
if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="omega-hero">', unsafe_allow_html=True)
        st.image("logo.png", width=96)
        st.markdown(
            '<div class="omega-hero-title">How can I help you?</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="omega-hero-subtitle">'
            'Message OmegaVeo with any question, or ask about the weather in a city.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

# Chat history inside a card-like container
st.markdown('<div class="omega-card">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # close omega-main


# ----------------- CHAT INPUT -----------------
user_input = st.chat_input("Message OmegaVeo")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get answer from main.py logic
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = answer_query(user_input)
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

