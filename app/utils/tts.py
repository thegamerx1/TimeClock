import tempfile
import pyttsx3
import hashlib
from shutil import move
from pathlib import Path

VOICE_DIR = Path(tempfile.gettempdir()).joinpath("voicefiles/")
Path(VOICE_DIR).mkdir(exist_ok=True)


def create_engine():
    engine = pyttsx3.init()

    engine.setProperty("rate", 130)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    # for voice in voices:
    # print(voice)
    # TODO: Add this to config.json
    engine.setProperty("voice", voices[0].id)

    return engine


def generate_tts(text: str) -> str:
    text_hash = hashlib.md5(text.encode()).hexdigest()
    archivo_voz = text_hash + ".mp3"
    destination = VOICE_DIR.joinpath(archivo_voz)

    if destination.exists():
        return text_hash

    engine = create_engine()

    print(VOICE_DIR.joinpath(archivo_voz))
    engine.save_to_file(text=text, filename=archivo_voz)
    engine.runAndWait()
    engine.stop()
    # Sufrimiento
    move("./" + archivo_voz, VOICE_DIR)
    return text_hash


def tts_from_id(id: str) -> Path:
    # TODO: ESTO ES VULNERABLE A LFI SOLUCIONAR DESPUES
    return VOICE_DIR.joinpath(id + ".mp3")
