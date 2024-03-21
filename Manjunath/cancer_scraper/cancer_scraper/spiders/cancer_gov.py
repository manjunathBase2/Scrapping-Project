import scrapy

class CancerGovSpider(scrapy.Spider):
    name = 'cancer_gov'
    allowed_domains = ['www.cancer.gov']
    start_urls = ['https://www.cancer.gov/']

    def parse(self, response):
        # Extracting textual data from the homepage
        data = {
            'url': response.url,
            'title': response.xpath('//title/text()').get(),
            'text': ' '.join(response.xpath('//text()').getall()).strip()
        }

        # Save the data to a text file
        with open('scraped_data.txt', 'w', encoding='utf-8') as f:
            f.write(f"URL: {data['url']}\n")
            f.write(f"Title: {data['title']}\n")
            f.write(f"Text: {data['text']}\n")
