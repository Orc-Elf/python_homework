# encoding: utf-8
# @Time: 2023/12/14  23:32
# @Author: Jing Zhou
# @Module: BilibiliSpider
# @Contact: zhoujing@cuc.edu.cn
# @Software: PyCharm
# @User: zhouj

import requests
from bs4 import BeautifulSoup

ua = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
        'Safari/537.36'
}

r = requests.get('https://search.bilibili.com/all?keyword=python', headers=ua)

soup = BeautifulSoup(r.text, 'html.parser')  # 构建BeautifulSoup对象

# 利用CSS选择器得到所有视频的信息
sel_front = ('#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > '
             'div.video.i_wrapper.search-all-list > div > div:nth-child(')

sel_rear = ') > div > div.bili-video-card__wrap.__scale-wrap > div > div'

result = []

for i in range(30):

    addr = sel_front + str(i + 1) + sel_rear
    video_list = soup.select(addr)

    # print(video_list)
    for video in video_list:
        video_info = {}

        element = video.select('a')  # 显示标题
        video_info['title'] = str(i + 1) + ":" + element[0].text
        print(video_info['title'])

        element = video.select('a')
        video_info['url'] = element[0]['href']
        #   print(video_info['url'])

        element = video.select('p > a > span.bili-video-card__info--author')  # 显示作者
        video_info['author'] = element[0].text
        #   print(video_info['author'])

        element = video.select('p > a > span.bili-video-card__info--date')  # 显示时间

        if len(element) == 0:
            video_info['date'] = 'n/a'
            element = video.select('p > a > span.bili-video-card__info--cheese_episode_count')
            if len(element) == 0:
                video_info['update'] = 'n/a'
            else:
                video_info['update'] = element[0].text
        else:
            video_info["date"] = element[0].text
        #   print(video_info['date'])

        result.append(video_info)

print(result)
