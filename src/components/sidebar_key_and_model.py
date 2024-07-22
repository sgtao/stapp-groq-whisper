# sidebar_key_and_model.py
import os

import streamlit as st


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
