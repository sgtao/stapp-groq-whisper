# 13_chatbot_with_voiceinput..py
import streamlit as st
from groq import Groq

from components.sidebar_key_and_model import sidebar_key_and_model
from components.modal_voice_input import modal_voice_input


# ページの設定
st.set_page_config(page_title="Chatbot with voice input", page_icon="💬")

st.session_state.system_prompt = (
    "You are a helpful assistant. And response in only Japanese."
)
# チャット履歴の初期化
if "groq_chat_history" not in st.session_state:
    st.session_state.groq_chat_history = []

st.title("💬 Groq Chatbot with voice input App")
st.write("This page hosts a chatbot interface with voice input.")

sidebar_key_and_model()
groq_api_key = st.session_state.groq_api_key

if groq_api_key == "":
    st.info("Please add your API key to continue.")
else:
    # ファイルアップロード
    uploaded_file = st.file_uploader(
        "Before 1st question, You can upload an article",
        type=("txt", "md"),
        disabled=(st.session_state.groq_chat_history != []),
    )
    # チャットボットの最初の表示メッセージ
    with st.chat_message("assistant"):
        st.write("Hello!! Say something from input")
    # チャット履歴の表示
    for message in st.session_state.groq_chat_history:
        if message["role"] != "system":  # SYSTEM_PROMPTは表示しない
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

with st.sidebar:
    st.subheader("Audio Input:")
    if st.button("Record audio?"):
        modal_voice_input()

    # 音声入力の結果をst.session_state.transcript_shownに保存する
    if "transcript_shown" not in st.session_state:
        st.session_state.transcript_shown = ""

    # 音声入力の結果を表示する
    st.write("Transcript: (copy from click 📋 icon)")
    st.code(st.session_state.transcript_shown)

# 音声入力の結果をst.chat_inputのデフォルト値として使用する
if question := st.chat_input("Ask something", disabled=not groq_api_key):
    # promptの作成
    user_prompt = ""
    if st.session_state.groq_chat_history == []:
        # 最初のチャットの場合：
        # SYSTEM_PROMPTをメッセージに連結
        system_prompt_item = [
            {
                "role": "system",
                "content": st.session_state.system_prompt,
                "name": "userSupplement",
            }
        ]
        st.session_state.groq_chat_history = system_prompt_item

        # 最初のチャットで添付ファイルがある場合、upload_fileをuser_promptに添付
        # print(type(uploaded_file)) # At no attachment, <class 'NoneType'>
        if uploaded_file is not None:
            article = uploaded_file.read().decode()
            # print(f"attachmented article:{article}")
            user_prompt = f"""Human: Here's an article(添付ファイル):\n\n<article>
            {article}\n\n</article>\n\n{question}\n\nAssistant:"""
        else:
            user_prompt = question

    else:
        # 継続チャットの場合：
        user_prompt = question

    # completionのメッセージを履歴に追加
    st.session_state.groq_chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    # ユーザーのメッセージを表示
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # completionの作成
    if groq_api_key:
        # setup client and parameters
        client = Groq(
            api_key=groq_api_key,
        )
        max_tokens = 2048
        temperature = 0.0
        top_p = 0.0

        # dispatch chat
        chat_completion = client.chat.completions.create(
            messages=st.session_state.groq_chat_history,
            model=st.session_state.selected_model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        # print(chat_completion.choices[0].message.content)
        completion = chat_completion.choices[0].message.content
    else:
        completion = user_prompt

    # prompt, completionのメッセージを履歴に追加
    st.session_state.groq_chat_history.append(
        {"role": "assistant", "content": completion}
    )

    # コンプリーションメッセージを表示
    with st.chat_message("assistant"):
        st.markdown(completion)

    # 最後のメッセージまでスクロール
    st.markdown(
        """
      <script>
        const chat = window.parent.document.querySelector(".chat-container");
        chat.scrollTop = chat.scrollHeight;
      </script>
      """,
        unsafe_allow_html=True,
    )
