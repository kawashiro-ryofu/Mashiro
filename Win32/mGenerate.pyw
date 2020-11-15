#!/usr/bin/python3
#
#   ToixPop (Win32 ver.)
#   Version:    BETA 2
#
#   Copyright © 2020 RYOUN
#
#   mGenerate.pyw: WordCloud Background Maker
#

__version__ = "BETA 2 20201115"

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
import sys
import _thread
import pystray #SysTrayIcon
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image 
import base64
from io import BytesIO
import webbrowser
import tkinter as tk


# Bind The SIGINT signal
def sigoff(signum,frame):
    _thread.exit()
    exit(signum)

signal.signal(signal.SIGINT, sigoff)
signal.signal(signal.SIGTERM , sigoff)


#Globle Variable:words
#Store the words that make up the Word-cloud.
words:str = ""

# Flag Of Manually Refresh
refresh:bool = False

def applyBG(pic:str):
    try:
        # Apply Background Wallpaper

        # open register
        regKey = win32api.RegOpenKeyEx(
            win32con.HKEY_CURRENT_USER,
            "Control Panel\\Desktop",
            0,
            win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(
            regKey,
            "WallpaperStyle",
            0,
            win32con.REG_SZ,
            "2")
        win32api.RegSetValueEx(
            regKey,
            "TileWallpaper",
            0,
            win32con.REG_SZ,
            "0")
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER,
            pic,
            win32con.SPIF_SENDWININICHANGE)
    except:
        errexec("Failed to change wallpaper",0)

#The Spider
def spiders(url:list,StopWords:list):
    text:str = ""

    try:
        for c in range(len(url)):

            connections = requests.get(url[c])
            
            #Craw paragraph elements
            out = etree.HTML(connections.text).xpath("//h1/text()")
            out += etree.HTML(connections.text).xpath("//p/text()")
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

def mSettingsGUI():
    os.popen(os.path.split(os.path.realpath(__file__))[0]+'\\mSettingsGUI.pyw')

def AutoStartConf(ProfileConfigure:bool):
    try:
        if(ProfileConfigure == True):
            # Set auto-start item in the registry
            Key = win32api.RegOpenKeyEx(
                win32con.HKEY_CURRENT_USER,
                "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                0,
                win32con.KEY_SET_VALUE)

            win32api.RegSetValueEx(
                Key,
                "TopixPop",
                0,
                win32con.REG_SZ,
                os.path.split(
                    os.path.realpath(__file__)
                )[0]+'\\'+os.path.split(os.path.realpath(__file__))[1])
        else:
            Key = win32api.RegOpenKeyEx(
                win32con.HKEY_CURRENT_USER,
                "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                0,
                win32con.KEY_SET_VALUE)

            win32api.RegSetValueEx(
                Key,
                "TopixPop",
                0,
                win32con.REG_SZ,
                ""
            )
    except:
        errexec("Failed To Edit Registry",0)

def sysTrayIcon():
    

    icon = pystray.Icon("TopixPop")
    
    IconBase64 = """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"""
    byte_data = base64.b64decode(IconBase64)
    IconPNG = BytesIO(byte_data)
    icon.icon = Image.open(IconPNG)

    def act1(icon,item):
        mSettingsGUI()

    def act2(icon,item):
        _thread.start_new_thread( about, () )

    def act3(icon,item):
        global refresh
        refresh = True
    
    def act4(icon,item):
        icon.stop()
        # Restore Wallpaper
        regKey = win32api.RegOpenKeyEx(
            win32con.HKEY_CURRENT_USER,
            "Control Panel\\Desktop",
            0,
            win32con.KEY_ALL_ACCESS
        )
        applyBG(
            win32api.RegQueryValueEx(
                regKey,
                'Wallpaper'
            )[0]
        )
        os._exit(0)

    # Three menu items are defined and given corresponding functions
    icon.menu=menu(
        item('Settings',act1),
        item('About',act2),
        item('Refresh',act3),
        item("Exit",act4)
        )

    # Update the state in on_clicked and return the new state in the form of a checked call
    icon.run()

