import scrapy
from scrapy.linkextractors import LinkExtractor
import PyPDF2
from docx import Document
from io import BytesIO
import pytesseract
from PIL import Image

class CancerGovSpider(scrapy.Spider):
    name = 'cancer_gov_v7'
    allowed_domains = ['www.cancer.gov']
    start_urls = ['https://www.cancer.gov/about-website/sitemap']
    visited_urls = set()
    visited_titles = set()

    def parse(self, response):
        # Extracting textual data from the page
        title = response.css('title::text').get()
        url = response.url

        # Extracting textual content from different types of files
        if '.pdf' in url:
            content = self.extract_text_from_pdf(response.body)
        elif '.docx' in url:
            content = self.extract_text_from_docx(response.body)
        else:
            p_text = [t.strip() for t in response.css('p::text').getall()]
            h1_texts = [t.strip() for t in response.css('h1::text').getall()]
            h2_texts = [t.strip() for t in response.css('h2::text').getall()]
            h3_texts = [t.strip() for t in response.css('h3::text').getall()]
            dt_texts = [t.strip() for t in response.css('dt::text').getall()]
            dd_texts = [t.strip() for t in response.css('dd::text').getall()]
            content = p_text + h1_texts + h2_texts + h3_texts + dt_texts + dd_texts        

        # Writing extracted data to file
        if 'espanol' not in url and url not in self.visited_urls and title not in self.visited_titles:
            with open('scraped_data_v7.txt', 'a+', encoding='utf-8') as f:
                if title is not None:
                    f.write(f"\ntitle: {title}\n")
                    self.visited_titles.add(title)
                    f.write(f"@: {url}\n")
                    self.visited_urls.add(url)
                    f.write(f"txt: {' '.join(content)}\n")
                    f.write(f"{'-'*50}\n")

        # Follow links
        sub_pages = response.css('a::attr(href)').getall()
        sub_pages += response.css('link::attr(href)').getall()

        # Convert relative URLs to absolute URLs
        sub_pages = [response.urljoin(url) for url in sub_pages]

        for sub_page_url in sub_pages:
            if 'espanol' not in sub_page_url and sub_page_url not in self.visited_urls:
                self.visited_urls.add(sub_page_url)
                self.visited_titles.add(title)
                yield response.follow(sub_page_url, callback=self.parse)

    def extract_text_from_pdf(self, pdf_data):
        text = []
        try:
            pdf_reader = PyPDF2.PdfFileReader(BytesIO(pdf_data))
            for page_num in range(pdf_reader.numPages):
                text.append(pdf_reader.getPage(page_num).extractText())
        except PyPDF2.utils.PdfReadError:
            print("Error reading PDF")
        return text

    def extract_text_from_docx(self, docx_data):
        text = []
        try:
            doc = Document(BytesIO(docx_data))
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
        except Exception as e:
            print("Error reading DOCX:", e)
        return text

    def extract_text_from_image(self, image_data):
        text = []
        try:
            image = Image.open(BytesIO(image_data))
            text = pytesseract.image_to_string(image)
        except Exception as e:
            print("Error reading image:", e)
        return text
