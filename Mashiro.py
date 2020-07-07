#!/usr/bin/python3
import wordcloud as wc
import matplotlib.pyplot as plt
import time

words = open("./WCT.txt",'r').read()
now = time.localtime(time.time())

if(now.tm_hour > 6 | now.tm_hour < 19):
    color = "white"
else:
    color = "black"

front = wc.WordCloud(background_color=color,font_path="C:\Windows\Fonts\MSYH.TTC",width = 1440,height = 900,margin = 2).generate(words)

plt.imshow(front)
plt.axis('off')
front.to_file("./a.jpg")

