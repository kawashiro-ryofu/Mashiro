#!/usr/bin/python3
#
#   Mashiro (Win32 ver.)
#   Version:    DEV05 20200730 2nd UPDATE
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

def sigoff(signum,frame):
    exit()

signal.signal(signal.SIGINT, sigoff)
words:str = ""

def errexec(returnInfo:str,Exit):
    #tkm.showerror("Error",returnInfo)
    win32api.MessageBox(0,returnInfo,"OOPS!",win32con.MB_ICONERROR)
    if(Exit == 1):
        exit();

#Exit Function
def offsig(signum,frame):
    exit(signum)



class SETTINGS:
    Color:list = [1,"white"]
    Margin:int
    Font:str
    Resolution = [1024,768]
    Mask:str
    AutoRefresh:int
    Spiders:list
    StopWords:list
    Position:list = [False,[0,0,0],[0,0,0]]
    # Position[0]:Enable
    # Position[1]:latitude  | [0][0] Degrees | [0][1] Cents
    # Position[2]:longitude | [1][0] Degrees | [1][1] Cents    
    # <=To Be Continued/|/

    def __init__(self):
        
        try:
            #Get Configure File(~/.Mashiro/settings.json)
            
            profile = json.loads(open(os.path.expanduser('~')+"\\.Mashiro\\settings.json","r",encoding="utf-8-sig").read())
            
        except:
            errexec(traceback.format_exc(),1)
        try:
            self.Color[0] = profile["Settings"]["BG-Color"]["Daylight"]
            self.Color[1] = profile["Settings"]["BG-Color"]["Color"]
            self.Margin = profile["Settings"]["BG-Margin"]
            self.Font = profile["Settings"]["BG-Font"]
            self.Resolution[0] = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            self.Resolution[1] = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            self.Mask = profile["Settings"]["Mask"]
            self.AutoRefresh = profile["Settings"]["AutoRefreshInterval"]
            self.Spiders = profile["Spiders"]
            self.StopWords = profile["StopWords"]
            self.Position[0] = profile["Settings"]["BG-Color"]["Position"]["Enable"]
            self.Position[1] = profile["Settings"]["BG-Color"]["Position"]["Latitude"]
            self.Position[2] = profile["Settings"]["BG-Color"]["Position"]["Longitude"]

            if(len(self.Position) != 3):
                raise(IOError)
                #To Be Continued

            if(self.Position[0] == False):
                self.Position[1] = [0,0,0]
                self.Position[2] = [0,0,0]
            

            # Set auto-start in the registry
            Key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Run",0,win32con.KEY_SET_VALUE)
            win32api.RegSetValueEx(Key,"Mashiro", 0, win32con.REG_SZ,os.path.split(os.path.realpath(__file__))[0]+os.path.split(os.path.realpath(__file__))[1])
            
        except IOError:
            errexec("Could not find config file \" "+ os.path.expanduser('~')+"\\.Mashiro\\settings.json" +"\"",1)

        except:
            errexec(traceback.format_exc(),1)


def applyBG(pic:str):

    # Apply Background Wallpaper 
    # * https://www.jb51.net/article/155070.htm
    
    # open register
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey,"WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,pic, win32con.SPIF_SENDWININICHANGE)

def spiders(url:list,StopWords:list):
    wordSource:str = ""
    text:str = ""

    try:
        for c in range(len(url)):
            out = etree.HTML(requests.get(url[c]).text).xpath("//p/text()")
            for d in range(len(out)):
                if(len(StopWords) != 0):
                    for e in range(len(StopWords)):
                        print(out[d])
                        if(re.search(StopWords[e],out[d])!=None):
                            pass
                text += (out[d] + ' ')

    except requests.exceptions.Timeout:
        text = "ConnectionTimedOut 连接超时 接続がタイムアウトしました 連接超時 СоединениеИстекший 연결이만료되었습니다 หมดเวลาการเชื่อมต่อ";
        

    except requests.exceptions.ConnectionError:
        text = "ConnectionError 连接错误 接続エラー 連接錯誤 ОшибкаПодключения 연결오류 การเชื่อมต่อล้มเหลว";
        
    except:
        errexec(traceback.format_exc(),1)

    print(text)
    return text

def main():
      while 1:
        setting = SETTINGS()
        global words
        words += spiders(setting.Spiders,setting.StopWords)

        try:
            now = time.localtime(time.time())
            print(now)
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
            if(setting.Color[0] == 1):
                if((now.tm_hour >= SUN[0]) and (now.tm_min >= SUN[1])):
                    # Generate Wordcolud
                    
                    front = wc.WordCloud(
                        background_color="white",
                        font_path=setting.Font,
                        width = setting.Resolution[0],
                        height = setting.Resolution[1],
                        margin = setting.Margin
                        ).generate(words)
                    print("Finished Generate Wordcloud Background ")
                    front.to_file(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")

                if((now.tm_hour>=SUN[2] and now.tm_min>=SUN[3])or(now.tm_hour < SUN[0])):
                    # Generate Wordcolud

                    front = wc.WordCloud(
                        background_color="black",
                        font_path=setting.Font,
                        width = setting.Resolution[0],
                        height = setting.Resolution[1],
                        margin = setting.Margin
                        ).generate(words)
                    print("Finished Generate Wordcloud Background ")
                    front.to_file(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")

            else:
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
            errexec("This URL is not available,Please Change Another Site.",0)
            words += "UnavailableURL"
            
        except:
            errexec(traceback.format_exc(),1)
        else:
            word = ""
            
        try:
            #Apply
            applyBG(os.path.expanduser('~')+"\\.Mashiro\\o.jpg")
       
        except:
            errexec(traceback.format_exc(),0)


        #(Wait)
        time.sleep(setting.AutoRefresh * 60)

if(__name__ == "__main__"):
    
    main()
