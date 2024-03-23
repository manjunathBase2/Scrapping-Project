import scrapy
from bs4 import BeautifulSoup

class CancerGovSpider(scrapy.Spider):
    name = 'cancer_gov_v2'
    allowed_domains = ['www.cancer.gov']
    start_urls = ['https://www.cancer.gov/about-website/sitemap']
    visited_urls = set()
    visited_titles = set()

    def parse(self, response):
        url = response.url

        if url.lower().endswith('.xml'):
            # Extracting urls from sitemap.xml
            soup = BeautifulSoup(response.text, 'xml')
            urls = [loc.text.strip() for loc in soup.find_all('loc')]
            for url in urls:
                if url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url=url, callback=self.parse)
        else:
            # Extracting textual data from the page
            title = response.css('title::text').get()
            text = [t.strip() for t in response.css('p::text').getall()]
            dd_texts = [t.strip() for t in response.css('dd::text').getall()]

            # Save the data to a text file
            if 'espanol' not in url and '.pdf' not in url and '.docx' not in url and 'Spanish' not in url and url not in self.visited_urls and title not in self.visited_titles:
                with open('scraped_data_v2.txt', 'a', encoding='utf-8') as f:
                    if title is not None:
                        f.write(f"\ntitle: {title}\n")
                        self.visited_titles.add(title)
                        f.write(f"url: {url}\n")
                        self.visited_urls.add(url)
                        f.write(f"text: {' '.join(text + dd_texts)}\n")

            sub_pages = response.css('a::attr(href)').getall()
            for sub_page_url in sub_pages:
                if 'espanol' not in sub_page_url and '.pdf' not in sub_page_url and '.docx' not in sub_page_url and 'Spanish' not in sub_page_url and sub_page_url not in self.visited_urls:
                    self.visited_urls.add(sub_page_url)
                    self.visited_titles.add(title)
                    yield response.follow(sub_page_url, callback=self.parse)
