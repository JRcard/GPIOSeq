# encoding: utf-8

import os, socket, getpass, wx

REMOTE_DIR = "/home/pi"
LOCAL_HOST = getpass.getuser() + "@" + socket.gethostname() + ".local"

TEMPFILE = "tempGPIOSeq.py"
TEMPDIR = os.getcwd()
#PREFS = {"REMOTE_USER": "", "REMOTE_HOST": "", "REMOTE_PASS": "", "LOCAL_PASS":""}
PREFS = {"REMOTE_USER": "pi", "REMOTE_HOST": "thebat.local", "REMOTE_PASS": "protools", "LOCAL_PASS":"protools10.30"}

class PrefDlg(wx.Dialog):
    def __init__(self, parent, title="Login Prefs"):                  
        wx.Dialog.__init__(self, parent=parent, title=title)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.piUserLabel = wx.StaticText(self, -1, "Pi Username")
        self.piUserText = wx.TextCtrl(self, -1, "%s" % PREFS["REMOTE_USER"], size=(80,20))
        self.piHostLabel = wx.StaticText(self, -1, "Pi Hostname (ends with .local or just the Ip adress)")
        self.piHostText = wx.TextCtrl(self, -1, "%s" % PREFS["REMOTE_HOST"], size=(80,20))
        self.piPassLabel = wx.StaticText(self, -1, "Pi Password")
        self.piPassText = wx.TextCtrl(self, -1, "%s" % PREFS["REMOTE_PASS"], style=wx.TE_PASSWORD)
        self.localPassLabel = wx.StaticText(self, -1, "Local Password")
        self.localPassText = wx.TextCtrl(self, -1, "%s" % PREFS["LOCAL_PASS"], style=wx.TE_PASSWORD)
        
        sizer.Add(self.piUserLabel, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(self.piUserText, 1, wx.BOTTOM|wx.LEFT, 5)
        sizer.Add(self.piHostLabel, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(self.piHostText, 1, wx.BOTTOM|wx.LEFT, 5)
        sizer.Add(self.piPassLabel, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(self.piPassText, 1, wx.BOTTOM|wx.LEFT, 5)
        sizer.Add(self.localPassLabel, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(self.localPassText, 1, wx.BOTTOM|wx.LEFT, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.Add(btn)

        btn2 = wx.Button(self, wx.ID_CANCEL)
        btnsizer.Add(btn2,0,wx.LEFT,15)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL| wx.TOP|wx.LEFT, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def setPref(self):
        PREFS["REMOTE_USER"] = self.piUserText.GetValue()
        PREFS["REMOTE_HOST"] = self.piHostText.GetValue()
        PREFS["REMOTE_PASS"] = self.piPassText.GetValue()
        PREFS["LOCAL_PASS"] = self.localPassText.GetValue()
        
        print PREFS