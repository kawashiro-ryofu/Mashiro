#!/usr/bin/python3
#  
#   Mashiro (Developing Version)
#   Licence Under MIT
#
#   (C)Copyright 2020 Team-RYOUN(Jeffery_Yu)
#

import tkinter as tk
# settings:
# Element 0:refresh (int)
# Element 1:maskImg { Element 0:Enable(0/1)
#                     Element 1:Img(if settings[0][1] isn't 1,this Element is 0.Or it will be a string of the directory)
#
#

settings = [0,[0,0]]


def main():
    #MainWindow
    Menu = tk.Tk()
    Menu.title("Mashiro Configuration")
    Menu.geometry("640x480")
    Menu["background"] = "black"

    #Title
    title = tk.Frame(Menu)
    tk.Label(title,text="🔧Configuration",bg="cyan",fg="black",font=("Arial",30)).pack(side="top",ipadx="3")
    title.pack(side="top")
 
    #Auto Refresh
    refresh = tk.Frame(Menu)
    tk.Label(Menu,text="Refresh Frequency",font=("Helvetica",15), fg="cyan",bg="black").pack()
    def freqScale(value):
        settings[0] = int(value)
        print(settings)
    autoRefresh = tk.Scale(refresh,label="Auto Refresh Frequency(minute)",from_=10,to=120,orient="horizontal",length=500,bg="black",fg="cyan",command=freqScale)
    autoRefresh.pack(side="top")
    refresh.pack(ipadx="2",side="top")
    
    '''
    
    Still Developing...

    #Wordcloud Mask Image
    maskImg = tk.Frame(Menu)
    enable = tk.IntVar()
    #Checkbox Status Updating
    def maskChk():
        settings[1][0] = enable.get()
    tk.Label(Menu,text="Word Cloud Masking Image",font=("Helvetica",15), fg="cyan",bg="black").pack()
    #if mask disabled,the output image is full of words
    mask = tk.Checkbutton(maskImg,text="Enable",fg="cyan",bg="black",variable=enable,onvalue=1,offvalue=0,command=maskChk)
    mask.pack()
    maskImg.pack(side="top")
    '''

    Menu.mainloop()
    #2do




if __name__ == "__main__":
    main()
