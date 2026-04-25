import asyncio
import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import StreamingResponse

# 分割した自作モジュールを読み込む
from llm_engine import OpenVINOEngine

# --- 設定 ---
MODEL_PATH = "../Qwen3-8B-int4-cw-ov"
    
DEVICE = "GPU"  # "GPU","AUTO" 
CONTEXT = 8192

# エンジンの初期化
engine = OpenVINOEngine(MODEL_PATH, DEVICE)
app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = False
    max_tokens: Optional[int] = CONTEXT
    stream_options: Optional[dict] = None

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest):
    # Pydanticのモデルから辞書のリストへ変換
    messages_dict = [{"role": m.role, "content": m.content} for m in req.messages]
    
    # llm_engine側のメソッドを呼び出して推論を開始
    q = engine.generate_stream(messages_dict, req.max_tokens)

    async def event_generator():
        tokens = 0
        while True:
            # キューにデータが入るまで非同期で待機
            while q.empty():
                await asyncio.sleep(0.01)
                
            token = q.get()
            
            if token is None:
                # 終了処理とトークン使用量の送信
                if req.stream_options and req.stream_options.get("include_usage"):
                    usage_chunk = {
                        "choices": [],
                        "usage": {"completion_tokens": tokens, "prompt_tokens": 0, "total_tokens": tokens}
                    }
                    yield f"data: {json.dumps(usage_chunk)}\n\n"
                yield "data: [DONE]\n\n"
                break
                
            tokens += 1
            chunk = {"choices": [{"delta": {"content": token}}]}
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
