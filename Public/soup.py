from urllib.request import urlopen
from bs4 import BeautifulSoup

text = urlopen('https://python.org/jobs').read()
soup = BeautifulSoup(text, 'html.parser')  # 实例化BeautifulSoup类
jobs = set()
for job in soup.body.section('h2'):  # 调用返回文档body中第一个                                               #section包含的所有h2元素
    jobs.add('{}({}) '.format(job.a.string, job.a[
        'href']))  # 每个h2                             # 元素的第一个链接job.a是我们关注的职位的url; # job.a.string是链接的文本内容，job.a['href']为属性的值
print('\n'.join(sorted(jobs, key=str.lower)))
