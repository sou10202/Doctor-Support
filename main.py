# app.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from ragie import Ragie
from openai import OpenAI
import tiktoken

load_dotenv()
app = FastAPI()

ragie = Ragie(auth=os.getenv("RAGIE_API_KEY"))
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
MAX_CONTEXT_TOKENS = 10000
SCOPE = "tutorial"

class QueryRequest(BaseModel):
    query: str
    history: list

def truncate_chunks(chunks, max_tokens):
    selected = []
    total = 0
    for chunk in chunks:
        tokens = len(tokenizer.encode(chunk.text))
        if total + tokens > max_tokens:
            break
        selected.append(chunk.text)
        total += tokens
    return selected

@app.post("/ask")
async def ask_ragie_ai(request: QueryRequest):
    try:
        retrieval_res = ragie.retrievals.retrieve(request={
            "query": request.query,
            "filter_": {"scope": SCOPE}
        })

        if not retrieval_res.scored_chunks:
            return {"answer": "関連情報が見つかりませんでした。質問を変えてみてください。"}

        limited_chunks = truncate_chunks(retrieval_res.scored_chunks, MAX_CONTEXT_TOKENS)
        context = "\n".join(limited_chunks)

        system_prompt = f"""あなたは専門的な医療AIです。
以下の情報に基づき、質問に対して自然な日本語で簡潔に答えてください。
回答はカジュアルかつ簡潔に行い、**見出しなし**で直接回答してください。ただし、必要な情報はすべて含めてください。
Markdown 形式で適切に装飾を行い、**太字**・*斜体*・リストなども使用してください。
必要に応じて情報をセクションや箇条書きで整理してください。
生データのIDや技術的なフィールドは含めないでください。
XMLやその他のマークアップ言語はリクエストがない限り使用しないでください。

===
{context}
===
"""

        chat = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.query}
            ]
        )

        return {"answer": chat.choices[0].message.content.strip()}

    except Exception as e:
        return {"answer": f"エラーが発生しました: {str(e)}"}

import os
import gradio as gr
from dotenv import load_dotenv
from ragie import Ragie
from openai import OpenAI
import tiktoken

load_dotenv()

# 認証
ragie = Ragie(auth=os.getenv("RAGIE_API_KEY"))
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ドキュメントが属する情報
# DOCUMENT_PARTITION = "test_partition"
SCOPE = "tutorial"


tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
MAX_CONTEXT_TOKENS = 10000  # 例：余白を持って10000に制限

def truncate_chunks(chunks, max_tokens):
    selected = []
    total = 0
    for chunk in chunks:
        tokens = len(tokenizer.encode(chunk.text))
        if total + tokens > max_tokens:
            break
        selected.append(chunk.text)
        total += tokens
    return selected

# 質問→検索→GPT回答（すべて日本語）
def ask_ragie_ai(query, history):
    try:
        retrieval_res = ragie.retrievals.retrieve(request={
            "query": query,
            "filter_": {"scope": SCOPE}
        })

        if not retrieval_res.scored_chunks:
            return "関連情報が見つかりませんでした。質問を変えてみてください。"

        limited_chunks = truncate_chunks(retrieval_res.scored_chunks, MAX_CONTEXT_TOKENS)
        context = "\n".join(limited_chunks)

        system_prompt = f"""あなたは専門的な医療AIです。
以下の情報に基づき、質問に対して自然な日本語で簡潔に答えてください。
回答はカジュアルかつ簡潔に行い、**見出しなし**で直接回答してください。ただし、必要な情報はすべて含めてください。
Markdown 形式で適切に装飾を行い、**太字**・*斜体*・リストなども使用してください。
必要に応じて情報をセクションや箇条書きで整理してください。
生データのIDや技術的なフィールドは含めないでください。
XMLやその他のマークアップ言語はリクエストがない限り使用しないでください。

===
{context}
===
"""

        chat = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )

        return chat.choices[0].message.content.strip()

    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


# Gradio UI
def launch_ui():
    gr.ChatInterface(
        fn=ask_ragie_ai,
        title="Doctor Support AI",
        description="質問を入力すると、日本語で回答します。",
        chatbot=gr.Chatbot(height=600), 
    ).launch()

if __name__ == "__main__":
    launch_ui()