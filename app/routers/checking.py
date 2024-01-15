from app import templates

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

from app.utils.database import get_db
from app.utils.tts import generate_tts, tts_from_id

from typing import Annotated
from datetime import datetime

router = APIRouter()


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


# @router.post(path="/login", summary="Logs into the app", tags=["Authentication"])
# async def post_login(
#     userId: Annotated[str, Form()], pin: Annotated[str, Form()]
# ) -> dict:
#     with get_db() as db:
#         db.cursor.execute(f"SELECT * FROM Personas WHERE Id = (?)", (userId))
#         persona = db.cursor.fetchone()

#     if persona is None or str(persona[3]) != pin:
#         print("bad :(")
#         return {"success": False}

#     # TODO: Fichar en la DB

#     return {"success": True}


@router.post(
    path="/loginCodigoQR", summary="Logs into the app", tags=["Authentication"]
)
async def post_login(pinCodigoQR: Annotated[str, Form()]) -> dict:
    db = get_db()
    db.cursor.execute(
        f"SELECT * FROM Personas WHERE PINCodigoQR = (?)",
        (pinCodigoQR),
    )
    persona = db.cursor.fetchall()

    if persona is None:
        return {"success": False}

    persona = persona[0]
    print(persona)

    fichajes = db.cursor.execute(
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

    db.cursor.execute(sql, (now))

    nombre = f"{persona[2]}, {persona[1]}"
    nombre_correcto = f"{persona[1]} {persona[2]}"

    id_voz = generate_tts(f"{mensaje} {nombre_correcto}")

    db.commit()
    db.close()
    return {
        "success": True,
        "mensaje": f"{mensaje} {nombre}",
        "voz_id": id_voz,
    }


@router.get(path="/voz/{id_voz}", summary="Da el archivo de voz")
async def get_voz(id_voz: str):
    id_archivo = tts_from_id(id_voz)
    if not id_archivo.exists():
        raise HTTPException(status_code=404, detail="La voz no fue generada aún")

    return FileResponse(id_archivo, media_type="audio/mpeg")
