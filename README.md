# chatux-server-llm

ちょっと待ってねっ。

謎の呪文
(git、python、pip は各自で用意してねっ)

```
pip3 install -r requirements.txt
ct2-transformers-converter --model line-corporation/japanese-large-lm-3.6b-instruction-sft --low_cpu_mem_usage --output_dir line-sft --quantization int8 --force
python3 ct2-main.py
```
