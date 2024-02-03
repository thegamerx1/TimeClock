from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse

from aztec_code_generator import AztecCode
import qrcode

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


@router.get(
    path="/generate_qr",
    summary="Generates a QR code",
    response_class=StreamingResponse,
)
async def generate_qr(string: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=2,
    )
    qr.add_data(string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    image = img.resize([312, 312], resample=Image.NEAREST)
    img_io = BytesIO()
    image.save(img_io, "JPEG", quality=100)
    img_io.seek(0)
    return StreamingResponse(img_io, media_type="image/jpeg")
