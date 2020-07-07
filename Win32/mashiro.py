# !/usr/bin/bash
#
#   Mashiro (Windows)
#   (C)RYOUN 2020
#
#   It Is In Developing!
#

import wx

class Main:
    def configure(self):
        conf = wx.App()
        root = wx.Frame(None, title = "Mashiro Configuration", size = (640,480))
        settings = wx.Panel(root)
        label = wx.StaticText(settings, label = "It Is In Developing", pos = (150,100))
        root.Show(True)
        conf.MainLoop()

    def main(self):
        self.configure()



if __name__ == "__main__":
    Mashiro = Main()
    Mashiro.main()