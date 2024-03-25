# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor

# class CancerGovSpider(CrawlSpider):
#     name = 'cancer_gov_v6'
#     allowed_domains = ['www.cancer.gov']
#     start_urls = ['https://www.cancer.gov/about-website/sitemap']
#     visited_urls = set()
#     visited_titles = set()

#     rules = (
#         Rule(LinkExtractor(deny=('(\.jpg|\.jpeg|\.png|\.gif|\.mp3|\.mp4|\.avi|\.pdf|\.docx)$',)), callback='parse_item', follow=True),
#     )

#     def parse_item(self, response):
#         # Extracting textual data from the page
#         title = response.css('title::text').get()
#         url = response.url
#         p_text = [t.strip() for t in response.css('p::text').getall()]
#         # h1_texts = [t.strip() for t in response.css('h1::text').getall()]
#         # h2_texts = [t.strip() for t in response.css('h2::text').getall()]
#         # h3_texts = [t.strip() for t in response.css('h3::text').getall()]
#         # dt_texts = [t.strip() for t in response.css('dt::text').getall()]
#         dd_texts = [t.strip() for t in response.css('dd::text').getall()]
#         content = p_text + dd_texts

#         # Extracting textual data from the html
#         if 'espanol' not in url and '.pdf' not in url and '.docx' not in url and 'Spanish' not in url and url not in self.visited_urls and title not in self.visited_titles:
#             with open('scraped_data_v6.txt', 'a+', encoding='utf-8') as f:
#                 if title is not None:
#                     f.write(f"\nttle: {title}\n")
#                     self.visited_titles.add(title)
#                     f.write(f"@: {url}\n")
#                     self.visited_urls.add(url)
#                     f.write(f"txt: {' '.join(content)}\n")
#                     f.write(f"{'-'*50}\n")

#         # Writing urls with .pdf into a text file
#         if '.pdf' in url:
#             with open('pdf_urls_v6.txt', 'a+', encoding='utf-8') as f:
#                 f.write(f"{url}\n")

#         # Writing urls with .docx into a text file
#         if '.docx' in url:
#             with open('docx_urls_v6.txt', 'a+', encoding='utf-8') as f:
#                 f.write(f"{url}\n")

#         # Extracting img urls along with alt text into a dictionary
#         # img_urls = response.css('img::attr(src)').getall()
#         # img_alt_texts = response.css('img::attr(alt)').getall()

#         # # Convert relative URLs to absolute URLs
#         # img_urls = [response.urljoin(url) for url in img_urls]

#         # # Writing img urls and alt texts into a json file
#         # img_dict = dict(zip(img_urls, img_alt_texts))
#         # with open('img_urls_v6.json', 'a+', encoding='utf-8') as f:
#         #     f.write(str(img_dict))
