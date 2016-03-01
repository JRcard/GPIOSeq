# encoding: utf-8

import wx
from constants import *
from variables import *

class Rectangle(wx.Rect):
    
    def __init__(self, startX=0, trackY=0, width=0, heigth=GRID_STEP):
        wx.Rect.__init__(self, startX, trackY, width, heigth)
        self.startX = startX
        self.trackY = trackY
        self.width = width
        self.heigth = heigth
        
        
    def draw(self,dc): 
        dc.SetPen(wx.Pen("#FFFFFF",1)) 
        dc.SetBrush(wx.Brush("#0000AA")) 
        dc.DrawRectangleRect(self)
       
    def isInside(self,x):
        return self.Contains(x)
        
    def getStart(self):
        return self.startX
        
    def getStop(self):
        return self.startX + self.width
        
    def getTrackNum(self):
        self.trackNum = self.trackY / GRID_STEP - 1 
        return self.trackNum
        
    def getWidth(self):
        return self.width
        
    def setStart(self,x):
        self.startX = x
        
    def setTrack(self,y):
        self.trackY = y
        
    def setWidth(self,z):
        self.width = z - self.startX
        

class TrackNameDlg(wx.Dialog):
    def __init__(self, parent, title, track):
                
        wx.Dialog.__init__(self, parent=parent, title="Name your pin", style=wx.DEFAULT_DIALOG_STYLE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.label = wx.StaticText(self, -1, "Name your GPIO %d" % track)
        self.text = wx.TextCtrl(self, -1, "", size=(80,20))
        
        sizer.Add(self.label, 0, wx.TOP|wx.ALL, 5)
        sizer.Add(self.text, 1, wx.BOTTOM|wx.ALL, 10)
        
        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def getText(self):
        return self.text.GetValue()


class Track(wx.Panel):
    def __init__(self, parent, id, name, pos, size):
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size)
        self.SetBackgroundColour("#AAAAAA")
        
        self.parent = parent
        self.id = id
        self.name = name
        self.pos = pos
        self.size = size
        
        self.trackNum = ((self.pos[1] - TRACKNAME_POS[1]) / GRID_STEP) + 1
        
        self.button = wx.Button(self, -1, self.name, style=wx.BORDER_NONE|wx.BU_EXACTFIT)       
        self.Bind(wx.EVT_BUTTON, self.onButton, self.button)
        
        
    def onButton(self,e):
        
        dlg = TrackNameDlg(self, -1, self.trackNum)

        if dlg.ShowModal() == wx.ID_OK:
            self.name = dlg.getText()
            self.button.SetLabel(self.name)

        dlg.Destroy()