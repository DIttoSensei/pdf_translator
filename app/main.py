from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import shutil

# Import serverless-safe modules
from .modules.pdf_extract import extract_pdf_from_path
from .modules.summarization_model import run_summarization
from .modules.translating_model import run_translation
from .modules.write_to_pdf import create_formatted_pdf

app = FastAPI()

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TMP_DIR = "/tmp"

# Templates
if not os.path.exists(TEMPLATES_DIR):
    raise RuntimeError("Templates folder missing!")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Static files
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse(os.path.join(BASE_DIR, "favicon.ico"))

@app.get("/apple-touch-icon.png")
async def get_apple_touch_icon():
    return FileResponse(os.path.join(BASE_DIR, "apple-touch-icon.png"))

@app.get("/favicon-16x16.png")
async def get_favicon_16():
    return FileResponse(os.path.join(BASE_DIR, "favicon-16x16.png"))

@app.get("/favicon-32x32.png")
async def get_favicon_32():
    return FileResponse(os.path.join(BASE_DIR, "favicon-32x32.png"))

@app.get("/site.webmanifest")
async def get_manifest():
    return FileResponse(os.path.join(BASE_DIR, "site.webmanifest"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    input_path = os.path.join(TMP_DIR, file.filename)
    output_path = os.path.join(TMP_DIR, f"PIDGIN_{file.filename}")

    # Save uploaded PDF to /tmp
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {e}")

    # Extract text
    try:
        raw_text = await extract_pdf_from_path(input_path)
        if not raw_text.strip():
            raise ValueError("PDF contains no extractable text")
    except Exception as e:
        print("PDF Extraction Failed:", e)
        raise HTTPException(status_code=500, detail=f"PDF extraction failed: {e}")

    # Summarize
    try:
        summary = run_summarization(raw_text)
    except Exception as e:
        print("Summarization Failed:", e)
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

    # Translate
    try:
        pidgin_text = run_translation(summary)
    except Exception as e:
        print("Translation Failed:", e)
        raise HTTPException(status_code=500, detail=f"Translation failed: {e}")

    # Generate PDF
    try:
        create_formatted_pdf(output_path, pidgin_text)
    except Exception as e:
        print("PDF Generation Failed:", e)
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

    # Return final PDF
    return FileResponse(
        path=output_path,
        filename=f"PIDGIN_{file.filename}",
        media_type="application/pdf"
    )
