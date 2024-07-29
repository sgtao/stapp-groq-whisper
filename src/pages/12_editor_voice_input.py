# 12_editor_voice_input.py
import streamlit as st

from components.sidebar_key_and_model import sidebar_key_and_model
from components.modal_voice_input import modal_voice_input


def update_transcript():
    st.session_state.transcript_shown = st.session_state.transcript


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
    modal_voice_input()

# show transcript
st.subheader("Transcript:")
if st.session_state.transcript_shown != "":
    shown_transcript = f"""{st.session_state.transcript_shown}"""
    st.code(shown_transcript, language="python")

# modify transcript
edit_transcript()
