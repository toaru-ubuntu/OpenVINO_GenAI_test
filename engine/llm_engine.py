import threading
import queue
import openvino_genai

class OpenVINOEngine:
    def __init__(self, model_path: str, device: str = "GPU"):
        print(f"Loading OpenVINO model from {model_path} on {device}...")
        self.pipe = openvino_genai.LLMPipeline(model_path, device)
        print("Model loaded successfully!")

    def generate_stream(self, messages: list, max_tokens: int = 4096):
        """ストリーミング推論を行い、結果をキューに格納して返す"""
        history = openvino_genai.ChatHistory()
          # --- ここに追加：システムプロンプトで思考を禁止する ---
        history.append({
            "role": "system", 
            "content": "あなたは優秀なアシスタントです。<think>タグを使った思考プロセスを出力しないでください。直接、最終的な回答のみを簡潔に述べてください。"
        })
        # ----------------------------------------------------
        for m in messages:
            history.append({"role": m["role"], "content": m["content"]})
            
        config = openvino_genai.GenerationConfig()
        config.max_new_tokens = max_tokens
        
        # --- 繰り返しループ対策 ---
        # 同じ言葉を繰り返すのを防ぐペナルティ（1.1〜1.2程度がおすすめ）
        config.repetition_penalty = 1.1 
        # テキストの多様性（0.7〜0.8程度）
        config.temperature = 0.7        
        
        q = queue.Queue()
        
        def streamer(subword):
            q.put(subword)
            return False

        def generation_thread():
            self.pipe.generate(history, config, streamer)
            q.put(None) # 終了シグナル

        threading.Thread(target=generation_thread).start()
        
        return q
