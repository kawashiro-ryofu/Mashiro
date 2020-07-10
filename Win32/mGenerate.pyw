#!/usr/bin/python3

#
#   Mashiro (Win32 ver.)
#   Version:    0.02 DEV
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
    def __init__(self):
        
        try:
            profile = json.loads(open("./settings.json","r").read())
        except:
            tkm.showerror("Error",traceback.format_exc())
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
        except:
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)

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
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)

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
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)
            
        try:
            #Apply
            applyBG(os.getcwd()+".\\o.jpg")
       
        except:
            tkm.showerror("Error",traceback.format_exc())
            offsig(0,0)


        #(Wait)
        time.sleep(setting.AutoRefresh * 60)

if(__name__ == "__main__"):
    main()