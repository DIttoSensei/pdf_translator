from pypdf import PdfReader
import io

# We now pass the 'file' object from FastAPI into this function
async def extract_pdf(upload_file):
    # 1. Read the file into memory (so we don't need to save to disk)
    content = await upload_file.read()
    pdf_stream = io.BytesIO(content)
    
    # 2. Pass the memory stream to PdfReader
    reader = PdfReader(pdf_stream)

    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text() + "\n"

    # We return the text instead of writing a .txt file
    # This keeps the data moving through the 'pipeline'
    return all_text