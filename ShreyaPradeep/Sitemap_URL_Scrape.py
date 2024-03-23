#this is a more optmized and better code
import requests
from bs4 import BeautifulSoup

def extract_urls_from_xml(urls):
  normal_urls = set()
  pdf_urls = set()
  docx_urls = set()
  for i in urls:
    response = requests.get(i)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')
        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if url.lower().endswith('.pdf'):
                pdf_urls.add(url)
            elif url.lower().endswith('.docx'):
                docx_urls.add(url)
            else:
                normal_urls.add(url)

  return normal_urls, pdf_urls, docx_urls
url = "https://www.cancer.gov/sitemap.xml"
urls = []
response = requests.get(url)
if response.status_code == 200:
  soup = BeautifulSoup(response.content, 'xml')
  loc_tags = soup.find_all('loc')
  urls = [loc.text for loc in loc_tags]
extract_urls_from_xml(urls)


'''import requests
from bs4 import BeautifulSoup

def extract_urls_from_xml(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')  
        normal_urls = set()
        pdf_urls = set()
        docx_urls = set()

        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if url.lower().endswith('.pdf'):
                pdf_urls.add(url)
            elif url.lower().endswith('.docx'):
                docx_urls.add(url)
            else:
                normal_urls.add(url)

        return normal_urls, pdf_urls, docx_urls
    else:
        print("Failed to fetch the page:", response.status_code)
        return set(), set(), set()

#change sitemap url here
url = "https://www.cancer.gov/nano/sitemap.xml"
normal_urls, pdf_urls, docx_urls = extract_urls_from_xml(url)

print("Normal URLs:")
for url in normal_urls:
    print(url)

print("\nPDF URLs:")
for url in pdf_urls:
    print(url)

print("\nDOCX URLs:")
for url in docx_urls:
    print(url)
    '''




