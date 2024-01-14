# Python爬虫和数据分析大作业

## 1. 项目简介
从豆瓣电影网站抓取电影信息，进行文本处理和情感分析，并生成词云图。

## 2. 尝试与优化
### 2.1 尝试
刚开始着手这个作业时，是完全参照老师给出的实验手册进行代码编写，但是在一通操作后发现无法成功运行
#### _废弃的代码如下_
```bad_wordcloud.py```
```python
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

```

### 2.2 再次尝试
在多次修改“实验手册式”的程序无果后，我决定自己从头开始写，于是我先从豆瓣电影网站上抓取了一部分电影的信息，然后进行文本处理和情感分析，并生成词云图。
#### _这是已经可以满足所有基本要求并且可以正常运行的代码_
```better_wordcloud.py```
```python
import requests
from bs4 import BeautifulSoup
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class DoubanMovies:
    def __init__(self):
        self.url = "https://movie.douban.com/top250"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_movie_synopsis(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = soup.find_all('div', class_='info')
        with open('douban_movies.txt', 'w', encoding='utf-8') as f:
            for movie in movies:
                title = movie.find('span', class_='title').text
                synopsis = movie.find('span', class_='inq').text if movie.find('span', class_='inq') else ''
                f.write(title + ': ' + synopsis + '\n')

    def process_text(self):
        with open('douban_movies.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        keywords = jieba.analyse.extract_tags(text, topK=100, withWeight=True)
        with open('keywords.txt', 'w', encoding='utf-8') as f:
            for item in keywords:
                f.write(item[0] + '\n')

    def generate_wordcloud(self):
        with open('keywords.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        my_wordcloud = WordCloud(font_path='simhei.ttf').generate(text)
        plt.imshow(my_wordcloud)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    d = DoubanMovies()
    d.get_movie_synopsis()
    d.process_text()
    d.generate_wordcloud()
```

### 2.3 优化
完成better_wordcloud.py后，发现离ddl还有一周，而且感觉自己尚有余力，于是决定完善代码，让他满足实验手册上的“高要求”。
#### 修改优化的地方有：
###### 1.采用scrapy的爬取框架来实现数据获取。
###### 2.改进关键词提取方法，考虑使用TextRank算法，并对文本内容进行情感分析。
###### 3.改进词云图绘制方法，采用心型蒙版进行绘制。
#### _优化后的代码如下_
```best_wordcloud.py```
```python
import json
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from snownlp import SnowNLP

# 初始化logger
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class DoubanMoviesSpider(scrapy.Spider):
    name = "douban_movies"
    start_urls = ["https://movie.douban.com/top250"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    def parse(self, response):
        sel = scrapy.Selector(response)
        movies = sel.css('div.info')
        for movie in movies:
            title = movie.css('span.title::text').get()
            synopsis = movie.css('span.inq::text').get() or 'No synopsis provided'
            yield {'title': title, 'synopsis': synopsis}


class DoubanMovies:
    def __init__(self):
        self.process = CrawlerProcess(settings={
            "FEEDS": {
                "douban_movies.json": {"format": "json"},
            },
        })
        self.process.crawl(DoubanMoviesSpider)

    def get_movie_synopsis(self):
        self.process.start()
        self.process.join()

    def process_text(self):
        try:
            with open('douban_movies.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            text = '\n'.join([item['title'] + ': ' + item['synopsis'] for item in data])
            keywords = jieba.analyse.textrank(text, topK=100, withWeight=True)
            with open('keywords.txt', 'w', encoding='utf-8') as f:
                for item in keywords:
                    f.write(item[0] + '\n')
        except Exception as e:
            logger.error("Error occurred during text processing", exc_info=True)
            raise e

    def sentiment_analysis(self):
        try:
            with open('douban_movies.json', 'r', encoding='utf-8') as f, open('sentiment_analysis_result.txt', 'w',
                                                                              encoding='utf-8') as result_file:
                data = json.load(f)
                for item in data:
                    s = SnowNLP(item['synopsis'])
                    result_file.write(f"Title: {item['title']}, Sentiment: {s.sentiments}\n")
        except Exception as e:
            logger.error("Error occurred during sentiment analysis", exc_info=True)
            raise e

    def generate_wordcloud(self):
        try:
            mask = np.array(Image.open('heart.png')) if os.path.exists('heart.png') else None
            with open('keywords.txt', 'r', encoding='utf-8') as f:
                text = f.read()
            my_wordcloud = WordCloud(font_path='simhei.ttf', mask=mask, background_color='white').generate(text)
            image_colors = ImageColorGenerator(mask)
            plt.imshow(my_wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
            plt.axis("off")
            plt.show()
        except Exception as e:
            logger.error("Error occurred during word cloud generation", exc_info=True)
            raise e


if __name__ == "__main__":
    try:
        d = DoubanMovies()
        d.get_movie_synopsis()
        d.process_text()
        d.sentiment_analysis()
        d.generate_wordcloud()
    except Exception as e:
        logger.error("Error occurred in main", exc_info=True)
   ```

