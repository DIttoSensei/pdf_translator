from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def create_formatted_pdf(output_path, final_text):
    # output_path will be something like "/tmp/result.pdf"
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    custom_style = ParagraphStyle(
        'LearningStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=10
    )
    
    story = []
    story.append(Paragraph("<b>TRANSLATED TEXT</b>", styles['Title']))
    story.append(Spacer(1, 20))
    
    # We turn the translated text into a paragraph
    p = Paragraph(final_text, custom_style)
    story.append(p)
        
    doc.build(story)