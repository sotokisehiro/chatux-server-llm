#!/usr/bin/env bash

# 最小限必要なLinuxコマンドのインストール（管理者権限が必要）
sudo apt install git
sudo apt install pip
sudo apt install python3-venv

# ダウンロード＆インストール
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
ct2-transformers-converter --model line-corporation/japanese-large-lm-3.6b-instruction-sft --low_cpu_mem_usage --output_dir line-sft --quantization int8 --force
wget -P models https://huggingface.co/mmnga/ELYZA-japanese-Llama-2-7b-fast-instruct-gguf/resolve/main/ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf

# サーバー起動
python3 main.py
