# a11_groq_whisper.py
import tempfile

import streamlit as st
import requests
from st_audiorec import st_audiorec

from components.sidebar_key_and_model import sidebar_key_and_model
from functions.transcribe_audio import transcribe_audio
from functions.transcribe_audio import transcribe_audio_with_prompt


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
        st.error("URLからの音声ダウンロードに失敗しました。")
        return None


def groq_whisper():
    st.title("Simple Groq Whisper App")

    sidebar_key_and_model()

    input_method = st.radio(
        "入力方法を選択してください",
        ["ファイルアップロード", "マイク録音", "URL指定"],
    )

    if input_method == "ファイルアップロード":
        uploaded_file = st.file_uploader(
            "音声ファイルをアップロードしてください",
            type=["wav", "mp3", "m4a"],
        )
        if uploaded_file is not None:
            st.audio(uploaded_file)
            if st.button("文字起こしを開始"):
                transcript = transcribe_audio(uploaded_file)
                st.write(transcript)

    elif input_method == "マイク録音":
        st.session_state.wav_audio_data = st_audiorec()

        if st.session_state.wav_audio_data is not None:
            # st.audio(st.session_state.wav_audio_data, format="audio/wav")
            if st.button("文字起こしを開始"):
                wav_file = record_audio_file(st.session_state.wav_audio_data)
                transcript = ""
                with open(wav_file, "rb") as wave_data:
                    transcript = transcribe_audio(wave_data)
                    st.write(transcript)
                    if transcript != "":
                        st.session_state.transcript = transcript
            if "transcript" in st.session_state:
                if st.button("再トライ：文字起こし"):
                    wav_file = record_audio_file(
                        st.session_state.wav_audio_data
                    )
                    with open(wav_file, "rb") as wave_data:
                        transcript = transcribe_audio_with_prompt(
                            wave_data,
                            st.session_state.transcript,
                        )
                        st.write(transcript)

    elif input_method == "URL指定":
        url = st.text_input("音声ファイルのURLを入力してください")
        if url:
            download_file = download_audio(url)
            with open(download_file, "rb") as audio_file:
                st.audio(audio_file)
                if st.button("文字起こしを開始"):
                    transcript = transcribe_audio(audio_file)
                    st.write(transcript)


groq_whisper()
