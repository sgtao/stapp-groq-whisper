# selector_language.py
import streamlit as st


class LangSelector:
    """Class for selecting the Groq model"""

    def __init__(self):
        """Define the available languages"""
        self.langs = [
            "english",
            "chinese",
            "german",
            "spanish",
            "russian",
            "korean",
            "french",
            "japanese",
            "portuguese",
            "turkish",
            "polish",
            "catalan",
            "dutch",
            "arabic",
            "swedish",
            "italian",
            "indonesian",
            "hindi",
            "finnish",
            "vietnamese",
            "hebrew",
            "ukrainian",
            "greek",
            "malay",
            "czech",
            "romanian",
            "danish",
            "hungarian",
            "tamil",
            "norwegian",
            "thai",
            "urdu",
            "croatian",
            "bulgarian",
            "lithuanian",
            "latin",
            "maori",
            "malayalam",
            "welsh",
            "slovak",
            "telugu",
            "persian",
            "latvian",
            "bengali",
            "serbian",
            "azerbaijani",
            "slovenian",
            "kannada",
            "estonian",
            "macedonian",
            "breton",
            "basque",
            "icelandic",
            "armenian",
            "nepali",
            "mongolian",
            "bosnian",
            "kazakh",
            "albanian",
            "swahili",
            "galician",
            "marathi",
            "punjabi",
            "sinhala",
            "khmer",
            "shona",
            "yoruba",
            "somali",
            "afrikaans",
            "occitan",
            "georgian",
            "belarusian",
            "tajik",
            "sindhi",
            "gujarati",
            "amharic",
            "yiddish",
            "lao",
            "uzbek",
            "faroese",
            "haitian creole",
            "pashto",
            "turkmen",
            "nynorsk",
            "maltese",
            "sanskrit",
            "luxembourgish",
            "myanmar",
            "tibetan",
            "tagalog",
            "malagasy",
            "assamese",
            "tatar",
            "hawaiian",
            "lingala",
            "hausa",
            "bashkir",
            "javanese",
            "sundanese",
            "cantonese",
        ]

    def select(self):
        """
        Display the language selection form
        Returns:
            st.selectbox of languages
        """
        st.subheader("Language Selector")
        st.write("Please select output language")

        return st.selectbox(
            "Select a language:", self.langs, label_visibility="collapsed"
        )


def selector_language():
    """
    Selector of languages
    """
    lang_selector = LangSelector()
    selected_language = lang_selector.select()
    return selected_language
