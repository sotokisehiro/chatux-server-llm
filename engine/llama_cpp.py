from llama_cpp import Llama

from engine.engine import Engine


class LlamaCppEngine(Engine):
    def __init__(self, cpu_thread=0) -> None:
        super().__init__(cpu_thread)
        model_name = "models/ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf"
        self.llm = Llama(
            model_path=model_name,
            n_threads=cpu_thread,
            seed=1234,
        )

    # ELYZA用生成呼び出し
    def generate_text(self, text_input: str) -> str:
        B_INST, E_INST = "[INST]", "[/INST]"  # pylint: disable=invalid-name
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"  # pylint: disable=invalid-name
        SYSTEM_PROMPT = "あなたは誠実で優秀な日本人のアシスタントです。"  # pylint: disable=invalid-name

        prompt = "{b_inst} {system}{prompt} {e_inst} ".format(
            b_inst=B_INST,
            system=f"{B_SYS}{SYSTEM_PROMPT}{E_SYS}",
            prompt=text_input,
            e_inst=E_INST,
        )

        output = self.llm(
            prompt,
            temperature=0.1,
            repeat_penalty=1.1,
            top_k=10000,
            stop=["Instruction:", "Input:", "Response:"],
        )

        return output["choices"][0]["text"]  # type: ignore[index]
