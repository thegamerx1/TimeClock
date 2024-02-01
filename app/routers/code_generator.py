from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse

from aztec_code_generator import AztecCode
from io import BytesIO
from PIL import Image

router = APIRouter()


@router.get(
    path="/generate_aztec_code",
    summary="Generates an aztec code",
    response_class=StreamingResponse,
)
async def generate_actec(string: str):
    aztec_code = AztecCode(string, compact=False, ec_percent=50)
    image = aztec_code.image().resize([312, 312], resample=Image.NEAREST)
    img_io = BytesIO()
    image.save(img_io, "JPEG", quality=100)
    img_io.seek(0)
    return StreamingResponse(img_io, media_type="image/jpeg")
