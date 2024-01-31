from app import templates

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from app.utils.database import get_db
from app.utils.tts import generate_tts, tts_from_id

from typing import Annotated
from datetime import datetime

router = APIRouter()
db_con = get_db()


@router.get(
    path="/",
    summary="Serves the login template",
    include_in_schema=False,
    response_class=HTMLResponse,
)
async def get_login(request: Request):
    # users = []
    # db_con.cursor.execute("SELECT * FROM Personas WHERE BloquearAcceso = 0")
    # for row in db_con.cursor.fetchall():
    #     users.append({"name": f"{row[2]}, {row[1]}", "Id": row[0]})

    context = {
        "request": request,
        # "users": users,
    }
    return templates.TemplateResponse("pages/login.html", context)


@router.post(
    path="/loginCodigoQR",
    summary="Logs in with a qr code",
    response_class=JSONResponse,
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "mensaje": "Welcome John Doe",
                        "voz_id": "0cc175b9c0f1b6a831c399e269772661",
                    }
                }
            },
        },
    },
)
async def post_login(pinCodigoQR: Annotated[str, Form()]) -> dict:
    db_con.cursor.execute(
        f"SELECT * FROM Personas WHERE PINCodigoQR = (?)",
        (pinCodigoQR),
    )
    persona = db_con.cursor.fetchone()

    if persona is None:
        return {"success": False}


    fichajes = db_con.cursor.execute(
        f"SELECT * FROM Fichajes WHERE IdPersona = {persona[0]} AND FechaSalida Is Null ORDER BY FechaEntrada"
    )

    laprimera = fichajes.fetchone()
    now = datetime.now()

    if not laprimera == None and laprimera[3] == None:
        sql = f"UPDATE Fichajes SET FechaSalida = ? WHERE Id = {laprimera[0]}"
        mensaje = "Que tengas un buen día"
    else:
        sql = f"INSERT INTO Fichajes (FechaEntrada,IdPersona,Metodo) VALUES (?,{persona[0]},1)"
        mensaje = "Hola, bienvenido"

    db_con.cursor.execute(sql, (now))

    nombre = f"{persona[2]}, {persona[1]}"
    nombre_correcto = f"{persona[1]} {persona[2]}"

    id_voz = generate_tts(f"{mensaje} {nombre_correcto}")

    db_con.commit()
    return {
        "success": True,
        "mensaje": f"{mensaje} {nombre}",
        "voz_id": id_voz,
    }


@router.get(
    path="/voz/{id_voz}",
    summary="Serves a generated audio file",
    response_class=FileResponse,
    responses={
        200: {
            "description": "Serves the audio file",
            "content": {"audio/mpeg": {}},
        },
        404: {
            "description": "Audio file not found",
        },
    },
)
async def get_voz(id_voz: str) -> FileResponse:
    id_archivo = tts_from_id(id_voz)
    if not id_archivo.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(id_archivo, media_type="audio/mpeg")
