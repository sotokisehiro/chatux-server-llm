import torch
from transformers import AutoModelForCausalLM, LlamaTokenizer

from engine.engine import Engine


class AutoModelForCausalLMEngine(Engine):
    def __init__(self, cpu_thread=0) -> None:
        super().__init__(cpu_thread)
        self.tokenizer = LlamaTokenizer.from_pretrained(
            "novelai/nerdstash-tokenizer-v1", additional_special_tokens=["▁▁"]
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "stabilityai/japanese-stablelm-base-alpha-7b",
            trust_remote_code=True,
        )
        print(type(self.model))
        print(type(self.model))
        print(type(self.model))
        print(type(self.model))
        print(type(self.model))

        self.model.half()
        self.model.eval()

        if torch.cuda.is_available():
            self.model = self.model.to("cuda")

    # Japanese StableLM Alpha 生成呼び出し
    def generate_text(self, input) -> str:
        prompt = """
        AI で科学研究を加速するには、
        """.strip()

        input_ids = self.tokenizer.encode(
            prompt, add_special_tokens=False, return_tensors="pt"
        )

        # this is for reproducibility.
        # feel free to change to get different result
        seed = 23
        torch.manual_seed(seed)

        tokens = self.model.generate(
            input_ids.to(device=self.model.device),
            max_new_tokens=128,
            temperature=1,
            top_p=0.95,
            do_sample=True,
        )

        out = self.tokenizer.decode(tokens[0], skip_special_tokens=True)
        return out
