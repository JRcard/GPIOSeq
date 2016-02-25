#!/usr/bin/env python
# encoding: utf-8

import os
import wx
from Template import *
from variables import *


class SeqMenu(wx.MenuBar):
    
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        
        self.parent = parent
        # create each menu itself who will go on the menu bar
        self.program = wx.Menu()
        self.file = wx.Menu()
        self.edit = wx.Menu()
        self.help = wx.Menu()
               
        # Put the "Program" menu on the menu bar and put action in this menu    
        self.Append(self.program, "&Program")
        self.menuExport = self.program.Append(100, "Export\tCtrl+E", "Export data")
        self.menuExit = self.program.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        # Put the "File" menu on the menu bar and put action in this menu           
        self.Append(self.file, "&File")
        self.menuNew = self.file.Append(wx.ID_NEW, "&New", "New file")
        self.menuOpen = self.file.Append(wx.ID_OPEN, "&Open...", "Open a file")
        self.menuSave = self.file.Append(wx.ID_SAVE, "&Save", "Save a File")
        
        # Put the "Edit" menu on the menu bar and put action in this menu           
        self.Append(self.edit, "&Edit")
        self.menuCopy = self.edit.Append(wx.ID_COPY, "&Copy", "Copy the selection")
        self.menuPaste = self.edit.Append(wx.ID_PASTE, "&Paste", "Paste the last copy")

        # Put the "Help" menu on the menu bar and put action in this menu   
        self.Append(self.help, "&Help")
        self.menuHelp = self.help.Append(wx.ID_ABOUT, "&About", "Information about this program")

###### Binding menu bar ###########

        # PROGRAM
        self.Bind(wx.EVT_MENU, self.onExit, self.menuExit)
        self.Bind(wx.EVT_MENU, self.onExport, self.menuExport, id=100)
        
        
        # FILE
        self.Bind(wx.EVT_MENU, self.onNew, self.menuNew)
        self.Bind(wx.EVT_MENU, self.onOpen, self.menuOpen)
        self.Bind(wx.EVT_MENU, self.onSave, self.menuSave)
        
        # EDIT 
        #self.Bind(wx.EVT_MENU, self.onCopy, self.menuCopy)
        #self.Bind(wx.EVT_MENU, self.onPaste, self.menuPaste)
        
        # HELP 
        self.Bind(wx.EVT_MENU, self.onAbout, self.menuHelp)
        
########   MENU  -------methods-------  ##########

    def onExit(self, e):
#        dlg = wx.MessageDialog(self, 
#            "Do you really want to close this application?",
#            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
#        result = dlg.ShowModal()
#        dlg.Destroy()
#        if result == wx.ID_OK:
        self.parent.Destroy()
        
    def onExport(self, e):
        # Generation du texte du Sequenceur
        text = SETUP % (str(dictGPIO))  
        text += SEQUENCE
        
        # Ecriture du fichier
        self.dirname = ' '
        dlg = wx.FileDialog(self, "Export your file", self.dirname, "", "*.py", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), "w")
            f.write(text)
            f.close()
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
            f.close()  
        dlg.Destroy()
        
    def onSave(self,e):
        self.dirname = ' '
        dlg = wx.FileDialog(self, "Save your file", self.dirname, "", "*.txt", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            itcontains = "HORS FONCTION POUR L'INSTANT"
            
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            filehandle = open(os.path.join(self.dirname, self.filename), "w")
            filehandle.write(itcontains)
            filehandle.close()
            
        dlg.Destroy()
        
    def onAbout(self,e):
        dlg = wx.MessageDialog(self, "A sequencer for GPIO", "About SeqGPIO", wx.OK)  
        dlg.ShowModal()
        dlg.Destroy()
        
