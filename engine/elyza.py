from llama_cpp import Llama

from engine.engine import Engine


class ElyzaEngine(Engine):
    def __init__(self, cpu_thread=0) -> None:
        super().__init__(cpu_thread)
        model_name = "models/ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf"
        self.llm = Llama(
            model_path=model_name,
            n_threads=cpu_thread,
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
