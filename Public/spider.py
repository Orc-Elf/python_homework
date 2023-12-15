import requests
from bs4 import BeautifulSoup

url = 'https://search.bilibili.com/all?keyword=python&from_source=webtop_search&spm_id_from=333.1007&search_source=5'
r = requests.get(url)

print(r.status_code)
# soup = BeautifulSoup(r.text, 'html.parser')
