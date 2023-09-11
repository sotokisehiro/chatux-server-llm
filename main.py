import argparse
import html
import os

import ctranslate2
import transformers
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from llama_cpp import Llama

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


class Engine(object):
    def generate_text(self, input) -> str:
        raise NotImplementedError()


class ElyzaEngine(Engine):
    def __init__(self) -> None:
        self.llm = Llama(
            model_path=MODEL_NAME,
            n_threads=CPU_THREAD,
            seed=1234,
        )

    # ELYZA用生成呼び出し
    def generate_text(self, input) -> str:
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        DEFAULT_SYSTEM_PROMPT = "あなたは誠実で優秀な日本人のアシスタントです。"

        prompt = "{b_inst} {system}{prompt} {e_inst} ".format(
            b_inst=B_INST,
            system=f"{B_SYS}{DEFAULT_SYSTEM_PROMPT}{E_SYS}",
            prompt=input,
            e_inst=E_INST,
        )

        output = self.llm(
            prompt,
            temperature=0.1,
            repeat_penalty=1.1,
            top_k=10000,
            stop=["Instruction:", "Input:", "Response:"],
        )

        return output["choices"][0]["text"]


class CtranslateEngine(Engine):
    def __init__(self) -> None:
        self.model_name = "line-corporation/japanese-large-lm-3.6b-instruction-sft"
        self.ct2_model = "line-sft"
        if CPU_THREAD == 0:
            self.generator = ctranslate2.Generator(self.ct2_model)
        else:
            self.generator = ctranslate2.Generator(
                self.ct2_model,
                inter_threads=CPU_THREAD,
            )
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_name, use_fast=False
        )

    # LINE用生成呼び出し
    def generate_text(self, input) -> str:
        prompt = "ユーザー :" + input + "システム :"
        tokens = self.tokenizer.convert_ids_to_tokens(
            self.tokenizer.encode(prompt, add_special_tokens=False)
        )
        results = self.generator.generate_batch(
            [tokens],
            max_length=100,
            sampling_topk=20,
            sampling_temperature=0.5,
            include_prompt_in_result=False,
            repetition_penalty=1.1,
        )
        text = self.tokenizer.decode(results[0].sequences_ids[0])
        return text


# 生成AIエンジンの初期化
if SWITCH_AI_ENGINE == 0:
    # llama_cpp_python
    # ELYZA/Llama2系の生成エンジン).
    engine: Engine = ElyzaEngine()
else:
    # Ctranslate2
    # LINE生成エンジン.
    engine: Engine = CtranslateEngine()


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
