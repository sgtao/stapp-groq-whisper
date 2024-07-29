# record_audio_file.py
import tempfile


def record_audio_file(audio_bytes):
    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".wav"
    ) as temp_audio:
        temp_audio.write(audio_bytes)
        return temp_audio.name
