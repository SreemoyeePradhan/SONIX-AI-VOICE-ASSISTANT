import streamlit as st
from main import ask_gemini, speak, listen, log_interaction

st.set_page_config(page_title="Gemini Voice Assistant", layout="centered")

# ✅ Fix the white text by styling it to black
st.markdown("""
    <style>
    .user-avatar, .bot-avatar {
        float: left;
        margin-right: 10px;
        color: black; /* <-- Black text */
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Sonix: Your Personal AI Voice Assistant 📢")

# ✅ Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message or press '🎤 Speak' to say something:")
    col1, col2 = st.columns([1, 1])
    with col1:
        submit = st.form_submit_button("Send")
    with col2:
        voice_input = st.form_submit_button("🎤 Speak")

# ✅ Voice input
if voice_input:
    user_input = listen()

# ✅ Process input
if user_input and (submit or voice_input):
    st.session_state.chat_history.append(f"User: {user_input}")
    response = ask_gemini(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append(f"Gemini: {response}")
    st.session_state.last_response = response  # Store latest Gemini response
    log_interaction(user_input, response)

# ✅ Speak the response only if it hasn't been spoken yet
if st.session_state.last_response:
    speak(st.session_state.last_response)
    st.session_state.last_response = ""  # Prevent re-speaking on rerun

# ✅ Display chat history with styled output
for line in st.session_state.chat_history:
    if line.startswith("User:"):
        st.markdown(f"""
        <div class='user-avatar'>
            👤 <strong>User:</strong> {line[6:]}
        </div><br><br>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='bot-avatar'>
            🤖 <strong>Gemini:</strong> {line[8:]}
        </div><br><br>""", unsafe_allow_html=True)
