from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- 1. LLMから回答を得る関数の定義 ---
def get_llm_response(user_input, expert_type):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5) 
    
    # 選択された専門家に応じてシステムメッセージを切り替える
    if expert_type == "料理研究家":
        system_message = "あなたは一流の料理研究家です。レシピや食材について専門的に答えてください。"
    elif expert_type == "ITコンサルタント":
        system_message = "あなたは経験豊富なITコンサルタントです。技術的な課題に対して論理的な解決策を提案してください。"
    else:
        system_message = "あなたは親切なアシスタントです。"

    # プロンプトのテンプレートを作成
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input}")
    ])

    # チェイン（一連の処理）を構成
    chain = prompt | llm | StrOutputParser()
    
    # 実行して結果を返す
    return chain.invoke({"input": user_input})

# --- 2. Streamlit UI の作成 ---
st.title("専門家AIチャットアプリ")
st.write("このアプリは、選択した専門家があなたの質問に回答してくれるアプリです。")

# ラジオボタンで専門家を選択
expert_choice = st.radio(
    "相談したい専門家を選んでください：",
    ("料理研究家", "ITコンサルタント")
)

# 入力フォーム
user_text = st.text_input("質問を入力してください：")

# 送信ボタン
if st.button("送信"):
    if user_text:
        with st.spinner("AIが考えています..."):
            # 関数を呼び出し
            response = get_llm_response(user_text, expert_choice)
            # 結果を表示
            st.subheader("回答結果:")
            st.write(response)
    else:
        st.warning("質問を入力してください。")
            