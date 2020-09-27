#!/usr/bin/python3
#
#   TopixPop (Win32)
#   Version:  BETA 1
#
#   Copyright © 2020 RYOUN
#
#   mSettingGUI.py: Settings(GUI)
#
import tkinter as tk
import tkinter.colorchooser as tkcolor
import tkinter.filedialog as tkfile
import tkinter.font as tkfont
from tkinter import ttk
import mSet
import json
import _thread
import time
import requests
import locale
import re
import tkinter.messagebox as tkmsg
import platform
import os
import signal
import PIL
import base64
from io import BytesIO
from PIL import Image, ImageTk

'''Show Changes On Title'''
def TitleEffact(threadname,delay,Info):
    MainWin.title(Info)
    time.sleep(2)
    MainWin.title("TopixPop Settings")

'''Generate the window class'''
MainWin = tk.Tk()
MainWin.title("TopixPop Settings")
MainWin.geometry("640x480")
MainWin.resizable(0,0)

'''icon'''
IconBase64 = """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"""
IconTemp = open("tmp","wb+")
IconTemp.write(base64.b64decode(IconBase64))
IconTemp.close()
MainWin.iconphoto(False , tk.PhotoImage(file="tmp"))
os.remove("tmp")

'''Load Settings'''
try:
    setting = mSet.SETTINGS()
except IOError:
    AutoRefresh = tk.StringVar()
    AutoRefresh.set(10)
    ColorDayLight = tk.IntVar()
    ColorDayLight.set(int(True))
    Color = tk.StringVar()
    Color.set("#000000")
    Font = tk.StringVar()
    AutoStart = tk.IntVar()

    if(re.match('zh_CN',locale.getdefaultlocale()[0])!=None):
        print("OS",end=':')
        '''Chinese Simple'''
        '''For Windows 7'''
        if(
            (re.match(platform.version(),"6.1.7601")!=None)is True or
            (re.match(platform.version(),"6.1.7600")!=None)is True
            ):
            print("Win7")
            Font.set("C:\\Windows\\Fonts\\MSYH.TTF")
        else:
            print("Win8.1+")
            '''For Windows 8.1 And Windows 10'''
            Font.set("C:\\Windows\\Fonts\\MSYH.TTC")
    elif(re.match('zh',locale.getdefaultlocale()[0])!=None):
        '''Chinese Traditional'''
        Font.set("C:\\Windows\\Fonts\\simhei.ttf")

    elif(re.match('jp',locale.getdefaultlocale()[0])!=None):
        '''Japaneese'''
        Font.set("C:\\Windows\\Fonts\\msgothic.ttc")

    else:
        '''English And More'''
        Font.set("C:\\Windows\\Fonts\\l_10646.ttf")

    #<=/|To Be Continued

    Spider = ["https://github.com"]
    StopWords:list = []
    Position:list = [False,[0,0,0],[0,0,0]]
else:
    '''Convert'''
    AutoRefresh = tk.StringVar()
    AutoRefresh.set(setting.AutoRefresh)
    ColorDayLight = tk.IntVar()
    ColorDayLight.set(int(setting.Color[0]))
    Color = tk.StringVar()
    Color.set(setting.Color[1])
    Font = tk.StringVar()
    Font.set(setting.Font)
    Spider = setting.Spiders
    StopWords:list = setting.StopWords
    Position:list = setting.Position
    AutoStart = tk.IntVar()
    AutoStart.set(setting.AutoStart)
