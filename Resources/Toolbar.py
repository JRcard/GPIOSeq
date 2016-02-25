#!/usr/bin/env python
# encoding: utf-8

import wx

class Tb(wx.ToolBar):
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent)
        
        self.tsize = (30,30)

        self.new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, self.tsize)
        self.open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, self.tsize)
        self.save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, self.tsize)

        #self.play_bmp = wx.BitmapFromImage(wx.Image("Icons/Play.png").Scale(30,30))
        #self.stop_bmp = wx.BitmapFromImage(wx.Image("Icons/Stop.png").Scale(30,30))
        #self.straight_bmp = wx.BitmapFromImage(wx.Image("Icons/Next.png").Scale(30,30))
        #self.loop_bmp = wx.BitmapFromImage(wx.Image("Icons/Reload.png").Scale(30,30))
        
        
        self.AddLabelTool(10, "New", self.new_bmp, shortHelp="New", longHelp="create a New File")
        self.AddLabelTool(11, "Open", self.open_bmp, shortHelp="Open", longHelp="Open a saved file")
        self.AddLabelTool(12, "Save", self.save_bmp, shortHelp="Save", longHelp="Save your work")  
        self.AddSeparator()      
        #self.AddLabelTool(13, "Play", self.play_bmp, shortHelp="Start", longHelp="Start the sequence")
        #self.AddLabelTool(14, "Stop", self.stop_bmp, shortHelp="Stop", longHelp="Stop the sequence")
        #self.AddLabelTool(15, "Straight", self.straight_bmp, shortHelp="Straight", longHelp="Play the sequence straight and stop at the end")
        #self.AddLabelTool(16, "Loop", self.loop_bmp, shortHelp="Loop", longHelp="Loop the sequence")
        #self.AddCheckTool(17, "Loop", self.loop_bmp, shortHelp="loop", longHelp="LOOOOOOPING!!" )
    

        self.Bind(wx.EVT_TOOL, self.onNew, id=10)
        self.Bind(wx.EVT_TOOL, self.onOpen, id=11)
        self.Bind(wx.EVT_TOOL, self.onSave, id=12)        
        #self.Bind(wx.EVT_TOOL, self.onPlay, id=13)
        #self.Bind(wx.EVT_TOOL, self.onStop, id=14)
        #self.Bind(wx.EVT_TOOL, self.onStraight, id=15)
        #self.Bind(wx.EVT_TOOL, self.onLoop, id=16)
        #self.Bind(wx.EVT_TOOL, self.onLoop, id=17)
        
        self.SetToolBitmapSize(self.tsize)
        self.Realize()

##############################################

     
    def onNew(self,e):
        print "choose a new file"
        
    def onOpen(self,e):
        """Open a file"""
        self.dirname = ' '
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, " ", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), "r")
            f.close()  
        dlg.Destroy()
        
    def onSave(self,e):
        self.dirname = ' '
        dlg = wx.FileDialog(self, "Save your file", self.dirname, " ", "*.*", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            itcontains = self.text.GetValue()
            
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            filehandle = open(os.path.join(self.dirname, self.filename), "w")
            filehandle.write(itcontains)
            filehandle.close()
            
        dlg.Destroy()
        

    #def onLoop(self,e):
    #    print "looooping"
        
##############################################


#    def onPlay(self,e):
#        print "go!!"
#        
#    def onStop(self,e):
#        print "stop!!"
#        
#    def onLoop(self,e):
#        print "looooooooping!!"
#
#    def onStraight(self,e):
#        print "Stop at the end!!!" 
         
