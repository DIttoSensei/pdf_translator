from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import shutil

# Relative imports for serverless-safe modules
from .modules.pdf_extract import extract_pdf
from .modules.summarization_model import run_summarization
from .modules.translating_model import run_translation
from .modules.write_to_pdf import create_formatted_pdf

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure templates folder exists
if not os.path.exists(TEMPLATES_DIR):
    raise RuntimeError("Templates folder missing!")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Only mount static if folder exists
if os.path.exists(STATIC_DIR):
    from fastapi.staticfiles import StaticFiles
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

TMP_DIR = "/tmp"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    input_path = os.path.join(TMP_DIR, file.filename)
    output_path = os.path.join(TMP_DIR, f"PIDGIN_{file.filename}")

    # Save uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Rewind file pointer for reading
    await file.seek(0)

    try:
        # Extract text (async-safe)
        raw_text = await extract_pdf(file)  # Your pdf_extract.py uses async
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF extraction failed: {e}")

    # Summarize (inside function to avoid cold-start import crash)
    try:
        summary = run_summarization(raw_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

    # Translate
    try:
        pidgin_text = run_translation(summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {e}")

    # Create PDF
    try:
        create_formatted_pdf(output_path, pidgin_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

    # Return PDF file
    return FileResponse(
        path=output_path,
        filename=f"PIDGIN_{file.filename}",
        media_type="application/pdf"
    )
