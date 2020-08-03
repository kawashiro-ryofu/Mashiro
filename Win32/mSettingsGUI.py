import tkinter as tk
import tkinter.colorchooser as tkcolor
import tkinter.filedialog as tkfile
import tkinter.font as tkfont
from tkinter import ttk
import mSet
import json
import _thread
import time
import fontname



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

LeftPart = tk.Frame(MainWin)

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

'''Heading'''
tk.Label(
    MainWin,
    text="🔧Settings",
    font=("Arial",30)
    ).pack(side="top",ipadx="3")

'''Auto Refresh Interval'''
refresh = tk.Frame(LeftPart)
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
ColorConf = tk.Frame(LeftPart)
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
ColorConf.pack(ipadx="2",side="top")
'''Font Setting'''
FontConf = tk.Frame(LeftPart)
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

'''Automatic save the configuration file'''
def ApplyRefresh(threadname,delay):
    while(1):
        print(AutoRefresh.get(),end=';')
        print(ColorDayLight.get())
        if(ColorDayLight.get() != 1):
            ChooseColor.pack(side="right")
            ColorMoniter["bg"] = Color.get()
            ColorMoniter.pack(side="left")
        else:
            ChooseColor.pack_forget()
            ColorMoniter.pack_forget()
        time.sleep(delay)
_thread.start_new_thread( ApplyRefresh, ("Thread-0", 0.1))

LeftPart.pack(side="left")

MainWin.mainloop()