## 3. 数据入库
在上一步调试best_wordcloud的过程中，有一步是将情感分析的结果写入文件，而在结束编写后，我突然想到其实可以将这个数据写入数据库，正好把数据库的知识学以致用，于是我又写了一个新的功能
#### 首先在Python环境中安装`mysql-connector-python`库
```pip install mysql-connector-python```
#### 然后创建数据库连接，然后执行插入数据的SQL语句
```python
def save_to_database(title, sentiment):
    try:
        # 创建数据库连接
        cnx = mysql.connector.connect(user='root', password='5106',
                                      host='127.0.0.1',
                                      database='wordcloud')
        cursor = cnx.cursor()

        # 插入数据的SQL语句
        add_data = ("INSERT INTO sentiment_analysis (title, sentiment) "
                    "VALUES (%s, %s)")

        # 执行SQL语句
        cursor.execute(add_data, (title, sentiment))

        # 事务提交，确保数据被保存到数据库
        cnx.commit()

    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        # 关闭游标和连接
        cursor.close()
        cnx.close()
```
#### 最后在sentiment_analysis函数中调用这个函数
```python
# 调用save_to_database函数将情感分析结果保存到数据库
save_to_database(item['title'], float(s.sentiments))
```

### 4.最终成果
```Ultimate_wordcloud.py```
```python
import json
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from snownlp import SnowNLP

import mysql.connector


# 定义一个函数，将电影标题和情感分析结果保存到数据库
def save_to_database(title, sentiment):
    try:
        # 创建数据库连接
        cnx = mysql.connector.connect(user='root', password='5106',
                                      host='127.0.0.1',
                                      database='wordcloud')
        cursor = cnx.cursor()

        # 插入数据的SQL语句
        add_data = ("INSERT INTO sentiment_analysis (title, sentiment) "
                    "VALUES (%s, %s)")

        # 执行SQL语句
        cursor.execute(add_data, (title, sentiment))

        # 事务提交，确保数据被保存到数据库
        cnx.commit()

    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        # 关闭游标和连接
        cursor.close()
        cnx.close()


# 初始化logger
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# 定义一个Scrapy爬虫，用于抓取豆瓣电影信息
class DoubanMoviesSpider(scrapy.Spider):
    name = "douban_movies"

    # 生成所有页面的 URLs
    start_urls = [f"https://movie.douban.com/top250?start={i * 25}" for i in range(10)]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    def parse(self, response):
        sel = scrapy.Selector(response)
        movies = sel.css('div.info')
        for movie in movies:
            title = movie.css('span.title::text').get()
            synopsis = movie.css('span.inq::text').get() or 'No synopsis provided'
            yield {'title': title, 'synopsis': synopsis}


# 定义一个类，包含获取电影简介、处理文本、进行情感分析和生成词云的方法
class DoubanMovies:
    def __init__(self):
        self.process = CrawlerProcess(settings={
            "FEEDS": {
                "douban_movies.json": {"format": "json"},
            },
        })
        self.process.crawl(DoubanMoviesSpider)

    def get_movie_synopsis(self):
        self.process.start()
        self.process.join()

    def process_text(self):
        try:
            with open('douban_movies.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            text = '\n'.join([item['title'] + ': ' + item['synopsis'] for item in data])
            keywords = jieba.analyse.textrank(text, topK=100, withWeight=True)
            with open('keywords.txt', 'w', encoding='utf-8') as f:
                for item in keywords:
                    f.write(item[0] + '\n')
        except Exception as e:
            logger.error("Error occurred during text processing", exc_info=True)
            raise e

    def sentiment_analysis(self):
        try:
            with open('douban_movies.json', 'r', encoding='utf-8') as f, open('sentiment_analysis_result.txt', 'w',
                                                                              encoding='utf-8') as result_file:
                data = json.load(f)
                for item in data:
                    s = SnowNLP(item['synopsis'])
                    result_file.write(f"Title: {item['title']}, Sentiment: {s.sentiments}\n")
                    # 调用save_to_database函数将情感分析结果保存到数据库
                    save_to_database(item['title'], float(s.sentiments))
        except Exception as e:
            logger.error("Error occurred during sentiment analysis", exc_info=True)
            raise e

    def generate_wordcloud(self):
        try:
            mask = np.array(Image.open('heart.png')) if os.path.exists('heart.png') else None
            with open('keywords.txt', 'r', encoding='utf-8') as f:
                text = f.read()
            my_wordcloud = WordCloud(font_path='simhei.ttf', mask=mask, background_color='white').generate(text)
            image_colors = ImageColorGenerator(mask)
            plt.imshow(my_wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
            plt.axis("off")
            plt.show()
        except Exception as e:
            logger.error("Error occurred during word cloud generation", exc_info=True)
            raise e


# 主程序
if __name__ == "__main__":
    try:
        d = DoubanMovies()
        d.get_movie_synopsis()
        d.process_text()
        d.sentiment_analysis()
        d.generate_wordcloud()
    except Exception as e:
        logger.error("Error occurred in main", exc_info=True)
```
#### 运行结果:
_词云图如下：_
![wordcloud.png](wordcloud.png)
_数据库中的数据结果如下：_
![al_data.png](al_data.png)

### 完美结束

#### 注：本次作业所需的包放在requirements.txt中，可以通过以下命令安装
```pip install -r requirements.txt```