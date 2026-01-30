from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT


text = """"""
with open ('translated.txt', 'r') as file:
    text = file.read()

def create_formatted_pdf(filename, content_list):
    # 1. Create the document container
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # 2. Define a custom style for your learning notes
    custom_style = ParagraphStyle(
        'LearningStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14, # Space between lines
        alignment=TA_LEFT,
        spaceAfter=10
    )
    
    # 3. Build the "Story" (the list of elements in the PDF)
    story = []
    
    # Add a Header
    story.append(Paragraph("<b>TRANSLATED TEXT</b>", styles['Title']))
    story.append(Spacer(1, 20)) # 20 points of empty space
    
    # Add your strings
    for text in content_list:
        # Check if the string should be a sub-header or body
        if text.isupper():
            p = Paragraph(f"<b>{text}</b>", styles['Heading2'])
        else:
            p = Paragraph(text, custom_style)
        
        story.append(p)
        story.append(Spacer(1, 6)) # Small gap between paragraphs
        
    # 4. Generate the PDF
    doc.build(story)

# --- Usage Example ---
my_strings = [
    text
]

create_formatted_pdf("TRANSLATED.pdf", my_strings)
print("PDF 'TRANSLATED.pdf' created successfully.")