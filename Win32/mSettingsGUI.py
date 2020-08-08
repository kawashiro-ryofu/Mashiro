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
setting = mSet.SETTINGS()

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

def LocationEnable():
    if(EnableLocating.get() == 1):
        Position[0] = True
        NowLoc.pack()
        _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Locating Enabled"))
    else:
        Position[0] = False
        NowLoc.pack_forget()
        _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Locating Disabled"))

tk.Checkbutton(
    locationConf,
    text="Calculate Sunrise and Sunset by Getting Your Location",
    font=("Helvetica",10),
    variable=EnableLocating,
    command=LocationEnable,
).pack(ipadx="2",side="top")

locrq = requests.get("http://ip-api.com/json")
city:str
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
    Position[1] = f2s(latitude)
    Position[2] = f2s(longitude)
    NowLoc = tk.Label(locationConf,text=city)
        


locationConf.pack()
ColorConf.pack(ipadx="2",side="top")

# There are few problems to be solve.
# In Three Words, We Need Help
#
#Current Default font:
#    English(en_US en_AU en): Lucida Sana(C:\\Windows\\l_10646.ttf)
#    Chinese(zh_CN): MS-YaHei(C:\\Windows\\MSYH.ttc)    (zh_TW 如果台湾版自带微软雅黑字体，否则就用黑体)
#    Japaneese(ja):MS UI Gothic(C:\\Windows\\msgothic.ttc)
#   To Be Continued...
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
URLlist = tk.Listbox(
    URLlistPart,
    selectmode="MUTIPLE",
    height=5,
    width=20
)
for i in range(len(Spider)):
    URLlist.insert("end",Spider[i])
scrollbar = tk.Scrollbar(URLlistPart)
scrollbar.config(command=URLlist.yview)
scrollbar.pack(side="right",fill="y")
URLlist.pack(ipadx=2,side="left")
URLlistPart.pack()
'''URL List Editing'''
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
    a = URLlist.curselection()[0]
    del(Spider[a])
    _thread.start_new_thread( TitleEffact, ("TitleEffact", 0,"Delete URL success"))
    URLlist.delete(0)

tk.Button(SpiderConf,text="➕",command=AddUrl).pack(side="left")
tk.Button(SpiderConf,text="➖",command=DelUrl).pack(side="left")
SpiderConf.pack(ipadx="2",side="top")


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
_thread.start_new_thread( ApplyRefresh, ("Thread-0", 0.1))

MainWin.mainloop()
