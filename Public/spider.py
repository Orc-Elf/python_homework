import requests
from bs4 import BeautifulSoup

ua = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
        'Safari/537.36'
}

url = 'https://search.bilibili.com/all?keyword=python&from_source=webtop_search&spm_id_from=333.1007&search_source=5'
r = requests.get(url, headers=ua)

print(r.status_code)
# soup = BeautifulSoup(r.text, 'html.parser')
