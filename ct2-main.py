import transformers
import ctranslate2
import transformers
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# specify chat server
HOST = '0.0.0.0'
PORT = 8001
URL = f'http://{HOST}:{PORT}'

model_name = "rinna/japanese-gpt-neox-3.6b-instruction-ppo"
ct2_model = "rinna-ppo-ct2"

current_path = os.path.dirname(os.path.abspath(__file__))
generator = ctranslate2.Generator(ct2_model)

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_name, use_fast=False)


def generate_text(input):
    prompt = "ユーザー :" + input + "<NL>システム :"
    tokens = tokenizer.convert_ids_to_tokens(
        tokenizer.encode(prompt, add_special_tokens=False))
    results = generator.generate_batch(
        [tokens],
        max_length=100,
        sampling_topk=20,
        sampling_temperature=0.7,
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
