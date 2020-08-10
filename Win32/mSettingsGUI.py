#!/usr/bin/python3
#
#   Mashiro (Win32 ver.)
#   Version:    DEV05 Settings-GUI Developing
#  
#   (C)Copyright 2020 RYOUN & the Mashiro Developers
#
#   mSettingGUI.py:Mashiro Settings(GUI)
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

def mSettingsGUI():
    '''Show Changes On Title'''
    def TitleEffact(threadname,delay,Info):
        MainWin.title(Info)
        time.sleep(2)
        MainWin.title("Mashiro Settings")

    '''Generate the window class'''
    MainWin = tk.Tk()
    MainWin.title("Mashiro Settings")
    MainWin.geometry("640x480")
    MainWin.resizable(0,0)


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
        
        if(re.match('zh_CN',locale.getdefaultlocale()[0])!=None):
            '''Chinese Simple'''
            '''For Windows 7'''
            if(platform.version == "6.1.7601"):
                Font.set("C:\\Windows\\Fonts\\MSYH.TTF")
            else:
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

        Spider:list = ["https://github.com"]
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
        Spider:list = setting.Spiders
        StopWords:list = setting.StopWords
        Position:list = setting.Position

    '''Heading'''
    tk.Label(
        MainWin,
        text="🛠️Settings",
        font=("Arial",30)
        ).pack(side="top",ipadx="3")

    '''Auto Refresh Interval'''
    refresh = tk.Frame(MainWin)
    tk.Label(
        refresh,
        text="⏰Auto Refresh Interval",
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
        text="Minutes",
        font=("Helvetica",10),
        ).pack()
    refresh.pack(side="top")

    '''Color Settings'''
    ColorConf = tk.Frame(MainWin)
    tk.Label(
        ColorConf,
        text="🎨Color",
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
        font=("Helvetica",10),
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
        
    NowLoc = tk.Label(locationConf,text=city)


    def LocationEnable():
        if(EnableLocating.get() == 1):
            Position[0] = True
            tmp = GetLocation()
            Position[1] = tmp[0]
            Position[2] = tmp[1]
            NowLoc.pack()
            _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Locating Enabled"))
        else:
            Position[0] = False
            NowLoc.pack_forget()
            '''Replace User's Position as default'''
            Position[1] = [0,0,0]
            Position[2] = [0,0,0]
            _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Locating Disabled"))

    tk.Checkbutton(
        locationConf,
        text="Calculate Sunrise and Sunset by Getting Your Location",
        font=("Helvetica",10),
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
        text="✒Font",
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
        text="🕷Spider",
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
        InputWindow = tk.Toplevel()
        InputWindow.title("Enter URL.")
        InputWindow.geometry("256x96")
        InputWindow.resizable(0,0)
        tk.Label(InputWindow,text="Enter URL").pack(side="top")
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
        URLlist.delete(0)

    tk.Button(SpiderConf,text="➕",command=AddUrl).pack(side="left")
    tk.Button(SpiderConf,text="➖",command=DelUrl).pack(side="left")

    '''Stopwords Editing'''
    def stopword():
        swSetForm = tk.Toplevel()
        swSetForm.geometry("320x256")
        swSetForm.resizable(0,0)
        swSetForm.title("Stopwords Settings")
        
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
            InputWindow.resizable(0,0)
            
            tk.Label(InputWindow,text="Input Stop Word").pack(side="top")
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
            Stoplist.delete(0)
            _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Updated StopWords Lists"))
        tk.Button(swSetForm,text="➕",command=Add).pack(side="left")
        tk.Button(swSetForm,text="➖",command=Del).pack(side="left")
        swSetForm.mainloop()
        


    tk.Button(SpiderConf,text="🚫Stopwords Settings",command=stopword).pack(side="left")
    SpiderConf.pack(ipadx="2",side="top")

    '''Setting GUI Auto Refresh And Save'''
    def ApplyRefresh(threadname,delay):
        while(1):
            print(Position)
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
            "StopWords":StopWords
        })
        print(profile)
        open(os.path.expanduser('~')+"\\.Mashiro\\settings.json","w",encoding="utf-8-sig").write(profile)
        MainWin.destroy()
    MainWin.protocol("WM_DELETE_WINDOW", save)
    MainWin.mainloop()
