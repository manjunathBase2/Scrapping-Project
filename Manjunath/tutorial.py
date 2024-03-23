import scrapy


class TutorialSpider(scrapy.Spider):
    name = "tutorial"
    allowed_domains = ["www.cancer.gov"]
    start_urls = ["https://www.cancer.gov"]

    def parse(self, response):
        pass
