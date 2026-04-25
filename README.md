# OpenVINO_GenAI_test

OpenVINO GenAIを使ったテストリポジトリです。
使用する場合、自己責任でお願いします。

## 仕様するモデルファイル

https://huggingface.co/OpenVINO/Qwen3-8B-int4-cw-ov
上記リンクからダウンロードしています。
モデルを変更したい場合はソースコードを書き直してください。

## テスト環境

* **OS**: Linux (Ubuntu24.04.4LTS)
* **Python**: 3.12.3
* **ハードウェア**: 
  *Intel Arc A750(VRAM8GB)でテストしています。

## 🛠 インストール方法

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/toaru-ubuntu/OpenVINO_GenAI_test.git
   cd OpenVINO_GenAI_test
   
2. **Python仮想環境の作成と有効化**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    
3. **必要なパッケージのインストール**
    ```bash
    # OpenVINO GenAIインストール
    pip install openvino-genai optimum[openvino]
    # その他の必須ライブラリ
    pip install fastapi uvicorn pydantic openai gradio
    
4. **モデルファイルの配置** 
    ```bash
    OpenVINO_GenAI_test/Qwen3-8B-int4-cw-ov
    
5. **使い方**
仮想環境を有効化した状態で、メインスクリプトを実行します。
    ```bash
    python run.py

## 📄 ライセンス/ License

以下を参照してください。
https://github.com/openvinotoolkit/openvino.genai

参考URL
https://openvinotoolkit.github.io/openvino.genai/
