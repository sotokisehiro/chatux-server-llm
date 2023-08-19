# chatux-server-llm

ちょっと待ってねっ。

謎の呪文

```
pip install -r requirements.txt
ct2-transformers-converter --model line-corporation/japanese-large-lm-3.6b-instruction-sft --low_cpu_mem_usage --output_dir line-sft --quantization int8 --force
python ct2-main.py
```
