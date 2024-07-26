# language_selector.py
import streamlit as st

_LANGUAGES = {
    "en": "english",  # 英語
    "zh": "chinese",  # 中国語
    "de": "german",  # ドイツ語
    "es": "spanish",  # スペイン語
    "ru": "russian",  # ロシア語
    "ko": "korean",  # 韓国語
    "fr": "french",  # フランス語
    "ja": "japanese",  # 日本語
    "pt": "portuguese",  # ポルトガル語
    "tr": "turkish",  # トルコ語
    "pl": "polish",  # ポーランド語
    "nl": "dutch",  # オランダ語
    "ar": "arabic",  # アラビア語
    "sv": "swedish",  # スウェーデン語
    "it": "italian",  # イタリア語
    "id": "indonesian",  # インドネシア語
    "fi": "finnish",  # フィンランド語
    "uk": "ukrainian",  # ウクライナ語
    "el": "greek",  # ギリシャ語
    "cs": "czech",  # チェコ語
    "ro": "romanian",  # ルーマニア語
    "da": "danish",  # デンマーク語
    "hu": "hungarian",  # ハンガリー語
    "no": "norwegian",  # ノルウェー語
    "bg": "bulgarian",  # ブルガリア語
    "lt": "lithuanian",  # リトアニア語
    "lv": "latvian",  # ラトビア語
    "sl": "slovenian",  # スロベニア語
    "et": "estonian",  # エストニア語
}


class Language:
    def __init__(self, lang_code, language):
        self.lang_code = lang_code
        self.language = language


class LangSelector:
    """Class for selecting the Groq model"""

    def __init__(self):
        """Define the available languages"""
        self.langs = _LANGUAGES

    def select(self):
        """
        Display the language selection form
        Returns:
            Language object with lang_code and language
        """
        st.subheader("Language Selector")
        st.write("Please select output language")

        selected_language_name = st.selectbox(
            "Select a language:",
            list(self.langs.values()),
            label_visibility="collapsed",
        )
        selected_language_code = [
            key
            for key, value in self.langs.items()
            if value == selected_language_name
        ][0]
        return Language(selected_language_code, selected_language_name)


def language_selector():
    """
    Selector of languages
    """
    lang_selector = LangSelector()
    selected_language = lang_selector.select()
    return selected_language
