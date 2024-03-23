import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class CancerGovSpider(scrapy.Spider):
    name = 'cancer_gov_v3'
    allowed_domains = ['www.cancer.gov']
    start_urls = ['https://www.cancer.gov/about-website/sitemap']
    visited_urls = set()

    def parse(self, response):
        url = response.url

        if response.status != 200:
            self.logger.error(f"Failed to fetch {url}: Status code {response.status}")
            return

        if url.lower().endswith('.xml'):
            # Extracting URLs from sitemap.xml
            soup = BeautifulSoup(response.text, 'xml')
            urls = [loc.text.strip() for loc in soup.find_all('loc')]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            # Extracting textual data from the page
            title = response.css('title::text').get()
            text = response.css('p::text').getall()
            dd_texts = response.css('dd::text').getall()

            # Save the data to a text file
            if self.should_process_url(url, title):
                with open('scraped_data_v3.txt', 'a', encoding='utf-8') as f:
                    f.write(f"\ntitle: {title}\n")
                    f.write(f"url: {url}\n")
                    f.write(f"text: {' '.join(text + dd_texts)}\n")
                self.visited_urls.add(url)

            # Extract and follow links
            for sub_page_url in response.css('a::attr(href)').getall():
                absolute_url = response.urljoin(sub_page_url)
                if self.should_follow_url(absolute_url):
                    yield scrapy.Request(absolute_url, callback=self.parse)

    def should_process_url(self, url, title):
        if any(keyword in url.lower() for keyword in ['espanol', '.pdf', '.docx', 'spanish']):
            return False
        if url in self.visited_urls:
            return False
        if not title:
            return False
        return True

    def should_follow_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ['http', 'https']:
            return False
        if parsed_url.netloc not in self.allowed_domains:
            return False
        if url in self.visited_urls:
            return False
        return True
