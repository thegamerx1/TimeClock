from app import templates, db_path

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, FileResponse

from typing import Annotated

import tempfile
from pathlib import Path
import hashlib
import pyttsx3


import pyodbc

VOICE_DIR = Path(tempfile.gettempdir()).joinpath("voicefiles/")
Path(VOICE_DIR).mkdir(exist_ok=True)

router = APIRouter()


class get_db:
    def __init__(self):
        return None

    def __enter__(self):
        print(db_path)
        self.conn = pyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + db_path + ";"
        )
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, _a, _b, _c):
        self.cursor.close()
        self.conn.close()


@router.get(
    path="/",
    summary="Main page",
    tags=["Authentication"],
    response_class=HTMLResponse,
)
async def get_login(request: Request):
    users = []
    with get_db() as db:
        db.cursor.execute("SELECT * FROM Personas WHERE BloquearAcceso = 0")
        for row in db.cursor.fetchall():
            print(row)
            users.append({"name": f"{row[2]}, {row[1]}", "Id": row[0]})

    context = {
        "request": request,
        "users": users,
    }
    return templates.TemplateResponse("pages/login.html", context)


@router.post(path="/login", summary="Logs into the app", tags=["Authentication"])
async def post_login(
    userId: Annotated[str, Form()], pin: Annotated[str, Form()]
) -> dict:
    with get_db() as db:
        db.cursor.execute(f"SELECT * FROM Personas WHERE Id = (?)", (userId))
        persona = db.cursor.fetchone()

    if persona is None or str(persona[3]) != pin:
        print("bad :(")
        return {"success": False}

    # TODO: Fichar en la DB

    return {"success": True}


@router.post(
    path="/loginCodigoQR", summary="Logs into the app", tags=["Authentication"]
)
async def post_login(pinCodigoQR: Annotated[str, Form()]) -> dict:
    with get_db() as db:
        db.cursor.execute(
            f"SELECT * FROM Personas WHERE PINCodigoQR = (?)",
            (pinCodigoQR),
        )
        persona = db.cursor.fetchone()

    if persona is None:
        return {"success": False}

    nombre = f"{persona[2]}, {persona[1]}"

    id_voz = generar_voz(f"Hola, bienvenido {nombre}")

    # TODO: Fichar en la DB

    return {"success": True, "username": nombre, "voz_id": id_voz}


@router.get(path="/voz/{id_voz}", summary="Da el archivo de voz")
async def get_voz(id_voz: str):
    # TODO: ESTO ES VULNERABLE A LFI SOLUCIONAR DESPUES
    return FileResponse(VOICE_DIR.joinpath(id_voz + ".mp3"), media_type="audio/mpeg")


def create_engine():
    engine = pyttsx3.init()

    engine.setProperty("rate", 130)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    # for voice in voices:
    # print(voice)
    engine.setProperty("voice", voices[0].id)

    return engine


def generar_voz(texto: str) -> str:
    text_hash = hashlib.md5(texto.encode()).hexdigest()
    archivo = text_hash + ".mp3"
    destination = VOICE_DIR.joinpath(archivo)

    if destination.exists():
        return text_hash

    engine = create_engine()

    engine.save_to_file(text=texto, filename=archivo, dir=VOICE_DIR)
    engine.runAndWait()
    engine.stop()
    return text_hash
