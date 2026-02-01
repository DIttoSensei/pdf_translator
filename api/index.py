from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import tempfile

# Import your custom functions
from modules.pdf_extract import extract_pdf
from modules.summarization_model import run_summarization
from modules.translating_model import run_translation
from modules.write_to_pdf import create_formatted_pdf

app = FastAPI()

# NO @app.get("/") here. Vercel handles that via vercel.json

@app.post("/api/process")
async def handle_pdf_logic(file: UploadFile = File(...)):
    temp_dir = "/tmp"
    input_path = os.path.join(temp_dir, file.filename)
    output_path = os.path.join(temp_dir, f"PIDGIN_{file.filename}")


    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        await file.seek(0)

        # The Processing Chain
        raw_text = await extract_pdf(file) 
        summary = run_summarization(raw_text)
        pidgin_text = run_translation(summary)
        create_formatted_pdf(output_path, pidgin_text)

        return FileResponse(
            path=output_path, 
            filename=f"PIDGIN_{file.filename}",
            media_type='application/pdf'
        )

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))