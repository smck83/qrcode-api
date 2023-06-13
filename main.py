import io
import qrcode

from fastapi import FastAPI
from starlette.responses import StreamingResponse

app = FastAPI()

@app.get("/generate-qr-code")
def generate(message: str):
    img = qrcode.make(message)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0) # important here!
    return StreamingResponse(buf, media_type="image/jpeg")