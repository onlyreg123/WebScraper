import os
import requests
import string
from bs4 import BeautifulSoup

LINK_BASE = "https://www.nature.com"
LINK = LINK_BASE + "/nature/articles/?searchType=journalSearch&sort=PubDate&page="
# LINK = "https://www.nature.com/articles/d41586-021-01540-8"
# https://www.nature.com/nature/articles/?searchType=journalSearch&sort=PubDate&page=3
# Research Highlight


def prepare_string(s):
    out = s.translate(str.maketrans(' ', '_', string.punctuation))
    return out


def save_article(title, descr, page):
    path = ".//" + "Page_" + str(page)
    new_title = prepare_string(title) + ".txt"
    full_tittle = os.path.join(path, new_title)
    with open(full_tittle, "wb") as file:
        file.write(bytes(descr, encoding='utf-8'))


def get_art_details(href):
    r = requests.get(href)
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify())
    div = soup.find("div", class_=["c-article-body u-clearfix", "article-item__body"])
    details = ""

    for d in div:
        if d == "\n":
            continue
        details += d.text

    return details

def nature(page, type):
    r = requests.get(LINK + str(page))
    count = 0
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')

        count += 1
        a = soup.find_all("article")
        for article in a:
            if len(article.text) > 1:
                tipo = article.find(attrs={"data-test": "article.type"}).text.strip()
                if tipo.lower() != type:
                    continue
                art_detail = article.find("a", attrs={"data-track-action": "view article"})
                title = art_detail.text.strip()
                href = LINK_BASE + art_detail.get("href")
                descr = get_art_details(href)
                save_article(title, descr, page)
                count += 1


if __name__ == "__main__":
    pages = int(input())
    art_type = input().lower()
    # pages = 1
    # art_type = "research highlight"
    for page in range(1, pages + 1):
        path = ".//" + "Page_" + str(page)
        if not os.path.exists(path):
            os.mkdir(path)
        nature(page, art_type)


""" VERSION 1
request = get("https://www.nature.com/nature/articles")
soup = BeautifulSoup(request.content, 'html.parser')
saved_list = []

for x in soup.find_all('article'):
    news_type = x.find('span', {'data-test': 'article.type'}).text
    
    if news_type == '\nNews\n':
        topic = x.find('a', {'data-track-action': "view article"})
        name = topic.text.strip(' ').translate(str.maketrans("", "", punctuation)).replace(' ', '_') + '.txt'
        saved_list.append(name)
        
        article = get("https://www.nature.com" + topic.get('href'))
        s = BeautifulSoup(article.content, 'html.parser')

        file = open(name, 'w')
        file.write(s.find('div', {'class': 'c-article-body'}).text)
        file.close()

print('Saved articles', saved_list)
"""

"""  VERSION 2
def get_soup(url):
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    return BeautifulSoup(r.content, 'html.parser')


soup = get_soup('https://www.nature.com/nature/articles')
articles = soup.find_all('article')

news_article = list(filter(lambda article: article.find('span', {'class': 'c-meta__type'}).text == 'News', articles))

for na in news_article:
    header = na.find('h3')
    article_path = header.a.get('href')
    heading = header.a.text.strip()
    file_name = heading.translate(str.maketrans(dict.fromkeys(string.punctuation)))
    file_name = file_name.replace(' ', '_')

    article_url = 'https://www.nature.com' + article_path
    article_soup = get_soup(article_url)
    article_main = article_soup.find('div', {'class': 'c-article-body u-clearfix'})

    with open(file_name + '.txt', 'wb') as afile:
        afile.write(article_main.text.encode())
"""
