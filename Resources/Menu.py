#!/usr/bin/env python
# encoding: utf-8

import os
import wx
from Grid import *
from Scene import *
from Template import *
from variables import *


class SeqMenu(wx.MenuBar):
    
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        
        self.parent = parent
        
        # create each menu itself who will go on the menu bar

        self.file = wx.Menu()
        self.edit = wx.Menu()
        self.help = wx.Menu()

        # Put the "File" menu on the menu bar and put action in this menu           
        self.Append(self.file, "&File")
        self.menuNew = self.file.Append(wx.ID_NEW, "&New", "New file")
        self.menuOpen = self.file.Append(wx.ID_OPEN, "&Open...", "Open a file")
        self.menuSave = self.file.Append(wx.ID_SAVE, "&Save\tCtrl+S", "Save a File")
        self.file.AppendSeparator()
        self.menuExport = self.file.Append(100, "Export\tCtrl+E", "Export data")
#        self.file.AppendSeparator()
#        self.menuPref = self.file.Append(101,"Preferences\tCtrl+,", "Path and login preferences")
        self.file.AppendSeparator()
        self.menuExit = self.file.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
                
        # Put the "Edit" menu on the menu bar and put action in this menu   
        # TO DO: Undo, Redo        
        self.Append(self.edit, "&Edit")
        self.menuCopy = self.edit.Append(wx.ID_COPY, "&Copy", "Copy the selection")
        self.menuPaste = self.edit.Append(wx.ID_PASTE, "&Paste", "Paste the last copy")

        # Put the "Help" menu on the menu bar and put action in this menu   
        self.Append(self.help, "&Help")
        self.menuHelp = self.help.Append(wx.ID_ABOUT, "&About", "Information about this program")

###### Binding menu bar ##########
        # FILE
        self.Bind(wx.EVT_MENU, self.onNew, self.menuNew)
        self.Bind(wx.EVT_MENU, self.onOpen, self.menuOpen)
        self.Bind(wx.EVT_MENU, self.onSave, self.menuSave)
        self.Bind(wx.EVT_MENU, self.onExit, self.menuExit)
        self.Bind(wx.EVT_MENU, self.onExport, self.menuExport, id=100)
#        self.Bind(wx.EVT_MENU, self.onPref, self.menuPref, id=101)
        
        # EDIT  ##
        
        # TO DO: Undo, Redo
        #self.Bind(wx.EVT_MENU, self.onCopy, self.menuCopy)
        #self.Bind(wx.EVT_MENU, self.onPaste, self.menuPaste)
        
        # HELP 
        self.Bind(wx.EVT_MENU, self.onAbout, self.menuHelp)
        
########   MENU  -------methods-------  ##########

    def onExit(self, e):
#        if self.grid.sshLogin is not None:
#            self.grid.sshLogin.logout()
#        dlg = wx.MessageDialog(self, 
#            "Do you really want to close this application?",
#            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
#        result = dlg.ShowModal()
#        dlg.Destroy()
#        if result == wx.ID_OK:
        self.parent.Destroy()
        
    def onExport(self, e):
       
        # Ecriture du fichier
        self.dirname = ' '
        dlg = wx.FileDialog(self, "Export your file", self.dirname, "", "*.py", wx.SAVE | wx.OVERWRITE_PROMPT)
        if  dlg.ShowModal() == wx.ID_OK:
            prepareDictGPIO()
            print "DICTIONNARY!!!", dictGPIO
            
            # Generation du texte du Sequenceur
            text = SETUP % (str(dictGPIO))  
            text += SEQUENCE
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), "w")
            f.write(text)
            f.close()   
            clearDictGPIO()
        dlg.Destroy()

    
    def onNew(self,e):
        print "choose a new file"
        
    def onOpen(self,e):
        self.dirname = ' '
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, " ", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), "r")
            RECTANGLES = f.read()
            print RECTANGLES
            f.close()  
            
        dlg.Destroy()
        
    def onSave(self,e):
        self.dirname = ' '
        dlg = wx.FileDialog(self, "Save your file", self.dirname, "", "*.txt", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:

            itcontains = str(RECTANGLES)
            
            self.filename = dlg.GetFilename()
            print self.filename
            self.dirname = dlg.GetDirectory()
            filehandle = open(os.path.join(self.dirname, self.filename), "w")
            print filehandle
            filehandle.write(itcontains)
            filehandle.close()
               
        dlg.Destroy()
        

    def onAbout(self,e):
        dlg = wx.MessageDialog(self, "A sequencer for GPIO", "About SeqGPIO", wx.OK)  
        dlg.ShowModal()
        dlg.Destroy()
        
