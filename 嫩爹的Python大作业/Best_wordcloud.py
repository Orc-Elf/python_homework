# 导入库
import requests
from bs4 import BeautifulSoup

import time

# 循环抓取
offset = 0
while True:
    print(f"请求第{offset + 1}到第{offset + 20 + 1}部电影的信息...")
    url = f"https://movie.douban.com/typerank?type_name=%E7%A7%91%E5%B9%BB&type=17&interval_id=100:90&action=&start=0&limit=20"

    # 设置请求头
    HEADER = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
    }

    # HTTP GET 请求获取JSON数据
    r = requests.get(url, headers=HEADER)
    movie_lists = r.json()

    # 如果返回的JSON数据为空，说明已经没有数据了，退出循环
    if len(movie_lists) == 0:
        break

    # 分析JSON数据，获取电影信息
    for movie in movie_lists:
        title = movie['title']
        url = movie['url']

        # 进入电影详情页
        r = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(r.text, 'html.parser')

        print(f"电影《{title}》的详情页请求成功，开始分析...")

        # 找到电影简介的HTML元素
        html_element = soup.select('')
