

import wx
from constants import *
from Grid import *
from widgets import Track

class Scene(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)    
        self.SetBackgroundColour("#666666")
        
######## BUTTON BAR #########

        self.transpText = wx.StaticText(self, id=-1, label="Transport", pos=(185,1))
        
        self.playStop = wx.Button(self, id=-1, label="Play", pos=(120,19))
        self.Bind(wx.EVT_BUTTON, self.onStart, self.playStop)
        
        self.loop = wx.CheckBox(self, id=-1, label="loop", pos=(228,24))
        self.Bind(wx.EVT_CHECKBOX, self.onLoop, self.loop)
        
######## TIMELINE #####


######## TRACKNAME @@@@@@

        for i in range(TRACK_TOTAL):
            self.track = Track(self,-1, 
                               "GPIO%02d" % (i+1), 
                               pos=(TRACKNAME_POS[0],TRACKNAME_POS[1]+(i*GRID_STEP)), 
                               size=(59,19))

######## GRID ##########

        self.grid = Grid(self, pos=GRID_POS, size=GRID_SIZE)
        
######## METHODES      
    def onStart(self, evt):
        if self.playStop.GetLabel() == "Play":
            print "go!!"
            self.playStop.SetLabel("Stop")
                                      
        else:
            self.playStop.SetLabel("Play")
            print "stoped"
            
    def onLoop(self, evt):
        if self.loop.IsChecked():
            print "Looooping!!"
            
        else:
            print "Straight" 
            