# stapp-groq-whisper
Groq APIを使って Whisperアプリを立ち上げてみる

## コンテンツ
- サンプルコード（[streamlit-example](https://github.com/streamlit/streamlit-example)）を追加
- [Demo site](https://stapp-groq-whisper-nri4uidhbqpqcgi62tgjkn.streamlit.app/)

## Usage
- [poetry cli](https://cocoatomo.github.io/poetry-ja/cli/)を利用する

### Setup
```sh
poetry install
# if install main package, execute following: # previously --no-dev
# poetry install --only main
#
# to run tasks on poetry-shell.
poetry shell
```

### コマンド一覧
```sh
$ task --list
start        streamlit run src/main.py
test         pytest tests
test-cov     pytest tests --cov --cov-branch -svx
test-repo    pytest tests --cov --cov-report=html
format       black --line-length 79 src
lint         flake8 src
check-format black整形とflake8チェックを実行
```

### Start as local service
```sh
# on poetry shell
# streamlit hello
# streamlit run src/main.py
task start
# Local URL: http://localhost:8501
```


### format and lint check
```sh
# task format
# task lint
task check-format
```


### Test with `pytest`
- [streamlitのテスト手法](https://docs.streamlit.io/develop/concepts/app-testing/get-started)を参考にテストを実施
```sh
# on poetry shell
# pytest tests/test_main.py
task test
```

### Test coverage

#### show c1 coverage
```sh
# on poetry shell
task test-cov
```

#### output HTML coverage report
```sh
# on poetry shell
task test-repo
```


## 使用ライブラリ

このプロジェクトは以下のオープンソースライブラリを使用しています：

- [Streamlit](https://streamlit.io/) - Apache License 2.0

  Copyright © 2019-2024 Streamlit Inc.

  Streamlitは、データアプリケーションを簡単に作成するためのオープンソースライブラリです。


## ライセンス
Apache 2.0

このプロジェクトは Apache 2.0 ライセンスの下で公開されています。詳細は [LICENSE](./LICENSE) ファイルをご覧ください。

ただし、このプロジェクトは Apache License 2.0 でライセンスされている Streamlit を使用しています。
Streamlit のライセンス全文は [こちら](https://github.com/streamlit/streamlit/blob/develop/LICENSE) でご確認いただけます。
