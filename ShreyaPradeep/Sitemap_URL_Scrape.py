import requests
from bs4 import BeautifulSoup

def extract_urls_from_xml(urls,normal_urls,pdf_urls,docx_urls,pptx_urls, xlxs_urls,vid_urls):
  for i in urls:
    response = requests.get(i)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')
        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if 'espanol' not in url:
              if url.lower().endswith('.pdf'):
                pdf_urls.add(url)
              elif url.lower().endswith('.docx'):
                docx_urls.add(url)
              elif url.lower().endswith('.pptx'):
                pptx_urls.add(url)
              elif url.lower().endswith('.xlsx'):
                xlxs_urls.add(url)
              elif 'video' in url.lower() or url.lower().endswith(".mp4"):
                vid_urls.add(url)
              else:
                normal_urls.add(url)
  print(len(normal_urls))
  #return normal_urls, pdf_urls, docx_urls

url = "https://www.cancer.gov/sitemap.xml"
urls = []
normal_urls = set()
pdf_urls = set()
docx_urls = set()
xlxs_urls=set()
pptx_urls=set()
vid_urls=set()
response = requests.get(url)
if response.status_code == 200:
  soup = BeautifulSoup(response.content, 'xml')
  loc_tags = soup.find_all('loc')
  urls = [loc.text for loc in loc_tags]

print(len(urls))
extract_urls_from_xml(urls,normal_urls,pdf_urls,docx_urls,pptx_urls, xlxs_urls,vid_urls)

