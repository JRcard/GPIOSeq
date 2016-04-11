# encoding: utf-8

import wx, os
from constants import *
from variables import *
from Template import *
from Grid import *
from widgets import *
from pexpect import pxssh as px
from Pref import *

class Scene(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)    
        self.SetBackgroundColour("#666666")
        mainSize = wx.BoxSizer(wx.VERTICAL)
        
        self.sshLogin = None
 
######## BUTTON BAR #########
        self.login = wx.CheckBox(self,id=-1, label="Login")
        self.Bind(wx.EVT_CHECKBOX, self.onLogin, self.login)

        self.playStop = wx.Button(self, id=-1, label="Play")
        self.Bind(wx.EVT_BUTTON, self.onStart, self.playStop)

        self.loop = wx.CheckBox(self, id=-1, label="loop")
        self.Bind(wx.EVT_CHECKBOX, self.onLoop, self.loop)

        self.zoomText = wx.StaticText(self, id=-1, label="Zoom")
        self.zoom = Zoom(self, -1)   
        self.Bind(wx.EVT_SPINCTRL, self.onZoom, self.zoom)
        self.Bind(wx.EVT_TEXT, self.onZoom, self.zoom) 
        
        self.pref = wx.Button(self, id=-1, label="Login Prefs")
        self.Bind(wx.EVT_BUTTON, self.onPref, self.pref)
        
######## TIMELINE #####


######## TRACKNAME @@@@@@
        trackSize = wx.BoxSizer(wx.VERTICAL)
        TRACKS = []
        for i in range(TRACK_TOTAL):
            self.track = Track(self,-1, 
                               "GPIO%02d" % (i+1), 
                               pos=(TRACKNAME_POS[0],TRACKNAME_POS[1]+(i*GRID_STEP)), 
                               size=(59,GRID_STEP-1))

            TRACKS.append(self.track)
            trackSize.Add(TRACKS[i],0,wx.TOP,1)


######## GRID ##########
        self.grid = ScrollGrid(self, pos=GRID_POS, size=GRID_SIZE)


######## SIZERS #############
        buttonSize = wx.BoxSizer(wx.HORIZONTAL)
        zoomSize = wx.BoxSizer(wx.HORIZONTAL)
        transpSize = wx.BoxSizer(wx.VERTICAL)
        self.gridSize = wx.BoxSizer(wx.HORIZONTAL)
        
        buttonSize.Add(self.pref, 0, wx.RIGHT, 42)
        buttonSize.Add(self.playStop)
        buttonSize.Add(self.loop, 0, wx.LEFT, 5)
        zoomSize.Add(self.login, 0, wx.RIGHT, 140)
        zoomSize.Add(self.zoom)
        zoomSize.Add(self.zoomText)

        transpSize.Add(buttonSize, 0, wx.ALL, 10)
        transpSize.Add(zoomSize, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        self.gridSize.Add(trackSize,0,wx.TOP, 40)
        self.gridSize.Add(self.grid)
        
        mainSize.Add(transpSize, 0, wx.ALL, 5)
        mainSize.Add(self.gridSize,0,wx.ALIGN_CENTER|wx.TOP,40)
        
        self.SetSizer(mainSize)

######## METHODES 
    def onLogin(self,e):
        
## TO DO: error flag if any of the prefs are wrong!!! ###

        if not self.isPrefFilled():
            self.onPref(e)
            
        elif self.login.GetValue() == 1 and self.isPrefFilled():

            try:
                self.sshLogin = px.pxssh()
                self.sshLogin.force_password = True
                self.sshLogin.login(PREFS["REMOTE_HOST"],PREFS["REMOTE_USER"],PREFS["REMOTE_PASS"],auto_prompt_reset=False)
                print "step: 1 Raspi login!"
                #to do:  témoin visuel de connectivité
                
            except px.ExceptionPxssh,e:
                print "Fail on login"
                print str(e)
                    

                
        if self.login.GetValue() == 0 and self.sshLogin is not None:
            self.sshLogin.logout()
            print "Raspi logout!"



    def onStart(self,e):
        if self.login.GetValue() == 1:
            if self.playStop.GetLabel() == "Play":
                print "go!!"
                self.playStop.SetLabel("Stop")
                
                prepareDictGPIO()
                print "DICTIONNARY!!!", dictGPIO 
                
                text = SETUP % (str(dictGPIO))
                text += SEQUENCE
                pathFile = os.path.join(TEMPDIR, TEMPFILE)
                print pathFile
                f = open(pathFile, "w")
                f.write(text)
                f.close() 
                clearDictGPIO()
                
    ###################################### Transfer file ###################           
                #self.login.expect("$")
                self.sshLogin.sendline("scp " + LOCAL_HOST + ":" + pathFile + " " + REMOTE_DIR)
                
            #    if s.expect("are you sure you want to continue connecting"):
            #        s.sendline("yes")
            #        print "I said yes"
            ################################### PASSWORDLOCAL ############

                self.sshLogin.expect("Password:")
                self.sshLogin.sendline(PREFS["LOCAL_PASS"])
                print "password? Local password"
                print
                print "File tranfered"
    ###################################### Transfer file end #################   
               # TODO: delete tempFile
                self.sshLogin.expect("$")
                self.sshLogin.sendline("sudo python " + TEMPFILE)
                print "RUUUN!"
    #            self.sshLogin.prompt()
    #            print self.sshLogin.before
                
            else:
                self.playStop.SetLabel("Play")
                print "stoped"
                self.sshLogin.sendline("Ctrl+C")
                ## TO DO tempfile for gpio.cleanup()
                
        else:
            dlg = wx.MessageDialog(self, "you must be log in to start the Seq")
            dlg.ShowModal()
            dlg.Destroy()
            print "you must be log in to start the Seq"

    def onLoop(self,e):
        if self.loop.IsChecked():
            print "Looooping!!"
        else:
            print "Straight" 

    def onZoom(self,e):
        zoom = self.zoom.GetValue()
        self.grid.setZoom(zoom)
        w,h = self.grid.GetMinSize()
        self.SetVirtualSize((w*zoom,h))
        self.grid.Refresh()
        
    def onPref(self, e):
        ## TO DO: error flag if any of the prefs are wrong!!! ###
        dlg = PrefDlg(self)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.setPref()
            self.login.SetValue(1)
            self.onLogin(e)
            
        elif dlg.ShowModal == wx.ID_CANCEL:
            if self.login.GetValue() == 1:
                self.login.SetValue(0)

        dlg.Destroy()
        
    def isPrefFilled(self):
        if PREFS["REMOTE_USER"] == "" or PREFS["REMOTE_HOST"] == "" or PREFS["REMOTE_PASS"] == "" or PREFS["LOCAL_PASS"] == "":
            return False
        else:
            return True
            