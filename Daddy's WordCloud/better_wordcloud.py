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