def about():
    global __version__

    '''About Page'''
    About = tk.Tk()    
    About.title("About TopixPop")

    IconBase64 = """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"""
    IconTemp = open("tmp","wb+")
    IconTemp.write(base64.b64decode(IconBase64))
    IconTemp.close()
    About.iconphoto(False , tk.PhotoImage(file="tmp"))
    os.remove("tmp")
    del(IconTemp)
    
    About.resizable(0,0)

    Tpix = "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"
    open("tmp.png","wb+").write(base64.b64decode(Tpix))
    del(Tpix)
    Tpix = tk.PhotoImage(file="tmp.png")
    
    tk.Label(
        About,
        image = Tpix
    ).pack()
    
    tk.Label(
        About,
        text="Version:" + __version__ + "\n\nAuthors:\n Jeffery Yu (非科学のカッパ)\n Eilles Wan (EW羿君~)\n\n",
        font=("Arial",12),
    ).pack()

    tk.Label(
        About,
        text="License Under Mozilla Public License v2.0",
        font=("Arial",10)
    ).pack(side="bottom")
    tk.Label(
        About,
        text="Copyright © 2020 RYOUN, Some Rights Reserved",
        font=("Arial",12)
    ).pack(side="bottom")

    def website():
        webbrowser.open("https://github.com/kawashiro-ryofu/topixpop")

    def blog():
        webbrowser.open("https://www.kawashiros.club/")

    def icu996():
        webbrowser.open("https://996.icu/")

    Bts = tk.Frame(About)

    tk.Button(Bts,text="Visit Github Repository",command=website).pack()
    tk.Button(Bts,text="Author's blog",command=blog).pack()
    tk.Button(Bts,text="Support 996.icu",command=icu996).pack()

    Bts.pack()

    os.remove("tmp.png")
    About.mainloop()

def main():

    global refresh

    try:
        # Load Settings
        setting = SETTINGS()
    except:
        errexec("Failed To Read Settings Profile",0)
        try:
            open(
                os.path.split(os.path.realpath(__file__))[0]+'\\mSettingsGUI.pyw',
                "rb"
                )
        except FileNotFoundError:
            errexec(
                "The component is missing, please reinstall this product.",
                1
                )
        mSettingsGUI()
        # Waiting For Settings Profile
        wait=True
        while(wait):
            try:
                setting = SETTINGS()
                print("Waiting")
            except:
                pass
            else:
                wait=False

    _thread.start_new_thread( 
        AutoStartConf,
        (
            setting.AutoStart
        )
    )
    _thread.start_new_thread( 
        sysTrayIcon, 
        () 
    )
    
    #The Mainloop (Sure?
    while 1:
        #Load User's Configuration
        setting = SETTINGS()
        print("Autostart: " + str(setting.AutoStart))

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
            print("SUNDAT: ",end="")
            print(SUN)
            print("NOWSTAT: ",end="")
        except:
            # ERROR OUTPUT
            errexec(traceback.format_exc(),0)

        try:
            # Daylight Background Color
            if(
                (setting.Color[0] == 1) and
                now.tm_hour * 60 + now.tm_min >= SUN[0] * 60 + SUN[1]

                ):
                # Generate Wordcolud
                # During the day
                print("DAY")
                front = wc.WordCloud(
                    background_color="white",
                    font_path=setting.Font,
                    width = setting.Resolution[0],
                    height = setting.Resolution[1],
                    margin = setting.Margin
                    ).generate(words)

                front.to_file(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")

            elif(
                (setting.Color[0] == 1) and
                now.tm_hour * 60 + now.tm_min < SUN[0] * 60 + SUN[1]
                ):
                # Generate Wordcolud
                # In night
                print("NIGHT")
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
                print("DISABLED")
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
            words = "UnavailableURL URL不可用 使用できないURL НедоступныйURL  사용할수없는URL   URLไม่พร้อมใช้งาน "
            front = wc.WordCloud(
                background_color=setting.Color[1],
                font_path=setting.Font,
                width = setting.Resolution[0],
                height = setting.Resolution[1],
                margin = setting.Margin
                ).generate(words)
            mSettingsGUI()
            front.to_file(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")
        except OSError:
            errexec("Can not open resource\nPlease have a check in Your Settings",0)
            mSettingsGUI()

        except:
            errexec(traceback.format_exc(),1)
        else:
            #Clear The Words
            words = ""

        try:
            #Apply
            applyBG(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")
            words=""
        except:
            errexec(traceback.format_exc(),0)

        #(Wait)
        #time.sleep(setting.AutoRefresh * 60)

        remaining = setting.AutoRefresh * 60
        while(refresh == False):
            if(remaining < 2):
                refresh = True
            remaining-=1
            time.sleep(1)
        
        refresh = False
            

if(__name__ == "__main__"):

    main()
