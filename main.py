import argparse
import html
import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from engine import CTranslate2Engine, ElyzaEngine, Engine

# specify chat server
HOST = "127.0.0.1"
PORT = 8001


# 引数の評価
parser = argparse.ArgumentParser()
parser.add_argument("--listen", type=str, help="Network Share", default="127.0.0.1")
parser.add_argument("--port", type=int, help="Network port", default=8001)
parser.add_argument(
    "--maxspeed",
    type=str,
    help="Max speed up mode. ON/OFF (default OFF)",
    default="OFF",
)
parser.add_argument(
    "--aiengine", type=int, help="AI engine (default llama.cpp)", default=0
)
parser.add_argument(
    "--modelname",
    type=str,
    help="AI model (default ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf)",
    default="models/ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf",
)
args = parser.parse_args()

if args.listen != HOST:
    HOST = args.listen
if args.port != PORT:
    PORT = args.port
if args.maxspeed == "ON":
    # CPUコアの数を設定する。
    CPU_THREAD = os.cpu_count()
else:
    CPU_THREAD = 0

URL = f"http://{HOST}:{PORT}"
SWITCH_AI_ENGINE = args.aiengine
MODEL_NAME = args.modelname


# 生成AIエンジンの初期化
if SWITCH_AI_ENGINE == 0:
    # llama_cpp_python
    # ELYZA/Llama2系の生成エンジン).
    engine: Engine = ElyzaEngine(CPU_THREAD)
else:
    # Ctranslate2
    # LINE生成エンジン.
    engine: Engine = CTranslate2Engine(CPU_THREAD)


app = FastAPI()


# Remove CORS restrictions (if needed)
# from fastapi.middleware.cors import CORSMiddleware
# origins = [
#     f'http://{HOST}',
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/chat_api")
async def chat(text: str = "") -> dict[str, list[dict[str, str]]]:
    res = engine.generate_text(text)
    reply = html.escape(res).replace("\n", "<br>")
    print(f"input:{text} reply:{reply}")

    outJson = {"output": [{"type": "text", "value": reply}]}
    return outJson


app.mount("/", StaticFiles(directory="html", html=True), name="html")


def start_server() -> None:
    uvicorn.run(app, host=HOST, port=PORT)


def main() -> None:
    start_server()

    # When you want to open a browser at the same time
    # Use thread(if needed)
    # import threading
    # import webbrowser
    # threading.Thread(target=start_server).start()
    # webbrowser.open(URL, new=0, autoraise=True)


if __name__ == "__main__":
    main()
