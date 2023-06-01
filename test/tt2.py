# -*- coding: utf-8 -*-

"""
@File    : tt2.py
@Author  : xiaoming
@Time    : 2023-5-25 11:31
"""
import codecs

# f = codecs.open(dir+location, 'r', encoding='utf-8')
# txt = f.read()

from tqdm import tqdm
stopwords_file = 'stopwords.txt'
# stopwords_file = 'cn_stopwords.txt'  哈工大停用词表  https://github.com/goto456/stopwords
with codecs.open(stopwords_file, "r", encoding='ISO-8859-1') as words:  # ,encoding='utf-8'
    for i in tqdm(words):
        print(i)
        try:
            x = i.encode("ISO-8859-1").decode("utf-8")
        except Exception as e:
            x = ''
            print(e)
        if x != '':
            print(x)
            with codecs.open("stopwords.txt", "a", encoding='utf-8') as f:
                f.write(x)
    # stopwords = [i.strip() for i in words]
    # print(stopwords)
