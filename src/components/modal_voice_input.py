# modal_voice_input.py
import streamlit as st
from st_audiorec import st_audiorec

from components.language_selector import language_selector
from functions.transcribe_audio import transcribe_audio
from functions.record_audio_file import record_audio_file


@st.dialog("Transprit from Microphone Record")
def modal_voice_input():
    """
    モーダルダイアログとして音声入力を受け取り、文字起こしを行う関数。

    引数:
        なし

    返り値: `st.rerun()`により画面更新を行う
        なし
        # ただし、下の変数へ文字起こし文をセットする
        # - st.session_state.transcript
        # - st.session_state.transcript_shown
    """
    # ユーザーが選択した言語を取得し、プロンプトを設定
    output_language = language_selector()
    prompt = f"Specify context or spelling in {output_language.language}."
    lang = output_language.lang_code
    st.markdown(f"Transcribe Prompt: **{prompt}**")

    # マイク録音を開始し、録音データをセッション状態に保存
    st.session_state.wav_audio_data = st_audiorec()

    # 録音データが存在する場合の処理
    if st.session_state.wav_audio_data is not None:
        if st.button("Start transcription."):
            st.session_state.transcript = ""
            # 録音データをファイルに保存
            wav_file = record_audio_file(st.session_state.wav_audio_data)
            transcript = ""
            # 保存された音声ファイルを開き、文字起こしを実行
            with open(wav_file, "rb") as wave_data:
                transcript = transcribe_audio(wave_data, prompt, lang)
                if transcript != "":
                    st.session_state.transcript = transcript
            # 文字起こし結果を画面に表示
            st.write(st.session_state.transcript)

        # 「Apply to Transcript」ボタンが押された場合の処理
        if st.button("Apply to Transcript"):
            # 文字起こし結果を表示用のセッション状態に保存し、アプリを再実行
            st.session_state.transcript_shown = st.session_state.transcript
            st.rerun()
