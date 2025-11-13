import streamlit as st
from openai import OpenAI

# 🔑 OpenAI クライアント（Secrets から APIキーを取得）
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------
# サイドバー：今日のメンタリング設定
# -------------------------
st.sidebar.title("🧭 メンタリング設定")

focus = st.sidebar.selectbox(
    "今日のテーマ",
    [
        "学習計画を立てたい",
        "勉強が進まずモヤモヤしている",
        "タスクを整理したい",
        "研究・仕事の方針を整理したい",
        "とりあえず話を聞いてほしい",
    ],
)

goal = st.sidebar.text_area(
    "今日このチャットで得たいこと（任意）",
    placeholder="例：今週やることを3つに絞りたい／試験までの学習計画をざっくり決めたい など",
)

if st.sidebar.button("💥 会話をリセットする"):
    st.session_state.clear()
    st.experimental_rerun()

# -------------------------
# メイン画面
# -------------------------
st.title("💬 メンタリング・チャット")
st.caption("※ 学習・仕事・研究の整理や計画づくりを一緒に考えるためのチャットです。")

# システムプロンプト（メンタリング方針）
def build_system_prompt(focus_text: str, goal_text: str) -> str:
    base = f"""
あなたは、成人学習者・研究者・社会人のためのメンタリングアシスタントです。
学習や仕事の計画づくり、振り返り、モヤモヤの言語化をサポートします。

方針:
- 命令ではなく、「問いかけ」と「言語化の手伝い」を中心にしてください。
- できるだけ一度に質問しすぎず、1〜2問ずつ確認しながら進めてください。
- ユーザーの自己決定とペースを尊重し、できている点も必ず拾ってください。
- アドバイスをするときは、「いくつかの選択肢」として提案してください。
- 精神医療や診断が必要な内容には踏み込まず、「専門職への相談」を勧めるにとどめてください。

今日ユーザーが選んだテーマ: 「{focus_text}」
"""
    if goal_text.strip():
        base += f"\nユーザーが今日このチャットで得たいと考えていること: 「{goal_text.strip()}」\n"
    base += "\n最初の発話では、簡単に自己紹介をした上で、ユーザーの今の状況を丁寧に質問してください。"
    return base

system_prompt = build_system_prompt(focus, goal)

# -------------------------
# 会話履歴の初期化
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
    ]
else:
    # テーマやゴールが変わった場合はシステムメッセージだけ更新
    if st.session_state["messages"][0]["role"] == "system":
        st.session_state["messages"][0]["content"] = system_prompt

# これまでのメッセージを表示（system は表示しない）
for msg in st.session_state["messages"]:
    if msg["role"] == "system":
        continue
    st.chat_message("user" if msg["role"] == "user" else "assistant").write(msg["content"])

# -------------------------
# ユーザー入力
# -------------------------
user_input = st.chat_input("いまの状況や、相談したいことを書いてみてください…")

if user_input:
    # ユーザー発話を追加・表示
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # OpenAI API で応答生成
    with st.spinner("メンタリング中…"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state["messages"],
            )
            assistant_reply = response.choices[0].message.content

            # 応答を履歴に追加・表示
            st.session_state["messages"].append(
                {"role": "assistant", "content": assistant_reply}
            )
            st.chat_message("assistant").write(assistant_reply)

        except Exception as e:
            st.error("❌ メンタリング応答の生成中にエラーが発生しました。")
            st.write(str(e))
