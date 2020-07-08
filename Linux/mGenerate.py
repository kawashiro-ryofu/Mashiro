#!/usr/bin/python3.8

#
#   Mashiro (Linux ver.)
#   Version:    0.00 DEV(XFCE)
#   
#   (C)Copyright 2020 RYOUN & the Mashiro Developers
#
#   mGenerate.pyw: WordCloud Background Maker
#
import wordcloud as wc
import matplotlib.pyplot as plt
import time
import traceback
import json

class SETTINGS:
    Color = [1,"white"]
    Margin = 0
    Font = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc"
    Resolution = [1024,768]
    Mask = "0"
    TextSource = "./WCT.txt"
    AutoRefresh = 0
    def __init__(self):
        try:
            profile = json.loads(open("./settings.json","r").read())
        except:
            traceback.format_exc()

        self.Color[0] = profile["Settings"]["BG-Color"]["Daylight"]
        self.Color[1] = profile["Settings"]["BG-Color"]["Color"]
        self.Margin = profile["Settings"]["BG-Margin"]
        self.Font = profile["Settings"]["BG-Font"]
        self.Resolution[0] = profile["Settings"]["Resolution"]['x']
        self.Resolution[1] = profile["Settings"]["Resolution"]['y']
        self.Mask = profile["Settings"]["Mask"]
        self.TextSource = profile["Settings"]["TextSource"]
        self.AutoRefresh = profile["Settings"]["AutoRefreshInterval"]
        

def main():

    while 1:

        words = open("./WCT.txt",'r').read()
        now = time.localtime(time.time())

        if(now.tm_hour > 6 | now.tm_hour < 19):
            color = "white"
        else:
            color = "black"

        front = wc.WordCloud(background_color=color,font_path='/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf' ,width = 1440,height = 900,margin = 3).generate(words)

        plt.imshow(front)
        plt.axis('off')
        front.to_file("./a.jpg")

        time.sleep(60)




if __name__ == "__main__":
    main()