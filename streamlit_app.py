import streamlit as st
import openai
from openai import OpenAI, RateLimitError

# 🔑 Secrets に入れた APIキーでクライアントを作成
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("💬 ChatGPTと会話するアプリ")
st.write("OpenAI APIキーを使って、ChatGPT (GPT-4o) と会話します。")

# セッション状態に会話履歴を保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": "あなたは日本語で丁寧に会話するアシスタントです。",
        }
    ]

# これまでの会話を表示（systemは表示しない）
for msg in st.session_state["messages"]:
    if msg["role"] == "system":
        continue
    st.chat_message("user" if msg["role"] == "user" else "assistant").write(
        msg["content"]
    )

# ユーザー入力欄
user_input = st.chat_input("メッセージを入力してください…")

if user_input:
    # ユーザーメッセージを履歴に追加＆表示
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        # Chat Completions API で返答生成
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state["messages"],
        )
        assistant_reply = response.choices[0].message.content

        # 返答を履歴に追加＆表示
        st.session_state["messages"].append(
            {"role": "assistant", "content": assistant_reply}
        )
        st.chat_message("assistant").write(assistant_reply)

    except RateLimitError as e:
        st.error(
            "❌ APIの利用上限またはクレジット不足によりリクエストが拒否されました。\n\n"
            "以下のページからクレジットを追加してください：\n"
            "https://platform.openai.com/settings/organization/billing/overview"
        )
    except Exception as e:
        st.error("❌ 予期しないエラーが発生しました。")
        st.write(str(e))
