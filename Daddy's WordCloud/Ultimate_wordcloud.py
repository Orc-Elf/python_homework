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
