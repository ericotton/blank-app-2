import streamlit as st
from openai import OpenAI

st.title("🔑 OpenAI APIキー動作テスト")
st.write("このページは、APIキーが正しく使えるかどうかをテストします。")

# ★ API クライアントを初期化（Secrets から読み込み）
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("❌ Secrets に OPENAI_API_KEY が設定されていません。")
    st.stop()

# ★ テスト用メッセージ
if st.button("APIキーが動作するかテストする"):
    try:
        response = client.responses.create(
            model="gpt-4o",
            input="APIキーは動作していますか？短く回答してください。"
        )
        reply = response.output_text

        st.success("✅ APIキーは動作しています！")
        st.write("**モデルからの返答:**")
        st.write(reply)

    except Exception as e:
        st.error("❌ API呼び出しでエラーが発生しました。")
        st.write(str(e))