try: 

    '''Auto Refresh Interval'''
    refresh = tk.Frame(MainWin)
    tk.Label(
        refresh,
        text="Auto Refresh Interval",
        fg="blue",
        font=("Helvetica",20)
        ).pack()

    '''Title Effact'''
    def RefreshStatus():
        Info = "Auto Refresh Interval:Every "+ AutoRefresh.get() +" minute(s) refresh once"
        _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,Info))
    tk.Spinbox(
        refresh,
        from_=1,
        textvariable=AutoRefresh,
        to=180,
        justify="center",
        width=6,
        command=RefreshStatus
        ).pack()

    tk.Label(
        refresh,
        text="Minute(s)",
        
        ).pack()
    refresh.pack(side="top")

    '''Color Settings'''
    ColorConf = tk.Frame(MainWin)
    tk.Label(
        ColorConf,
        text="Background Color",
        fg="blue",
        font=("Helvetica",20),
    ).pack(ipadx="2",side="top")

    '''Title Effact'''
    def DaylightStatus():
        Info = "Daylight Background Color "
        if(ColorDayLight.get() == 1):
            Info += "Enabled"
        else:
            Info += "Disabled"
        _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,Info))
    '''Enable / Disable Daylight'''
    tk.Checkbutton(
        ColorConf,
        text="Enable Daylight Background Color",

        variable=ColorDayLight,
        command=DaylightStatus,
    ).pack(ipadx="2",side="top")
    '''Title Effact'''
    def ColorSet():
        Color.set(tkcolor.askcolor()[1])
        _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Finished Setting Color"))
    '''Set Color'''
    ChooseColor = tk.Button(
        ColorConf,
        text="Choose a Color",
        command=ColorSet
    )
    '''Show Color'''
    ColorMoniter = tk.Label(
        ColorConf,
        text = "        ",
        bg = Color.get()
    )
    '''LocationSetting'''
    locationConf = tk.Frame(ColorConf)
    EnableLocating = tk.IntVar()
    EnableLocating.set(int(Position[0]))
    city:str=""

    '''Get Location By API'''
    def GetLocation():
        global city,Position
        try:
            locrq = requests.get("http://ip-api.com/json")
        except requests.exceptions.ConnectionError:
            mSet.errexec("Failed to connect to remote server\nPlease Check Your Internet Connection",0)
            EnableLocating.set(0)
            Position[0] = False

        if(locrq.status_code >= 400):
            mSet.errexec("HTTP ErrorCode:"+str(locrq.status_code),0)
        else:
            dat = locrq.json()
            latitude = dat["lat"]
            longitude = dat["lon"]
            city = "You are at "+dat["city"] +","+ dat["regionName"] +","+ dat["country"]
            def f2s(i:float):
                deg = int(i)
                i -= deg * 1.0
                i *= 60
                cent = int(i)
                i -= cent * 1.0
                i *= 60
                sec = int(i)
                return [deg,cent,sec]
        return (f2s(latitude),f2s(longitude))


    def LocationEnable():
        if(EnableLocating.get() == 1):
            Position[0] = True
            tmp = GetLocation()
            Position[1] = tmp[0]
            Position[2] = tmp[1]
            _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Locating Enabled"))
        else:
            Position[0] = False
            Position[1] = [0,0,0]
            Position[2] = [0,0,0]
            _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Locating Disabled"))

    tk.Checkbutton(
        locationConf,
        text="Calculate Time Of Sunrise and Sunset by Getting Your Location",

        variable=EnableLocating,
        command=LocationEnable,
    ).pack(ipadx="2",side="top")




    locationConf.pack()
    ColorConf.pack(ipadx="2",side="top")

    # There are tons of problems to be solve.
    # In Three Words, We Need Help
    #
    # Current Default font:
    #    English(en_US en_AU en): Lucida Sana(C:\\Windows\\Fonts\\l_10646.ttf)
    #    Chinese(zh_CN): MS-YaHei(C:\\Windows\\MSYH.ttc)    (zh_TW 如果台湾版自带微软雅黑字体，否则就用黑体)
    #    Japaneese(ja):MS UI Gothic(C:\\Windows\\Fonts\\msgothic.ttc)
    #    To Be Continued...
    '''
    Font Setting
    FontConf = tk.Frame(MainWin)
    tk.Label(
        FontConf,
        text="Font",
        fg="blue",
        font=("Helvetica",20),
    ).pack(ipadx="2",side="top")

    ttk.Combobox(
        FontConf
    ).pack()

    tk.Label(
        FontConf,
        textvariable=Font,
    ).pack(side="left")

    FontConf.pack(ipadx="2",side="top")
    '''


    '''Automatic save the configuration file'''

    '''Spider Configuration'''
    SpiderConf = tk.Frame(MainWin)
    tk.Label(
        SpiderConf,
        text="Spider",
        fg="blue",
        font=("Helvetica",20),
    ).pack(ipadx="2",side="top")
    URLlistPart = tk.Frame(SpiderConf)
    '''List Of URLs For Spider'''
    URLlist = tk.Listbox(
        URLlistPart,
        selectmode="MUTIPLE",
        height=8,
        width=40
    )
    '''Insert URLs'''
    for i in range(len(Spider)):
        URLlist.insert("end",Spider[i])
    scrollbar = tk.Scrollbar(URLlistPart)
    scrollbar.config(command=URLlist.yview)
    scrollbar.pack(side="right",fill="y")
    URLlist.pack(ipadx=2,side="left")
    URLlistPart.pack()
    '''Editing'''
    def AddUrl():
        global Spider
        InputWindow = tk.Toplevel()
        InputWindow.title("Enter URL.")
        InputWindow.geometry("256x96")
        InputWindow.resizable(0,0)
        IconBase64 = """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"""
        IconTemp = open("tmp","wb+")
        IconTemp.write(base64.b64decode(IconBase64))
        IconTemp.close()
        InputWindow.iconphoto(False , tk.PhotoImage(file="tmp"))
        os.remove("tmp")

        tk.Label(InputWindow,text="Enter URL.").pack(side="top")
        def Save():
            ''' Valid Check'''
            if(re.match('http://',NewURLi.get())==None and re.match('https://',NewURLi.get())==None):
                tkmsg.showerror("Oops","Invalid Syntax")
            else:
                global Spider,URLlist
                '''Add Into the current setting'''
                Spider += [NewURLi.get()]
                URLlist.insert("end",NewURLi.get())
                _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Added URL"))
                InputWindow.destroy()
        NewURLi = tk.Entry(InputWindow,width=40)
        tk.Button(InputWindow,text="OK",command=Save).pack(side="bottom",ipadx=3,ipady=3)
        NewURLi.pack(side="top",ipadx=3,ipady=3)
        InputWindow.mainloop()

    def DelUrl():
        global Spider
        '''Select Current Selection and Remove It'''
        a = URLlist.curselection()[0]
        del(Spider[a])
        _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Delete URL success"))
        URLlist.delete(a)

    tk.Button(SpiderConf,text="+ Add",command=AddUrl).pack(side="left")
    tk.Button(SpiderConf,text="- Delete",command=DelUrl).pack(side="left")

    '''Stopwords Editing'''
    def stopword():
        swSetForm = tk.Toplevel()
        swSetForm.geometry("320x256")
        swSetForm.resizable(0,0)
        IconBase64 = """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"""
        IconTemp = open("tmp","wb+")
        IconTemp.write(base64.b64decode(IconBase64))
        IconTemp.close()
        swSetForm.iconphoto(False , tk.PhotoImage(file="tmp"))
        os.remove("tmp")
        swSetForm.title("Stop Words")

        StoplistPart = tk.Frame(swSetForm)
        '''Stopwords List'''
        Stoplist = tk.Listbox(
            StoplistPart,
            selectmode="MUTIPLE",
            height=10,
            width=40
        )
        for i in range(len(StopWords)):
            Stoplist.insert("end",StopWords[i])

        scrollbar = tk.Scrollbar(StoplistPart)
        scrollbar.config(command=Stoplist.yview)
        scrollbar.pack(side="right",fill="y")
        Stoplist.pack(ipadx=2,side="left")

        StoplistPart.pack()

        def Add():
            InputWindow = tk.Toplevel()
            InputWindow.title("Add Stop Word")
            InputWindow.geometry("256x96")
            IconBase64 = """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"""
            IconTemp = open("tmp","wb+")
            IconTemp.write(base64.b64decode(IconBase64))
            IconTemp.close()
            InputWindow.iconphoto(False , tk.PhotoImage(file="tmp"))
            os.remove("tmp")
            InputWindow.resizable(0,0)

            tk.Label(InputWindow,text="Enter Stop Word").pack(side="top")
            def Save():
                    global StopWords
                    '''Add Into Current Stopwords List'''
                    StopWords += [AddStopWord.get()]
                    Stoplist.insert("end",AddStopWord.get())
                    InputWindow.destroy()
                    _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Updated StopWords Lists"))

            AddStopWord = tk.Entry(InputWindow,width=40)
            tk.Button(InputWindow,text="OK",command=Save).pack(side="bottom",ipadx=3,ipady=3)
            AddStopWord.pack(side="top",ipadx=3,ipady=3)
            InputWindow.mainloop()

        def Del():
            global StopWords
            '''Select Current Selection and Remove It'''
            a = Stoplist.curselection()[0]
            del(StopWords[a])
            Stoplist.delete(a)
            _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Updated StopWords Lists"))
        tk.Button(swSetForm,text="+ Add",command=Add).pack(side="left")
        tk.Button(swSetForm,text="- Delete",command=Del).pack(side="left")
        swSetForm.mainloop()


    tk.Checkbutton(
        MainWin,
        text="Start automatically when entering the desktop",
        variable=AutoStart,
    ).pack(ipadx="2",side="top")


    tk.Button(SpiderConf,text="Stop Words",command=stopword).pack(side="left")
    SpiderConf.pack(ipadx="2",side="top")

    '''Setting GUI Auto Refresh And Save'''
    def ApplyRefresh(threadname,delay):
        while(1):
            if(ColorDayLight.get() != 1):
                locationConf.pack_forget()
                ChooseColor.pack(side="right")
                ColorMoniter["bg"] = Color.get()
                ColorMoniter.pack(side="left")

            else:
                locationConf.pack()
                ChooseColor.pack_forget()
                ColorMoniter.pack_forget()
            time.sleep(delay)
    '''Auto Start Checkbox'''


    _thread.start_new_thread( ApplyRefresh, ("Thread-0", 0.1))
    def save():
        profile = json.dumps({
            "Settings":{
                "BG-Color":{
                    "Daylight":bool(ColorDayLight.get()),
                    "Color":Color.get(),
                    "Position":{
                        "Enable":bool(Position[0]),
                        "Latitude":Position[1],
                        "Longitude":Position[2]
                    }
                },
                "BG-Margin":0,
                "BG-Font":Font.get(),
                "Mask":"",
                "AutoRefreshInterval":int(AutoRefresh.get())
            },
            "Spiders":Spider,
            "StopWords":StopWords,
            "AutoStart":bool(AutoStart.get())
        })
        print(profile)
        try:
            with open(os.path.expanduser('~')+"\\.Mashiro\\settings.json","w",encoding="utf-8") as settingJson:
                settingJson.write(profile)
        except FileNotFoundError:
            os.mkdir(os.path.expanduser('~')+"\\.Mashiro")
            with open(os.path.expanduser('~')+"\\.Mashiro\\settings.json","w",encoding="utf-8") as settingJson:
                settingJson.write(profile)

        MainWin.destroy()
        time.sleep(5)
    MainWin.protocol("WM_DELETE_WINDOW", save)
    MainWin.mainloop()
except:
    os.remove(os.path.expanduser('~')+"\\.Mashiro\\settings.json")
    import mSet
    mSet.errexec("Unreadable profile\n",1)