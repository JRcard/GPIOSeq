# encoding: utf-8

import wx, os, sys
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
        ## j'ai passé vraiment beaucoup de temps à analyser et a essayer plein de façon pour avoir une scrollbar et rien n'y fait...
        ## aussi je souhaiterais que la scrollBar soit local sur ma grid et non sur le main_frame.
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
        
        if not self.isPrefFilled():
            self.onPref(e)
            self.login.SetValue(0)
            
        elif self.login.GetValue() == 1 and self.isPrefFilled():

            try:
                self.sshLogin = px.pxssh()
                self.sshLogin.force_password = True
                self.sshLogin.login(PREFS["REMOTE_HOST"],PREFS["REMOTE_USER"],PREFS["REMOTE_PASS"],auto_prompt_reset=False)
                print "step: 1 Raspi login!"
                
            except px.ExceptionPxssh,e:
                ## il me reste encore des trucs a apprendre sur la gestion de certaines erreurs de login dans pexpect. 
                ## Je devrai créer plein de problemes et pour ensuite créer les msg qui s'y rattache.
                dlg = wx.MessageDialog(self, "Fail on login: " + str(e) + "\nLook in the login preferences.", style=wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()
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
                localPathFile = os.path.join(TEMPDIR, TEMPFILE)
                print localPathFile
                f = open(localPathFile, "w")
                f.write(text)
                f.close() 
                clearDictGPIO()
                
    ###################################### Transfer file ###################           
                self.sshLogin.expect("$")
                self.sshLogin.sendline("scp " + LOCAL_HOST + ":" + localPathFile + " " + REMOTE_DIR)
                
    #####################################################################################################
            ### si c'est la premiere fois que le raspberry est connecté en ssh avec l'ordinateur de l'utilisateur
            ### je ne peux plus le tester... ou bien c'est mal monté car ça ne fonctionne pas... à suivre.
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
                self.sshLogin.expect("$")
                self.sshLogin.sendline("sudo python " + TEMPFILE)
                print "RUUUN!"
#                self.sshLogin.prompt()
#                print self.sshLogin.before
                
                
            else:
                ### Ne fonctionne pas... Comment envoyer une commande dans le raspberry pour arrêter un process... 
                ### l'équivalent du ctrl+C directement dans le terminal....
                remotePathFile = os.path.join(REMOTE_DIR, TEMPFILE)
                self.playStop.SetLabel("Play")
                print "stoped"
                self.sshLogin.sendline("killall -9 python")
                self.sshLogin.expect("$")
                self.sshLogin.sendline("rm" + remotePathFile)
                os.remove(TEMPFILE)
                ## TO DO tempfile for gpio.cleanup()
                
        else:
            dlg = wx.MessageDialog(self, "you must be log in to start the Seq", style=wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.onPref(e)
            print "you must be log in to start the Seq"

    def onLoop(self,e):
        if self.loop.IsChecked():
            print "Looooping!!"
        else:
            print "Straight" 

    def onZoom(self,e):
        zoom = self.zoom.GetValue()
        self.grid.setZoom(zoom)
        self.grid.sizer.Show(self,True)
        w,h = self.grid.GetMinSize()
        self.SetVirtualSize((w*zoom,h))
        self.grid.Refresh()
        
    def onPref(self,e):

        dlg = PrefDlg(self)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.setPref()
            self.login.SetValue(1)
            self.onLogin(e)


        dlg.Destroy()
        
    def isPrefFilled(self):
        if PREFS["REMOTE_USER"] == "" or PREFS["REMOTE_HOST"] == "" or PREFS["REMOTE_PASS"] == "" or PREFS["LOCAL_PASS"] == "":
            return False
        else:
            return True
            