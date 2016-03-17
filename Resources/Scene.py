

import wx
from constants import *
from Grid import *
from widgets import Zoom

class Scene(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)    
        self.SetBackgroundColour("#666666")
        mainSize = wx.BoxSizer(wx.VERTICAL)
        
######## BUTTON BAR #########

        buttonSize = wx.BoxSizer(wx.HORIZONTAL)
        zoomSize = wx.BoxSizer(wx.HORIZONTAL)
        transpSize = wx.BoxSizer(wx.VERTICAL)
        
        self.playStop = wx.Button(self, id=-1, label="Play")
        self.Bind(wx.EVT_BUTTON, self.onStart, self.playStop)
        
        self.loop = wx.CheckBox(self, id=-1, label="loop")
        self.Bind(wx.EVT_CHECKBOX, self.onLoop, self.loop)

        self.zoomText = wx.StaticText(self, id=-1, label="Zoom")        
        self.zoom = Zoom(self, -1)   
        self.Bind(wx.EVT_SPINCTRL, self.onZoom, self.zoom)
        self.Bind(wx.EVT_TEXT, self.onZoom, self.zoom)     

        buttonSize.Add(self.playStop)
        buttonSize.Add(self.loop)
        zoomSize.Add(self.zoom)
        zoomSize.Add(self.zoomText)
        
        transpSize.Add(buttonSize, 0, wx.ALL, 5)
        transpSize.Add(zoomSize, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        mainSize.Add(transpSize, 0, wx.ALL, 5)
        
######## TIMELINE #####


######## TRACKNAME @@@@@@


######## GRID ##########
        gridSize = wx.BoxSizer(wx.VERTICAL) 
        
        self.grid = Grid(self, pos=GRID_POS, size=GRID_SIZE)
        
        mainSize.Add(self.grid,0,wx.ALIGN_CENTER|wx.TOP, 60)
        
        self.SetSizer(mainSize)
######## METHODES      
    def onStart(self,e):
        if self.playStop.GetLabel() == "Play":
            print "go!!"
            self.playStop.SetLabel("Stop")
                                      
        else:
            self.playStop.SetLabel("Play")
            print "stoped"
            
    def onLoop(self,e):
        if self.loop.IsChecked():
            print "Looooping!!"
            
        else:
            print "Straight" 
            
    def onZoom(self,e):
        zoom = self.zoom.GetValue()
        self.grid.setZoom(zoom)
        self.grid.Refresh()
        
            