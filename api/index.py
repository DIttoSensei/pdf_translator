from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import os
import shutil
import tempfile

# Import your custom functions from the modules folder
from modules.pdf_extract import extract_pdf
from modules.summarization_model import run_summarization
from modules.translating_model import run_translation
from modules.write_to_pdf import create_formatted_pdf

app = FastAPI()

# This helps find your public folder even if you run from different spots
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(BASE_DIR, "public", "index.html")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open(HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>404: Frontend not found</h1><p>Check if public/index.html exists.</p>"

@app.post("/api/process")
async def handle_pdf_logic(file: UploadFile = File(...)):
    # This finds the "temp" folder on Windows OR Linux automatically
    temp_dir = tempfile.gettempdir() 
    
    input_path = os.path.join(temp_dir, file.filename)
    output_path = os.path.join(temp_dir, f"TRANSLATED_{file.filename}")

    try:
        # 1. Save the uploaded file temporarily to the temp folder
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. RESET the file pointer 
        # (Needed because shutil.copyfileobj moved it to the end)
        await file.seek(0)

        # 3. The Assembly Line
        # Step A: Extract Text
        raw_text = await extract_pdf(file) 
        
        # Step B: Summarize (Calls Hugging Face)
        summary = run_summarization(raw_text)
        
        # Step C: Translate (Calls Hugging Face)
        pidgin_text = run_translation(summary)
        
        # Step D: Create PDF (Uses ReportLab)
        create_formatted_pdf(output_path, pidgin_text)

        # 4. Return the finished PDF to the user's browser
        return FileResponse(
            path=output_path, 
            filename=f"PIDGIN_{file.filename}",
            media_type='application/pdf'
        )

    except Exception as e:
        # This will show you exactly what went wrong in the terminal
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))