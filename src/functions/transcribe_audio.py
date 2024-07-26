# transcribe_audio.py
from groq import Groq
import streamlit as st


def transcribe_audio(audio_data, prompt="", lang="en"):
    if audio_data is None:
        st.error("cannot find audio data")
        return

    if prompt == "":
        transcript_prompt = "Specify context or spelling"
    else:
        transcript_prompt = prompt

    try:
        client = Groq(api_key=st.session_state.groq_api_key)

        transcription = client.audio.transcriptions.create(
            file=audio_data,
            model="whisper-large-v3",
            prompt=transcript_prompt,  # Optional
            response_format="json",  # Optional
            language=lang,  # Optional
            temperature=0.0,  # Optional
        )
        # print(transcription.text)
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
