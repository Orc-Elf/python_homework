# 导入库
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path
import jieba.analyse
import wordcloud

# 设置请求头
HEADER = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}


# 循环抓取
def fetch_movie_info(offset=0):
    print(f"请求第{offset + 1}到第{offset + 20 + 1}部电影的信息...")
    url = f"https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action=&start={offset}&limit=20"

    # HTTP GET 请求获取JSON数据
    r = requests.get(url, headers=HEADER)
    movie_lists = r.json()

    # 如果返回的JSON数据为空，说明已经没有数据了，退出循环
    if len(movie_lists) == 0:
        return

    # 分析JSON数据，获取电影信息
    for movie in movie_lists:
        title = movie['title']
        url = movie['url']

        # 进入电影详情页
        r = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(r.text, 'html.parser')

        print(f"电影《{title}》的详情页请求成功，开始分析...")

        # 找到电影简介的HTML元素
        html_element_list = soup.select('#link-report-intra > span.all.hidden')
        if len(html_element_list) == 0:
            html_element_list = soup.select('#link_report_intra')

        e = html_element_list[0]
        # 写入文件
        with open(title + '.txt', 'w', encoding='utf-8') as f:
            f.write(e.get_text())

    offset += 20
    time.sleep(3)


def generate_wordcloud():
    movie_lists = Path('./').glob('*.txt')

    keywords = []

    for movie in movie_lists:
        with open(movie, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace('\n', '')
            content = content.replace(' ', '')
            content = content.replace('　', '')
            content = content.replace('©豆瓣', '')

            keywords += jieba.analyse.extract_tags(content, withWeight=True)

    result = {}

    for key, value in keywords:
        # 如果关键词已经在字典中，累加权重
        if key in result:
            result[key] += value
        else:
            result[key] = value

    # 倒序排列
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)

    # 加载自定义字典
    jieba.load_userdict('user_words.txt')

    # 设置停用字典
    jieba.analyse.set_stop_words('stop_words.txt')

    # 生成词云
    # 中文字体路径，默认使用 Windows 下的仿宋字体
    font_path = 'C:\Windows\Fonts\simfang.ttf'

    # 设置字体路径，宽800高600并且仅显示50个词
    ws = wordcloud.WordCloud(font_path=font_path, width=800, height=600, max_words=50)

    # 生成词云
    ws.fit_words(result)

    # 将词云存入图片
    ws.to_file('wordcloud.png')


# 主程序
if __name__ == "__main__":
    for i in range(10):  # 抓取10页电影信息
        fetch_movie_info(i * 20)
    generate_wordcloud()
