from gtts import gTTS
from io import BytesIO


def text_to_speech_bytes(text: str) -> bytes:
    """
    Given text, return MP3 audio bytes using gTTS.
    """
    if not text.strip():
        return b""

    tts = gTTS(text)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.getvalue()
