from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import shutil

from modules.pdf_extract import extract_pdf
from modules.summarization_model import run_summarization
from modules.translating_model import run_translation
from modules.write_to_pdf import create_formatted_pdf

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

TMP_DIR = "/tmp"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    input_path = os.path.join(TMP_DIR, file.filename)
    output_path = os.path.join(TMP_DIR, f"PIDGIN_{file.filename}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = await extract_pdf(file)
    summary = run_summarization(raw_text)
    pidgin = run_translation(summary)

    create_formatted_pdf(output_path, pidgin)

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"PIDGIN_{file.filename}"
    )
