#!/usr/bin/python3
#
#   Mashiro (Win32 ver.)
#   Version:    DEV05 4rd UPDATE
#  
#   (C)Copyright 2020 RYOUN & the Mashiro Developers
#
#   mSet.py: mGenerate Needed Functions and Classes
#

import win32api,os,win32con,traceback,json

# Error Output
def errexec(returnInfo:str,Exit:bool):
    #tkm.showerror("Error",returnInfo)
    win32api.MessageBox(0,returnInfo,"OOPS!",win32con.MB_ICONERROR)
    if(Exit == True):
        exit()

# Store the user configuration
class SETTINGS:
    #Background Color
    Color:list = [1,"white"]
    #The Margin Of The Words
    Margin:int
    #The Font Path
    Font:str
    #The Resolution of Screen
    Resolution = [1024,768]
    #Mask Image
    Mask:str
    #Auto Refresh Interval
    AutoRefresh:int
    #The URL for the spider crawling information.
    Spiders:list
    #Words that are not allowed to appear
    StopWords:list
    #The Coordinates of Your location
    #You Can Disable This In The Setting Profile
    #We Need Your Location To Calculate Sunrise And Sunset time
    Position:list = [False,[0,0,0],[0,0,0]]
    # Position[0]:Enable
    # Position[1]:latitude  | [0][0] Degrees | [0][1] Cents
    # Position[2]:longitude | [1][0] Degrees | [1][1] Cents    

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
                #If You Disabled This,We Will Set The Default Latitude And Longitude 0°,0°
                #This won't affect anything         

        except IOError:
            errexec("Failed To Read File \""+ os.path.expanduser('~')+"\\.Mashiro\\settings.json" +"\"",1)

        except:
            errexec(traceback.format_exc(),1)
