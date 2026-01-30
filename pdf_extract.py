# importing required modules
from pypdf import PdfReader

# creating a pdf reader object
reader = PdfReader('testing.pdf')

# printing number of pages in pdf file
#print(len(reader.pages))

all_text = ""
for page in reader.pages:
    all_text += page.extract_text() + "\n" # Add a newline between pages

with open("extracted.txt", 'w') as file:
    file.write(all_text)
    print("Text extracted and saved to extracted.txt")