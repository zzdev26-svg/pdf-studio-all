"""PDF -> Markdown conversion service, single endpoint + single static page."""

import tempfile
from pathlib import Path

import pymupdf4llm
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB

app = FastAPI(title="PDF Studio")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/ads.txt")
def ads_txt():
    return FileResponse(STATIC_DIR / "ads.txt")


@app.post("/api/convert")
async def convert(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="El PDF supera el tamaño máximo permitido (25 MB).")

    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp.flush()
        try:
            markdown = pymupdf4llm.to_markdown(tmp.name)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"No se pudo convertir el PDF: {exc}") from exc

    return {"filename": file.filename, "markdown": markdown}
