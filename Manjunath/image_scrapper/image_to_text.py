import requests
from PIL import Image
import pytesseract
from io import BytesIO
!apt-get install tesseract-ocr
!apt-get install tesseract-ocr-all
!pip install pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
def image_text(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        extracted_text = pytesseract.image_to_string(img)
        return extracted_text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

info=image_text('https://www.cancer.gov/sites/g/files/xnrzdm211/files/styles/cgov_article/public/cgov_contextual_image/2020-02/how-nci-receives-funding.jpg?h=e2108550&itok=yXXWAZKY')
print(info)