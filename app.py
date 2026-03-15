import streamlit as st
from utils import get_ai_response, text_to_speech, speech_to_text
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="VoxAI", page_icon="🤖")

st.title("VoxAI 🤖 Voice Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------- CHAT HISTORY --------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------- TEXT INPUT --------
text_prompt = st.chat_input("Type your question")

# -------- VOICE INPUT --------
audio = mic_recorder(
    start_prompt="🎤 Start recording",
    stop_prompt="⏹ Stop recording",
    key="mic"
)

prompt = None

# -------- HANDLE VOICE --------
if audio:

    st.audio(audio["bytes"])

    with st.spinner("Listening..."):
        spoken_text = speech_to_text(audio["bytes"])

    if spoken_text is None or spoken_text.startswith("Sorry"):
        st.error("Could not understand audio")
        prompt = None
    else:
        prompt = spoken_text
        st.write("You said:", prompt)

# -------- HANDLE TEXT --------
if text_prompt:
    prompt = text_prompt

# -------- AI PROCESS --------
if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("AI thinking..."):
        response = get_ai_response(st.session_state.messages)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    # -------- TEXT → VOICE --------
    audio_file = text_to_speech(response)

    if audio_file:
        st.audio(audio_file, format="audio/mp3")
    else:
        st.warning("Voice output unavailable")