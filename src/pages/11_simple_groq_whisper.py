# 11_simple_groq_whisper.
import tempfile

import streamlit as st
import requests
from st_audiorec import st_audiorec

from components.sidebar_key_and_model import sidebar_key_and_model
from components.language_selector import language_selector
from functions.transcribe_audio import transcribe_audio


def record_audio_file(audio_bytes):
    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".wav"
    ) as temp_audio:
        temp_audio.write(audio_bytes)
        return temp_audio.name


def download_audio(url):
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav"
        ) as temp_audio:
            temp_audio.write(response.content)
            return temp_audio.name
    else:
        st.error("Fail to download file form URL.")
        return None


# ウィジェットを操作したときのコールバック関数
def on_change_clear_state():
    if "transcript" in st.session_state:
        st.session_state.transcript = ""


def groq_whisper():
    st.title("Simple Groq Whisper App")
    st.markdown(
        "The application uses Grop's `whisper-large-v3` to transcribe audio."
    )

    sidebar_key_and_model()

    input_method = st.radio(
        label="Please select audio input method.",
        options=["File-Upload", "Microphone-Record", "Specify-URL"],
        on_change=on_change_clear_state,
    )

    output_language = language_selector()
    prompt = f"Specify context or spelling in {output_language.language}."
    lang = output_language.lang_code
    st.markdown(f"Transcribe Prompt: **{prompt}**")

    if input_method == "File-Upload":
        uploaded_file = st.file_uploader(
            "Upload audio file.",
            type=["wav", "mp3", "m4a"],
        )
        if uploaded_file is not None:
            st.audio(uploaded_file)
            if st.button("Start transcription."):
                transcript = transcribe_audio(uploaded_file, prompt, lang)
                if transcript != "":
                    st.write(transcript)
                    st.session_state.transcript = transcript

    elif input_method == "Microphone-Record":
        st.session_state.wav_audio_data = st_audiorec()

        if st.session_state.wav_audio_data is not None:
            # st.audio(st.session_state.wav_audio_data, format="audio/wav")
            if st.button("Start transcription."):
                wav_file = record_audio_file(st.session_state.wav_audio_data)
                transcript = ""
                with open(wav_file, "rb") as wave_data:
                    transcript = transcribe_audio(wave_data, prompt, lang)
                    if transcript != "":
                        st.write(transcript)
                        st.session_state.transcript = transcript

    elif input_method == "Specify-URL":
        url = st.text_input(
            label="Please enter the URL of the audio file (wav file).",
            placeholder="input URL of wave file",
        )
        if url:
            download_file = download_audio(url)
            with open(download_file, "rb") as audio_file:
                st.audio(audio_file)
                if st.button("Start transcription."):
                    transcript = transcribe_audio(audio_file, prompt, lang)
                    if transcript != "":
                        st.write(transcript)
                        st.session_state.transcript = transcript


groq_whisper()
