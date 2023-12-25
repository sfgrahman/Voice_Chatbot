import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

float_init()

def initialize_session_state():
    if "message" not in st.session_state:
        st.session_state.messages=[ 
                                   {"role":"assistant", "content": "Hi! How may I assist you today?"}
                                   ]
        # if "audio_initialized" not in st.session_state:
        # st.session_state.audio_initialized = False

initialize_session_state()

st.title("Conversational Voice Chatbot")
st.markdown("""
<style>
.big-font {
    font-size:24px !important;
    color: #e8b62c;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Integrating OpenAI\'s Speech-to-Text & Text-to-Speech</p>', unsafe_allow_html=True)

st.sidebar.header("Enter OpenAI Key(**Not store anywhere**)")
os.environ['OPENAI_API_KEY'] = st.sidebar.text_input("Enter your openai keys", type="password")

footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder(recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="user",
    icon_size="4x") 


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
if audio_bytes:
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)
        
        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

footer_container.float("bottom: 0rem;")