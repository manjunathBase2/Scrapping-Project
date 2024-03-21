!apt-get install tesseract-ocr
!apt-get install tesseract-ocr-all
!pip install pytesseract

import requests
from PIL import Image
import pytesseract
from io import BytesIO
from bs4 import BeautifulSoup

# Set the Tesseract OCR executable path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def extract_text_from_image(image_url):
    try:
      if not image_url.startswith(('http://', 'https://')):
        image_url = 'https://www.cancer.gov/' + image_url
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for bad response status codes

        # Open the image using PIL
        img = Image.open(BytesIO(response.content))

        # Perform OCR on the image
        extracted_text = pytesseract.image_to_string(img)

        return extracted_text.strip()  # Strip whitespace from the extracted text

    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

def extract_image_text_from_webpage(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad response status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract image URLs and alt text
        images = soup.find_all('img')
        image_info = [(img['src'], img.get('alt', '')) for img in images]

        # Extract text from each image
        image_texts = {}
        for img_url, alt_text in image_info:
            extracted_text = extract_text_from_image(img_url)
            image_texts[img_url] = {'alt_text': alt_text, 'extracted_text': extracted_text}

        return image_texts

    except Exception as e:
        print(f"Error extracting image texts from webpage: {e}")
        return None

def save_image_texts_to_file(image_texts, filename='image_texts.txt'):
     try:
      from google.colab import drive
      drive.mount('/content/drive')
      with open('/content/drive/My Drive/image_texts.txt', 'w',encoding='utf-8') as file:
        for img_url, text_info in image_texts.items():
          alt_text = text_info['alt_text']
          extracted_text = text_info['extracted_text']
          file.write(f"Image URL: {img_url}\n")
          file.write(f"Alt Text: {alt_text}\n")
          file.write(f"Extracted Text: {extracted_text}\n")
          file.write("-" * 50 + "\n")
      print(f"Image texts saved to {filename} successfully.")
     except Exception as e:
        print(f"Error saving image texts to file: {e}")

url = 'https://www.cancer.gov/about-nci/budget' 
image_texts = extract_image_text_from_webpage(url)
if image_texts:
    save_image_texts_to_file(image_texts)
else:
    print("No image texts extracted.")
