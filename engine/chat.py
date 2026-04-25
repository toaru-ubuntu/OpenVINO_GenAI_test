import gradio as gr
import time
from openai import OpenAI

# ここを実際のモデル名に変更
MODEL_NAME = "openai/gpt-oss-20b"

client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")

def chat(message, history):
    start = time.time()
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": message}],
        stream=True,
        stream_options={"include_usage": True}
    )
    
    reply = ""
    tokens = 0
    
    for chunk in response:
        if chunk.usage:
            tokens = chunk.usage.completion_tokens
        
        if chunk.choices and chunk.choices[0].delta.content:
            reply += chunk.choices[0].delta.content
            elapsed = time.time() - start
            tps = tokens / elapsed if tokens > 0 else 0
            
            if tokens > 0:
                yield f"{reply}\n\n---\n📊 {tokens} tokens in {elapsed:.2f}s ({tps:.1f} tok/s)"
            else:
                yield reply
    
    elapsed = time.time() - start
    tps = tokens / elapsed if tokens > 0 else 0
    yield f"{reply}\n\n---\n📊 {tokens} tokens in {elapsed:.2f}s ({tps:.1f} tok/s)"

# カスタムCSSでチャットエリアを広げる
custom_css = """
.chatbot {
    height: 70vh !important;
    max-height: 800px !important;
}
"""

with gr.Blocks() as demo:
    gr.ChatInterface(
        chat,
        title="vLLM Chat",
        chatbot=gr.Chatbot(height=780)
    )

demo.launch(css=custom_css, inbrowser=True)
