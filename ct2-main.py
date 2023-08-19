import transformers
import ctranslate2
import transformers
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import argparse

# specify chat server
HOST = '127.0.0.1'
PORT = 8001
URL = f'http://{HOST}:{PORT}'

# 引数の評価
parser = argparse.ArgumentParser()
parser.add_argument("--listen", type=str,
                    help="Network Share", default="127.0.0.1")
parser.add_argument("--port", type=int,
                    help="Network Share", default=8001)
args = parser.parse_args()

if args.listen != HOST:
    HOST = args.listen
if args.port != PORT:
    PORT = args.port

model_name = "line-corporation/japanese-large-lm-3.6b-instruction-sft"
ct2_model = "line-sft"

current_path = os.path.dirname(os.path.abspath(__file__))
generator = ctranslate2.Generator(ct2_model)

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_name, use_fast=False)


def generate_text(input):
    prompt = "ユーザー :" + input + "システム :"
    tokens = tokenizer.convert_ids_to_tokens(
        tokenizer.encode(prompt, add_special_tokens=False))
    results = generator.generate_batch(
        [tokens],
        max_length=100,
        sampling_topk=20,
        sampling_temperature=0.5,
        include_prompt_in_result=False,
        repetition_penalty=1.1,
    )
    text = tokenizer.decode(results[0].sequences_ids[0])
    return text


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
async def chat(text: str = ""):
    res = generate_text(text)
    generated_text = res
    reply = generated_text.replace('\n', '<br>')
    print(f'input:{text} reply:{reply}')

    outJson = {
        "output": [
            {
                "type": "text",
                "value": reply
            }
        ]
    }
    return outJson


app.mount("/", StaticFiles(directory="html", html=True), name="html")


def start_server():
    uvicorn.run(app, host=HOST, port=PORT)


def main():
    start_server()

    # When you want to open a browser at the same time
    # Use thread(if needed)
    # import threading
    # import webbrowser
    # threading.Thread(target=start_server).start()
    # webbrowser.open(URL, new=0, autoraise=True)


if __name__ == "__main__":
    main()
