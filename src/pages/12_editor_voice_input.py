# 12_editor_voice_input.py
import tempfile

import streamlit as st
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


def editor_voice_input():
    st.title("Edittin Voice Input App")
    st.markdown("Editing and correcting a voice input.")

    sidebar_key_and_model()

    output_language = language_selector()
    prompt = f"Specify context or spelling in {output_language.language}."
    lang = output_language.lang_code
    st.markdown(f"Transcribe Prompt: **{prompt}**")

    # Microphone-Record:
    st.subheader("Microphone-Record")
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


editor_voice_input()
