# pdf extraction
import requests
from PyPDF2 import PdfReader
from io import BytesIO

# Function to extract text from PDF
def extract_text_from_pdf(pdf_url):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_content = response.content
        pdf_reader = PdfReader(BytesIO(pdf_content))
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        return "Failed to download PDF"

# URL of the PDF to extract data from
pdf_url = "https://pdf.hres.ca/dpd_pm/00036917.PDF"

# Extract data from the PDF
pdf_text = extract_text_from_pdf(pdf_url)

# Print the extracted text
print(pdf_text)
output_file_path = "extracted_text.txt"
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(pdf_text)
