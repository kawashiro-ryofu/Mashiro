#!/usr/bin/python3.8

#
#   Mashiro (Linux ver.)
#   Version:    0.02 DEV(XFCE)
#   
#   (C)Copyright 2020 RYOUN & the Mashiro Developers
#
#   mGenerate.pyw: WordCloud Background Maker
#

import tkinter.messagebox as tkm
import wordcloud as wc
import matplotlib.pyplot as plt
import time
import traceback
import json
import signal

#Exit Function
def offsig(signum,frame):
    exit(signum)

#Bind 
signal.signal(signal.SIGTSTP, offsig)

class SETTINGS:
    #Default Settings
    
    #Color  Element 1:Daylight Mode;
    #       Element 2:Background Color.
    Color = [1,"white"]
    #Margin Of The Word Cloud
    Margin = 0
    #Word Font
    Font = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc"
    #Screen Resolution
    Resolution = [1024,768]
    #Word Cloud Mask Image
    #Disable:0
    Mask = "0"
    #Default Text Source
    TextSource = "./WCT.txt"
    #Autorefresh Inervals(minutes)
    AutoRefresh = 1
    #Wallpaper Image Output Source
    Output = "~/.mashiro"

    def __init__(self):
        try:
            profile = json.loads(open("./settings.json","r").read())
        except:
            errexec(traceback.format_exc())
            offsig(0,0)

        try:
            self.Color[0] = profile["Settings"]["BG-Color"]["Daylight"]
            self.Color[1] = profile["Settings"]["BG-Color"]["Color"]
            self.Margin = profile["Settings"]["BG-Margin"]
            self.Font = profile["Settings"]["BG-Font"]
            self.Resolution[0] = profile["Settings"]["Resolution"]['x']
            self.Resolution[1] = profile["Settings"]["Resolution"]['y']
            self.Mask = profile["Settings"]["Mask"]
            self.TextSource = profile["Settings"]["TextSource"]
            self.AutoRefresh = profile["Settings"]["AutoRefreshInterval"]
            self.Output = profile["Settings"]["Output"]
        except:
            errexec(traceback.format_exc())
            offsig(0,0)

def main():

    while 1:
        setting = SETTINGS()
        try:
            # WCT.txt:Words To Generate Background Wallpaper
            words = open(setting.TextSource,'r').read()
            now = time.localtime(time.time())
        except:
            errexec(traceback.format_exc())
            offsig(0,0)

        try:
            # Daylight Background Color
            if(setting.Color[0] == 1):
                if(now.tm_hour > 6 | now.tm_hour < 19):
                    color = "white"
                else:
                    color = "black"
            else:
                color = setting.Color[1]
        except:
            errexec(traceback.format_exc())
            offsig(0,0)
        try:
        
            # Generate Wordcolud
            front = wc.WordCloud(background_color=color,font_path=setting.Font ,width = setting.Resolution[0],height = setting.Resolution[1],margin = setting.Margin).generate(words)

            plt.imshow(front)
            front.to_file(setting.Output)
        except:
            errexec(traceback.format_exc())
            offsig(0,0)

        time.sleep(setting.AutoRefresh * 60)




if __name__ == "__main__":
    main()