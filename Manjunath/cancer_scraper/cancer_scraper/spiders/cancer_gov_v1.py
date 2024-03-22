import scrapy

class CancerGovSpider(scrapy.Spider):
    name = 'cancer_gov_v1'
    allowed_domains = ['www.cancer.gov']
    start_urls = ['https://www.cancer.gov/about-cancer/causes-prevention/risk']

    def parse(self, response):
        # Extracting textual data from the homepage
        title = response.css('title::text').get()
        url = response.url
        text = response.css('p::text').getall()

        # Save the data to a text file
        with open('scraped_data_v2.txt', 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Text: {' '.join(text)}\n")

        sub_pages = response.css('a::attr(href)').getall()

        for sub_page in sub_pages:
            if 'espanol' in sub_page:
                continue
            yield response.follow(sub_page, callback=self.parse_subpage)

        self.log(f'Successfully scraped: {url}')

    def parse_subpage(self,response):

        # Extracting textual data from the homepage
        title = response.css('title::text').get()
        url = response.url
        text = response.css('p::text').getall()

        # Save the data to a text file
        with open('scraped_data_v1.txt', 'a', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Text: {' '.join(text)}\n")

        self.log(f'Successfully scraped: {url}')
        
