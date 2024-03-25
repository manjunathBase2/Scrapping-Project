# import scrapy
# from scrapy.linkextractors import LinkExtractor
# import json

# class CancerGovSpider(scrapy.Spider):
#     name = 'cancer_gov_v5'
#     allowed_domains = ['www.cancer.gov']
#     start_urls = ['https://www.cancer.gov/about-website/sitemap']
#     visited_urls = set()
#     visited_titles = set()
#     visited_img_urls = set()

#     def parse(self, response):
#         # Extracting textual data from the page
#         title = response.css('title::text').get()
#         url = response.url
#         p_text = [t.strip() for t in response.css('p::text').getall()]
#         h1_texts = [t.strip() for t in response.css('h1::text').getall()]
#         h2_texts = [t.strip() for t in response.css('h2::text').getall()]
#         h3_texts = [t.strip() for t in response.css('h3::text').getall()]
#         dt_texts = [t.strip() for t in response.css('dt::text').getall()]
#         dd_texts = [t.strip() for t in response.css('dd::text').getall()]
#         content = p_text + h1_texts + h2_texts + h3_texts + dt_texts + dd_texts        

#         # Extracting textual data from the html
#         if 'espanol' not in url and '.pdf' not in url and '.docx' not in url and 'Spanish' not in url and url not in self.visited_urls and title not in self.visited_titles:
#             with open('scraped_data_v5.txt', 'a+', encoding='utf-8') as f:
#                 if title is not None:
#                     f.write(f"\nttle: {title}\n")
#                     self.visited_titles.add(title)
#                     f.write(f"@: {url}\n")
#                     self.visited_urls.add(url)
#                     f.write(f"txt: {' '.join(content)}\n")
#                     f.write(f"{'-'*50}\n")

#         # Writing URLs with .pdf into a JSON file
#         if '.pdf' in url:
#             # Create a dictionary with the PDF URL
#             pdf_url = {'PDF_URL': url}

#             # Write the PDF URL to the JSON file in append mode
#             with open('pdf_urls_v5.json', 'a', encoding='utf-8') as json_file:
#                 json.dump(pdf_url, json_file, ensure_ascii=False)
#                 json_file.write('\n')  # Add a newline character to separate entries

#         # Writing URLs with .docx into a JSON file
#         if '.docx' in url:
#             # Create a dictionary with the .docx URL
#             docx_url = {'DOCX_URL': url}

#             # Write the .docx URL to the JSON file in append mode
#             with open('docx_urls_v5.json', 'a', encoding='utf-8') as json_file:
#                 json.dump(docx_url, json_file, ensure_ascii=False)
#                 json_file.write('\n')  # Add a newline character to separate entries

#         # # Extracting img urls along with alt text into a dictionary
#         # img_urls = response.css('img::attr(src)').getall()
#         # img_alt_texts = response.css('img::attr(alt)').getall()

#         # # Convert relative URLs to absolute URLs
#         # img_urls = [response.urljoin(url) for url in img_urls]

#         # # add the visited img urls to the set
#         # self.visited_img_urls.update(img_urls)

#         # # Combine the img_urls only those that have alt text and are not logos and are not previously visited
#         # img_data = {img_urls[i]: img_alt_texts[i] for i in range(len(img_urls)) if img_alt_texts[i] and 'logo' not in img_alt_texts[i].lower() and img_urls[i] not in self.visited_img_urls and '.svg' not in img_urls[i]} 

#         # # Writing img URLs and alt texts into a JSON file in append mode
#         # with open('img_urls_v5.json', 'a+', encoding='utf-8') as json_file:
#         #     json.dump(img_data, json_file, ensure_ascii=False)
#         #     json_file.write('\n')  # Add a newline character to separate entries

#         sub_pages = response.css('a::attr(href)').getall()
#         sub_pages += response.css('link::attr(href)').getall()

#         # Convert relative URLs to absolute URLs
#         sub_pages = [response.urljoin(url) for url in sub_pages]

#         for sub_page_url in sub_pages:
#             if 'espanol' not in sub_page_url and '.pdf' not in sub_page_url and '.docx' not in sub_page_url and 'Spanish' not in sub_page_url and sub_page_url not in self.visited_urls:
#                 self.visited_urls.add(sub_page_url)
#                 self.visited_titles.add(title)
#                 yield response.follow(sub_page_url, callback=self.parse)
