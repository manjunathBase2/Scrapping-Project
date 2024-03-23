import requests
from bs4 import BeautifulSoup

def scrape_page(url, visited_titles):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.title
        if title_tag:
            title = title_tag.string.strip()
            if title not in visited_titles:
                visited_titles.add(title)
                return soup
        return None  
    except requests.exceptions.RequestException as e:
        print("Failed to fetch the page:", e)
        return None

def extract_text_from_tag(tag):
    if tag.name == 'p' or tag.name == 'li':
        return tag.get_text().strip()
    elif tag.name == 'ol' or tag.name == 'ul':
        return ' '.join([extract_text_from_tag(child) for child in tag.children])
    else:
        return ''

def extract_info(soup, url):
    if soup:
        # Extracting title
        title = soup.title.string.strip() if soup.title else "No title available"
        '''if title not in visited_titles :
          visited_urls.add(url_to_scrape)'''
        # Extracting URL
        page_url = url
        
        # Extracting mixed content from paragraph and list tags
        text_content = soup.find_all(['p', 'ol', 'ul'])
        info = ' '.join([extract_text_from_tag(tag) for tag in text_content])
        
        return {'title': title, 'url': page_url, 'info': info}
    else:
        return None
      
visited_urls = set()
visited_titles = set()
num_requests = 10
sleep_time = 2 

from google.colab import drive
drive.mount('/content/drive')
with open('/content/drive/My Drive/web_scrape.txt', 'w',encoding='utf-8') as file:
  for _ in range(num_requests):
    for url_to_scrape in normal_urls :
      if url_to_scrape not in visited_urls:
        visited_urls.add(url_to_scrape)
        soup = scrape_page(url_to_scrape,visited_titles)
        if soup:
          scraped_info = extract_info(soup, url_to_scrape)
          if scraped_info:
            title=scraped_info['title']
            data=scraped_info['info']
            file.write(f"T!tle : {title}\n")
            file.write(f"ur$ : {url_to_scrape}\n")
            file.write(f"d@t@ : {data}\n")
            file.write("-" * 50 + "\n")
        else:
            print("No information extracted.")
      else:
          print("Scraping failed. Check the URL and try again.")
    time.sleep(sleep_time)
