#!/bin/bash
cd /home/sakasu/dev/bot/ # Pythonスクリプトがあるディレクトリに移動
source /home/sakasu/dev/bot/search.env  # .envファイルから環境変数を読み込む
/usr/bin/python3 /home/sakasu/dev/bot/search.py   # Pythonスクリプトを実行
