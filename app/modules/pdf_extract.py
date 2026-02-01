from pypdf import PdfReader
import io

async def extract_pdf(upload_file):
    content = await upload_file.read()
    pdf_stream = io.BytesIO(content)
    reader = PdfReader(pdf_stream)
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"
    return all_text
