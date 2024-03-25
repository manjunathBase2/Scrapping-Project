# import scrapy
# from bs4 import BeautifulSoup
# import requests
# from bs4 import BeautifulSoup
# import requests
# from PyPDF2 import PdfReader
# from io import BytesIO

# class CancerGovSpider(scrapy.Spider):
#     name = 'cancer_gov_v2'
#     allowed_domains = ['www.cancer.gov']
#     start_urls = ['https://www.cancer.gov/about-website/sitemap']
#     visited_urls = set()
#     visited_titles = set()

#     def extract_text_from_pdf(pdf_urls):
#         extracted_text = ""
#         for pdf_url in pdf_urls:
#             response = requests.get(pdf_url)
#             if response.status_code == 200:
#                 pdf_content = response.content
#                 pdf_reader = PdfReader(BytesIO(pdf_content))
#                 text = ''
#                 for page in pdf_reader.pages:
#                     text += page.extract_text()
#                 extracted_text += f"\n@: {pdf_url}\n" + f"txt: {text}\n"
#             else:
#                 print("Failed to download PDF")
#         return extracted_text

#     def parse(self, response):
#         # Extracting textual data from the page
#         title = response.css('title::text').get()
#         url = response.url
#         text = [t.strip() for t in response.css('p::text').getall()]
#         dd_texts = [t.strip() for t in response.css('dd::text').getall()]
        

#         # Extracting textual data from the html
#         if 'espanol' not in url and '.pdf' not in url and '.docx' not in url and 'Spanish' not in url and url not in self.visited_urls and title not in self.visited_titles:
#             with open('scraped_data_v2.txt', 'a', encoding='utf-8') as f:
#                 if title is not None:
#                     f.write(f"\nttle: {title}\n")
#                     self.visited_titles.add(title)
#                     f.write(f"@: {url}\n")
#                     self.visited_urls.add(url)
#                     f.write(f"txt: {' '.join(text + dd_texts)}\n")
#                     f.write(f"{'-'*50}\n")

#         # Extracting textual data from the pdf
#         if '.pdf' in url:
#             pdf_text = CancerGovSpider.extract_text_from_pdf([url])
#             with open('scraped_data_v2.txt', 'a', encoding='utf-8') as f:
#                 f.write(f"@: {url}\n")
#                 self.visited_urls.add(url)
#                 f.write(f"txt: {pdf_text}\n")
#                 f.write(f"{'-'*50}\n")

        
#         sub_pages = response.css('a::attr(href)').getall()
#         sub_pages += response.css('link::attr(href)').getall()

#         # Convert relative URLs to absolute URLs
#         sub_pages = [response.urljoin(url) for url in sub_pages]

#         for sub_page_url in sub_pages:
#             if 'espanol' not in sub_page_url and '.pdf' not in sub_page_url and '.docx' not in sub_page_url and 'Spanish' not in sub_page_url and sub_page_url not in self.visited_urls:
#                 self.visited_urls.add(sub_page_url)
#                 self.visited_titles.add(title)
#                 yield response.follow(sub_page_url, callback=self.parse)
