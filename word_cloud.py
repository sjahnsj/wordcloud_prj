from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from konlpy.tag import Twitter
from collections import Counter

import matplotlib.pyplot as plt
from wordcloud import STOPWORDS
from PIL import Image
import numpy as np
import time

# from konlpy.tag import Okt


# url = "https://search.naver.com/search.naver?where=news&ie=utf8&sm=tab_jum&query={}&&start={}".format(search_word , start_num)

search_word = "2024년 총선"
title_list = []
start_num = 1
max_news = 191
cnt = 1
while True:
    if start_num > max_news:
        break

    url = f"https://search.naver.com/search.naver?where=news&ie=utf8&sm=tab_jum&query={search_word}&&start={start_num}"
    req = requests.get(url)
    time.sleep(1)

    if req.ok:
        html = req.text
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        # 뉴스 타이틀 뽑기
        # titles = soup.select("ul.list_news > li > div > div > div> a:nth-of-type(2)")
        titles = soup.select("a.news_tit")
        # print(titles[0].get_text())
        for title in titles:
            # print(title.get_text())
            print(f"---{cnt}---")
            cnt += 1
            title_list.append(title.get_text())

    start_num += 10
print("--------------------------------------------------------")
print(len(title_list))
print(title_list)

twitter = Twitter()
# twitter = Okt()

# twitter함수를 통해 읽어들인 내용의 형태소를 분석한다.
sentences_tag = []
sentences_tag = twitter.pos("".join(title_list))

noun_adj_list = []


# tag가 명사이거나 형용사인 단어들만 noun_adj_list에 넣어준다.
for word, tag in sentences_tag:
    if tag in ["Noun", "Adjective"]:
        noun_adj_list.append(word)


# 가장 많이 나온 단어부터 40개를 저장한다.
counts = Counter(noun_adj_list)
tags = counts.most_common(40)



mask_img = np.array(Image.open("heart_mask.jpg"))
wc = WordCloud(
    # font_path="c:\\Windows\\Fonts\\H2MJSM.TTF",
    font_path="~/Library/Fonts/D2Coding-Ver1.3.2-20180524.ttf",
    background_color="black",
    max_font_size=60,
    mask=mask_img,
)



cloud = wc.generate_from_frequencies(dict(tags))

plt.figure(figsize=(10, 8))
plt.imshow(cloud)
plt.axis("off")
plt.show()

# 생성된 WordCloud를 keword.jpg로 보낸다.
cloud.to_file("keyword.jpg")
