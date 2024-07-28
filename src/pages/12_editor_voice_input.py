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


def update_transcript():
    st.session_state.transcript_shown = st.session_state.transcript


@st.dialog("Transprit from Microphone Record")
def editor_voice_input():
    output_language = language_selector()
    prompt = f"Specify context or spelling in {output_language.language}."
    lang = output_language.lang_code
    st.markdown(f"Transcribe Prompt: **{prompt}**")

    # マイク録音
    st.session_state.wav_audio_data = st_audiorec()

    if st.session_state.wav_audio_data is not None:
        if st.button("Start transcription."):
            st.session_state.transcript = ""
            wav_file = record_audio_file(st.session_state.wav_audio_data)
            transcript = ""
            with open(wav_file, "rb") as wave_data:
                transcript = transcribe_audio(wave_data, prompt, lang)
                if transcript != "":
                    st.session_state.transcript = transcript
            st.write(st.session_state.transcript)

        if st.button("Apply to Transcript"):
            update_transcript()
            st.rerun()


def edit_transcript():
    # edit transcript
    with st.expander(label="Edit transcript", icon="🖌️"):
        edited_transcript = st.text_area(
            "Ctrl + Enter (x2) to apply transcript",
            value=st.session_state.transcript,
            on_change=update_transcript,
            key="transcript_editor",
        )
        st.session_state.transcript = edited_transcript
        if st.button("Apply to Transcript"):
            update_transcript()
            st.write("click twice to apply to transcript.")


# main procedure
st.title("Editing Voice Input App")
st.markdown("Editing and correcting a voice input.")

# セッション状態の初期化
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "transcript_shown" not in st.session_state:
    st.session_state.transcript_shown = ""

sidebar_key_and_model()

st.subheader("Microphone-Record")
if st.button("Record audio?"):
    editor_voice_input()

# show transcript
st.subheader("Transcript:")
if st.session_state.transcript_shown != "":
    shown_transcript = f"""{st.session_state.transcript_shown}"""
    st.code(shown_transcript, language="python")

# modify transcript
edit_transcript()
