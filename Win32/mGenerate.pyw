<<<<<<< HEAD
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
import sys
import _thread
import pystray #SysTrayIcon
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image 
import base64
from io import BytesIO


# Bind The SIGINT signal
def sigoff(signum,frame):
    _thread.exit()
    exit(signum)
signal.signal(signal.SIGINT, sigoff)
signal.signal(signal.SIGTERM , sigoff)


#Globle Variable:words
#Store the words that make up the Word-cloud.
words:str = ""

def applyBG(pic:str):
    try:
        # Apply Background Wallpaper
        # * https://www.jb51.net/article/155070.htm

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

def mSettingsGUI():
    os.popen(os.path.split(os.path.realpath(__file__))[0]+'\\mSettingsGUI.pyw')

def AutoStartConf(threadname:str,ProfileConfigure:bool):
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
    icon = pystray.Icon("TopixPopTrayIcon")
    
    IconBase64 = """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"""
    byte_data = base64.b64decode(IconBase64)
    IconPNG = BytesIO(byte_data)
    icon.icon = Image.open(IconPNG)

    def act1(icon,item):
        mSettingsGUI()

    def act2(icon,item):
        about()

    def act3(icon,item):
        icon.stop()
        os._exit(0)

    #Three menu items are defined and given corresponding functions
    icon.menu=menu(item('Settings',act1),item('About',act2),item("Exit",act3))

    #Update the state in on_clicked and return the new state in the form of a checked call
    icon.run()

def about():
    pass

def main():
    
    #The Mainloop (Sure?
    while 1:
        #Load User's Configuration
        try:
            setting = SETTINGS()
            print(setting.AutoStart)
            _thread.start_new_thread( AutoStartConf, ("AutoStartConfiguration", setting.AutoStart) )
            _thread.start_new_thread( sysTrayIcon, () )
        except:
            errexec("Failed To Read Settings Profile",0)
            try:
                open(os.path.split(os.path.realpath(__file__))[0]+'\\mSettingsGUI.pyw',"rb")
            except FileNotFoundError:
                errexec("The component is missing, please reinstall this product.",1)
            mSettingsGUI()
            wait=True
            while(wait):
                try:
                    setting = SETTINGS()
                    print("Waiting")
                except:
                    pass
                else:
                    wait=False

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
            print(SUN)
        except:
            # ERROR OUTPUT
            errexec(traceback.format_exc(),0)

        try:

            # Daylight Background Color
            if(
                (setting.Color[0] == 1) and
                (now.tm_hour >= SUN[0]) and (now.tm_min >= SUN[1]) and
                (now.tm_hour < SUN[2]) and (now.tm_min < SUN[3])
                ):
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

            elif(
                (setting.Color[0] == 1) and
                (now.tm_hour >= SUN[2]) and (now.tm_min >= SUN[3])
                ):
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
            word=""
        except:
            errexec(traceback.format_exc(),0)


        #(Wait)
        time.sleep(setting.AutoRefresh * 60)

if(__name__ == "__main__"):

    main()
=======
#!/usr/bin/python3
#
#   TopixPop Win32
#   Version:    BETA
#
#   (C)Copyright 2020 RYOUN & the TopixPop Developers
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
import sys
import _thread

# Bind The SIGINT signal
def sigoff(signum,frame):
    exit(signum)
signal.signal(signal.SIGINT, sigoff)

#Globle Variable:words
#Store the words that make up the Word-cloud.
words:str = ""

def applyBG(pic:str):
    try:
        # Apply Background Wallpaper
        # * https://www.jb51.net/article/155070.htm

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

def mSettingsGUI():
    os.popen(os.path.split(os.path.realpath(__file__))[0]+'\\mSettingsGUI.pyw')

def AutoStartConf(threadname:str,ProfileConfigure:bool):
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
        #errexec("Failed To Edit Registry",0)
        errexec(traceback.format_exc(),0)

def main():
    
    #The Mainloop (Sure?
    while 1:
        #Load User's Configuration
        try:
            setting = SETTINGS()
            print(setting.AutoStart)
            _thread.start_new_thread( AutoStartConf, ("AutoStartConfiguration", setting.AutoStart) )
        except:
            errexec("Failed To Read Settings Profile",0)
            try:
                open(os.path.split(os.path.realpath(__file__))[0]+'\\mSettingsGUI.pyw',"rb")
            except FileNotFoundError:
                errexec("The component is missing, please reinstall this product.",1)
            mSettingsGUI()
            wait=True
            while(wait):
                try:
                    setting = SETTINGS()
                    print("Waiting")
                except:
                    pass
                else:
                    wait=False

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
            print(SUN)
        except:
            # ERROR OUTPUT
            errexec(traceback.format_exc(),0)

        try:

            # Daylight Background Color
            if(
                (setting.Color[0] == 1) and
                (now.tm_hour >= SUN[0]) and (now.tm_min >= SUN[1]) and
                (now.tm_hour < SUN[2]) and (now.tm_min < SUN[3])
                ):
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

            elif(
                (setting.Color[0] == 1) and
                (now.tm_hour >= SUN[2]) and (now.tm_min >= SUN[3])
                ):
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
            word=""
        except:
            errexec(traceback.format_exc(),0)


        #(Wait)
        time.sleep(setting.AutoRefresh * 60)

if(__name__ == "__main__"):

    main()
>>>>>>> 24f3721b2b49b44f4ebb702ae877e230200db43a
