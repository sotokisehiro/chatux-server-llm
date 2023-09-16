import ctranslate2
import transformers

from engine.engine import Engine


class CTranslate2Engine(Engine):
    def __init__(self, cpu_thread=0) -> None:
        super().__init__(cpu_thread)
        self.model_name = "line-corporation/japanese-large-lm-3.6b-instruction-sft"
        self.ct2_model = "line-sft"
        if cpu_thread == 0:
            self.generator = ctranslate2.Generator(self.ct2_model)
        else:
            self.generator = ctranslate2.Generator(
                self.ct2_model,
                inter_threads=cpu_thread,
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
