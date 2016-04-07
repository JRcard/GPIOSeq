#!/usr/bin/env python
# encoding: utf-8

import wx
from Menu import *
from Scene import *
#from Toolbar import *


class SeqFrame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.scene = Scene(self)

######## MENU ################
        self.menu = SeqMenu(self)
        self.SetMenuBar(self.menu)

######## TOOL BAR ############ 
        #self.tb = Tb(self.scene)

######## create status bar ###

        status = self.CreateStatusBar()

######## METHODES ############  

        self.Maximize()
        self.Show()

