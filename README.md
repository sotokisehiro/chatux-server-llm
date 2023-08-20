# chatux-server-llm

ローカル環境で動作する文章生成 AI チャットボットです。
CPU だけで動作します。（NVIDA のグラボは不要）

# 要件

- 第 8 世代以降の Corei 3
- メインメモリ 8G バイト
- ストレージ 10G バイト（SSD を強く推奨）
- OS: Linux/Windows11 で動作を確認しています。
- その他: Linux 用の簡易インストーラ/サーバー起動用のスクリプトあり

# インストール手順（Linux 版）

任意のディレクトリで、付属の簡易インストーラスクリプトを実行してください。

```
bash ./install_linux.sh
```

# インストール手順（Windows 版）

本サイトからなんらかの方法で環境一式をダウンロードし、任意のフォルダに配置したのち、PowerShell から次のコマンドを実行してください。

```
python3 -m venv venv
venv/Scripts/activate
pip3 install -r requirements.txt
ct2-transformers-converter --model line-corporation/japanese-large-lm-3.6b-instruction-sft --low_cpu_mem_usage --output_dir line-sft --quantization int8 --force

python3 ct2-main.py
```

# 実行時の注意

初回実行時のみ、インターネットから大量のダウンロードが発生するため、しばらくお待ちください。
エラーがなければ AI サーバーが起動しますので、
ブラウザから次の URL を開いてください。

```
http://127.0.0.1:8001/
```

次のような画面が表示されれば起動成功です。お楽しみください。

![Alt text](img/img01.png)

次の画像をクリックすると youtube で応答速度を確認できます。

[![応答イメージ](img/img02.png)](https://youtu.be/h3-edtm-NLQ)

# TIPS

- メモリ不足で言語モデル変換できない方は
  [huggingface](https://huggingface.co/sehiro/LINE-ct2-jp)
  から変換済のモデルをダウンロードしてください。
  もっともメモリを使う「ct2-transformers-converter」コマンドの実行をスキップできます。

## ToDo

- Windows 版インストーラの開発
- LoRA のサポート

# ライセンス

MIT
