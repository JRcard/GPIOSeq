

import wx, os
from constants import *
from variables import *
from Template import *
from Grid import *
from widgets import *

class Scene(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)    
        self.SetBackgroundColour("#666666")
        mainSize = wx.BoxSizer(wx.VERTICAL)
        
######## BUTTON BAR #########

        buttonSize = wx.BoxSizer(wx.HORIZONTAL)
        zoomSize = wx.BoxSizer(wx.HORIZONTAL)
        transpSize = wx.BoxSizer(wx.VERTICAL)
        
        self.connect = wx.CheckBox(self,id=-1, label="Connect")
        self.Bind(wx.EVT_CHECKBOX, self.onConnect, self.connect)
        
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
        zoomSize.Add(self.connect, 0, wx.RIGHT, 3)
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
    def onConnect(self,e):
         
        if self.connect.GetValue() == 1:
#            os.system(PASSWORD + "|" + RASPI)        #### je ne réussit pas a me connecter... je cherche encore la solution
            print "connection fail....!!!!!"

        
             
    def onStart(self,e):
        if self.playStop.GetLabel() == "Play":
            print "go!!"
            self.playStop.SetLabel("Stop")
            
            prepareDictGPIO()
            print "DICTIONNARY!!!", dictGPIO
            
            # Generation du texte du Sequenceur que je met dans mes documents (voir constants.py) 
            # c'est le fichier que je voudrais pousser vers le Raspi et faire jouer ensuite..... 
            
            text = SETUP % (str(dictGPIO))  
            text += SEQUENCE
            pathFile = os.path.join(TEMPDIR, TEMPFILE)
            f = open(pathFile, "w")
            f.write(text)
            f.close() 
            clearDictGPIO()
                                      
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
        
            