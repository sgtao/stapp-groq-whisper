# a11_groq_whisper.py
import os
import tempfile

import streamlit as st
from groq import Groq
import requests
from st_audiorec import st_audiorec


class ModelSelector:
    """Class for selecting the Groq model"""

    def __init__(self):
        """Define the available models"""
        self.models = ["llama3-8b-8192", "llama3-70b-8192"]

    def select(self):
        """
        Display the model selection form in the sidebar
        Returns:
            st.selectbox of Models
        """
        with st.sidebar:
            st.sidebar.title("Chat Model")
            return st.selectbox(
                "Select a model:", self.models, label_visibility="collapsed"
            )


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


def sidebar_key_and_model():
    """
    Sidebar with API-KEY input and Model selector
    """
    # API-KEYのプリセット確認
    if "groq_api_key" in st.session_state:
        groq_api_key = st.session_state.groq_api_key
    elif os.getenv("GROQ_API_KEY"):
        st.session_state.groq_api_key = os.getenv("GROQ_API_KEY")
        groq_api_key = st.session_state.groq_api_key
    else:
        groq_api_key = ""

    if "selected_model" in st.session_state:
        groq_api_key = st.session_state.groq_api_key
    else:
        st.session_state.selected_model = "llama3-70b-8192"

    with st.sidebar:
        # API-KEYの設定
        st.session_state.groq_api_key = st.text_input(
            "Groq API Key",
            key="api_key",
            type="password",
            placeholder="gsk_...",
            value=groq_api_key,
        )
        groq_api_key = st.session_state.groq_api_key
        "[Get an Groq API key](https://console.groq.com/keys)"

        # Select the model
        model = ModelSelector()
        st.session_state.selected_model = model.select()


def transcribe_audio(audio_file):
    try:
        client = Groq(api_key=st.session_state.groq_api_key)

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0,  # Optional
        )
        print(transcription.text)
        return transcription.text
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return ""


def transcribe_audio_with_prompt(audio_file, append_prompt=""):
    prompt = f"Specify context or spelling. {append_prompt}"
    print(f"Retry transcript with prompt:${prompt}")
  
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            prompt=prompt,
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0,  # Optional
        )
        print(transcription.text)
        return transcription.text
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return ""

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
                    wav_file = record_audio_file(st.session_state.wav_audio_data)
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
