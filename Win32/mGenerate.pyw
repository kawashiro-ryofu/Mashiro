#!/usr/bin/python3

#
#   Mashiro (Win32 ver.)
#   Version:    0.00 DEV
#   
#   (C)Copyright 2020 RYOUN & the Mashiro Developers
#
#   mGenerate.pyw: WordCloud Background Maker
#

import wordcloud as wc
import matplotlib.pyplot as plt
import time
import win32api, win32gui, win32con,os
import traceback
import json

class SETTINGS:
    Color = [1,"white"]
    Margin = 0
    Font = "C:\\Windows\\Fonts\\ARIALN.TTF"
    Resolution = [1024,768]
    Mask = "0"
    TextSource = "./WCT.txt"
    AutoRefresh = 0
    def __init__(self):
        profile = json.loads(open("./settings.json","r").read())
        self.Color[0] = profile["Settings"]["BG-Color"]["Daylight"]
        self.Color[1] = profile["Settings"]["BG-Color"]["Color"]
        self.Margin = profile["Settings"]["BG-Margin"]
        self.Font = profile["Settings"]["BG-Font"]
        self.Resolution[0] = profile["Settings"]["Resolution"]['x']
        self.Resolution[1] = profile["Settings"]["Resolution"]['y']
        self.Mask = profile["Settings"]["Mask"]
        self.TextSource = profile["Settings"]["TextSource"]
        self.AutoRefresh = profile["Settings"]["AutoRefreshInterval"]
        
def applyBG(pic):
    # Apply Background Wallpaper 
    # * https://www.jb51.net/article/155070.htm
    
    # open register
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey,"WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,pic, win32con.SPIF_SENDWININICHANGE)

def main():
    
    while 1:
        setting = SETTINGS()
        try:
            # WCT.txt:Words To Generate Background Wallpaper
            words = open(setting.TextSource,'r').read()
            now = time.localtime(time.time())

        except:
            # ERROR OUTPUT
            traceback.print_exc()

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
            traceback.print_exc()
            
        try:
            #Apply
            applyBG(os.getcwd()+".\\o.jpg")
       
        except:
            traceback.print_exc()


        #(Wait)
        time.sleep(60)

if(__name__ == "__main__"):
    main()