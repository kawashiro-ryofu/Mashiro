#!/usr/bin/python3

#
#   Mashiro (Win32 ver.)
<<<<<<< HEAD
#   Version:    DEV03
=======
#   Version:    0.02 DEV
>>>>>>> 70586401c29f3232e9dbc03924cda47e05c03327
#   
#   (C)Copyright 2020 RYOUN & the Mashiro Developers
#
#   mGenerate.pyw: WordCloud Background Maker
#

import tkinter.messagebox as tkm
import wordcloud as wc
import matplotlib.pyplot as plt
import time
import win32api, win32gui, win32con,os
import traceback
import json
import requests
from lxml import etree
import signal

def sigoff(signum,frame):
    exit()

signal.signal(signal.SIGINT, sigoff)

def errexec(returnInfo:str):
    tkm.showerror("Error",returnInfo)
    exit()

#Exit Function
def offsig(signum,frame):
    exit(signum)

#Bind 
signal.signal(signal.SIGTSTP, offsig)


class SETTINGS:
<<<<<<< HEAD
    Color:list = [1,"white"]
    Margin:int
    Font:str
    Resolution = [1024,768]
    Mask:str
    AutoRefresh:int
    Spiders:list
=======
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
>>>>>>> 70586401c29f3232e9dbc03924cda47e05c03327
    def __init__(self):
        
        try:
            profile = json.loads(open("./settings.json","r").read())
        except:
<<<<<<< HEAD
            errexec(traceback.format_exc())

=======
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)
>>>>>>> 70586401c29f3232e9dbc03924cda47e05c03327
        try:
            self.Color[0] = profile["Settings"]["BG-Color"]["Daylight"]
            self.Color[1] = profile["Settings"]["BG-Color"]["Color"]
            self.Margin = profile["Settings"]["BG-Margin"]
            self.Font = profile["Settings"]["BG-Font"]
            self.Resolution[0] = profile["Settings"]["Resolution"]['x']
            self.Resolution[1] = profile["Settings"]["Resolution"]['y']
            self.Mask = profile["Settings"]["Mask"]
<<<<<<< HEAD
            self.AutoRefresh = profile["Settings"]["AutoRefreshInterval"]
            self.Spiders = profile["Spiders"]
        except:
            errexec(traceback.format_exc())
        
def applyBG(pic:str):
=======
            self.TextSource = profile["Settings"]["TextSource"]
            self.AutoRefresh = profile["Settings"]["AutoRefreshInterval"]
        except:
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)

def applyBG(pic):
>>>>>>> 70586401c29f3232e9dbc03924cda47e05c03327
    # Apply Background Wallpaper 
    # * https://www.jb51.net/article/155070.htm
    
    # open register
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey,"WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,pic, win32con.SPIF_SENDWININICHANGE)

def spiders(url:list):
    try:
        wordSource:str = ""
        text:str = ""
        for c in range(len(url)):
            out = etree.HTML(requests.get(url[c]).text).xpath("//p/text()")
            for d in range(len(out)):
                print(out[d])
                text += (out[d] + ' ')
    except:
        errexec(traceback.format_exc())

    return text

def main():
    
    while 1:
        setting = SETTINGS()
        try:
            words = spiders(setting.Spiders)
            now = time.localtime(time.time())

        except:
            # ERROR OUTPUT
<<<<<<< HEAD
            errexec(traceback.format_exc())
=======
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)
>>>>>>> 70586401c29f3232e9dbc03924cda47e05c03327

        try:
            # Daylight Background Color
            if(setting.Color[0] == 1):
                if((now.tm_hour > 6) == 1):
                    color = "white"
                if((now.tm_hour > 19 or now.tm_hour < 6) == 1):
                    color = "black"

            else:
                color = setting.Color[1]

            # Generate Wordcolud
            front = wc.WordCloud(background_color=color,font_path=setting.Font,width = setting.Resolution[0],height = setting.Resolution[1],margin = setting.Margin).generate(words)

            plt.imshow(front)
            # Output Wallpaper
            front.to_file("./o.jpg")
            
        except:
<<<<<<< HEAD
            errexec(traceback.format_exc())
=======
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)
>>>>>>> 70586401c29f3232e9dbc03924cda47e05c03327
            
        try:
            #Apply
            applyBG(os.getcwd()+".\\o.jpg")
       
        except:
<<<<<<< HEAD
            errexec(traceback.format_exc())
=======
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)
>>>>>>> 70586401c29f3232e9dbc03924cda47e05c03327


        #(Wait)
        time.sleep(setting.AutoRefresh * 60)

if(__name__ == "__main__"):
    main()