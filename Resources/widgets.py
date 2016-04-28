# encoding: utf-8

import wx
from constants import *
from variables import *

## Je sais que ça fait plus d'une fois qu'on en jase.... mais je ne saisi pas encore la logique....
## Présentement mon rectangle ne donne plus du tout les bonnes valeurs de absStart stop et AbsWidth... voir les méthodes:getAbsStart,getAbsStop,getAbsWidth
## j'avais réussit à changer les rectangles de place grace au zoom. mais il ne revenais plus à leur place quand je "dézoomais"
## et la marge que je laisse pour les TRACKNAME me cause de beaux maux de tête. Je me demande si les NAMETRACK n'étaient pas mieux à l"extérieur de ma grid

class Rectangle(wx.Rect):
    
    def __init__(self, X=0, Y=0, width=0, heigth=GRID_STEP):
        wx.Rect.__init__(self, X, Y, width, heigth)
        self.X = X
        self.Y = Y
        self.width = width
        self.heigth = heigth
        

    def draw(self,dc,zoom,pen,brush): 
        dc.SetPen(wx.Pen(pen,1)) 
        dc.SetBrush(wx.Brush(brush)) 
        dc.DrawRectangle(self.X*zoom,self.Y,self.width*zoom,self.heigth)

        
    def getTrackNum(self):
        self.trackNum = self.Y / self.heigth - 1 
        return self.trackNum
                
    def getAbsStart(self):
        return self.X * TIMELINE_UNIT
        
    def getAbsStop(self):
        return (self.X + self.width) * TIMELINE_UNIT
        
    def getAbsWidth(self):
        return self.width * TIMELINE_UNIT

        

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
            self.button.SetLabel(dlg.getText())

        dlg.Destroy()
        

class Zoom(wx.SpinCtrl):
    def __init__(self, parent, id):
        wx.SpinCtrl.__init__(self, parent=parent, id=id, size=(40,20), value="1", min=1, max=5, name="Zoom")
        
    
    
    
    