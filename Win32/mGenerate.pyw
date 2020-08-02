#!/usr/bin/python3
#
#   Mashiro (Win32 ver.)
#   Version:    DEV05 4rd UPDATE
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
import requests
from lxml import etree
import signal
import re
import sun
from mSet import SETTINGS,errexec

# Bind The SIGINT signal
def sigoff(signum,frame):
    exit(signum)
signal.signal(signal.SIGINT, sigoff)

#Globle Variable:words
#Store the words that make up the Word-cloud.
words:str = ""

def applyBG(pic:str):

    # Apply Background Wallpaper 
    # * https://www.jb51.net/article/155070.htm
    
    # open register
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey,"WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,pic, win32con.SPIF_SENDWININICHANGE)

#The Spider 
def spiders(url:list,StopWords:list):
    text:str = ""

    try:
        for c in range(len(url)):
            #Craw paragraph elements
            out = etree.HTML(requests.get(url[c]).text).xpath("//p/text()")
            for d in range(len(out)):
                #If the Stopwords function is enabled
                if(len(StopWords) != 0):
                    for e in range(len(StopWords)):
                        if(re.search(StopWords[e],out[d])==None):
                            text += (out[d] + ' ')
                        else:
                            pass
                else:
                    #If the Stopwords function is disabled
                    text += (out[d] + ' ')

    except requests.exceptions.Timeout:
        text = "ConnectionTimedOut 连接超时 接続がタイムアウトしました 連接超時 СоединениеИстекший 연결이만료되었습니다 หมดเวลาการเชื่อมต่อ"
    except requests.exceptions.ConnectionError:
        text = "ConnectionError 连接错误 接続エラー 連接錯誤 ОшибкаПодключения 연결오류 การเชื่อมต่อล้มเหลว"
        
    except:
        errexec(traceback.format_exc(),1)
        
    return text

def main():
    # Set auto-start item in the registry
    Key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        win32con.KEY_SET_VALUE)

    win32api.RegSetValueEx(
        Key,
        "Mashiro",
        0,
        win32con.REG_SZ,
        os.path.split(
            os.path.realpath(__file__))[0]+'\\'+os.path.split(os.path.realpath(__file__))[1])

    #The Mainloop (Sure?
    while 1:
        #Load User's Configuration
        setting = SETTINGS()
        global words
        #Craw Words From the Web
        words = spiders(setting.Spiders,setting.StopWords)

        try:
            now = time.localtime(time.time())
            #Calculate Sunrise And Sunset Time
            SUN = sun.calc(
                now.tm_year,
                now.tm_mon,
                now.tm_mday,
                setting.Position[1],
                setting.Position[2])
            
        except:
            # ERROR OUTPUT
            errexec(traceback.format_exc(),0)

        try:
            
            # Daylight Background Color
            if((setting.Color[0] == 1) and (now.tm_hour >= SUN[0]) and (now.tm_min >= SUN[1])):
                # Generate Wordcolud
                # During the day
                front = wc.WordCloud(
                    background_color="white",
                    font_path=setting.Font,
                    width = setting.Resolution[0],
                    height = setting.Resolution[1],
                    margin = setting.Margin
                    ).generate(words)
                    
                front.to_file(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")

            elif((setting.Color[0] == 1)and((now.tm_hour>=SUN[2] and now.tm_min>=SUN[3])or(now.tm_hour < SUN[0]))):
                # Generate Wordcolud
                # In night
                front = wc.WordCloud(
                    background_color="black",
                    font_path=setting.Font,
                    width = setting.Resolution[0],
                    height = setting.Resolution[1],
                    margin = setting.Margin
                    ).generate(words)
                front.to_file(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")
            else:
                # Daylight Disabled
                # Generate Wordcolud
                front = wc.WordCloud(
                    background_color=setting.Color[1],
                    font_path=setting.Font,
                    width = setting.Resolution[0],
                    height = setting.Resolution[1],
                    margin = setting.Margin
                    ).generate(words)
                
                front.to_file(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")

        except ValueError:
            # (= \)
            errexec("This URL is not available,Please Change Another Site.",0)
            words = "UnavailableURL"
            front = wc.WordCloud(
                background_color=setting.Color[1],
                font_path=setting.Font,
                width = setting.Resolution[0],
                height = setting.Resolution[1],
                margin = setting.Margin
                ).generate(words)
                
            front.to_file(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")
            
        except:
            errexec(traceback.format_exc(),1)
        else:
            #Clear The Words
            words = ""
            
        try:
            #Apply
            applyBG(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")
       
        except:
            errexec(traceback.format_exc(),0)


        #(Wait)
        time.sleep(setting.AutoRefresh * 60)

if(__name__ == "__main__"):
    
    main()

