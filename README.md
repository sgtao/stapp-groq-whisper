# stpyapp-template
[streamlit](https://streamlit.io/)のアプリ開発するためのテンプレートを作ってみる


## Usage
- [poetry cli](https://cocoatomo.github.io/poetry-ja/cli/)を利用する

### Setup
```sh
poetry install
poetry shell
```

### Start as local service
```sh
# on poetry shell
# streamlit hello
streamlit run src/main.py
# Local URL: http://localhost:8501
```

### Test with `pytest`
- [streamlitのテスト手法](https://docs.streamlit.io/develop/concepts/app-testing/get-started)を参考にテストを実施
```sh
# on poetry shell
pytest tests/test_main.py
```

## License
Apache-2.0 license
