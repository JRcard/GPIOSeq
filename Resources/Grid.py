# encoding: utf-8
import wx
from constants import *
from variables import *
from widgets import *


class Grid(wx.ScrolledWindow):
    def __init__(self, parent, pos, size, zoom=1):
        wx.ScrolledWindow.__init__(self, parent, pos=pos, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        self.zoom = zoom
        self.pos = None
        self.create = False
        self.catch = False
        self.recSize = False
        self.rec = None
        self.dragX = 0
        self.dragY = 0
        
#        self.Bind(wx.EVT_SCROLL, self.onScroll)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onMouseRightDown)
        self.Bind(wx.EVT_RIGHT_UP,self.onMouseRightUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)  
                                      
                                                                                              
######### MOUSE METHODS #####
    def onMouseLeftDown(self,e):
        self.CaptureMouse()
        self.pos = self.clip(e.GetPositionTuple())
        posX = self.pos[0]/self.zoom
        posY = self.pos[1]
                
        for rec in RECTANGLES:
            if rec.isInside((posX,posY)):
                self.rec = rec
                self.create = False
                self.catch = True
                self.dragX = posX - self.rec.X
                self.dragY = posY - self.rec.Y
                print "catch to move!"
                break
                
        if self.catch:
            if self.pos[0] >= self.rec.width - 4:
                self.catch = False
                self.recSize = True   ##### concept a revoir!!!!!!!!
     
        if not self.catch and not self.recSize:
            self.rectangle = Rectangle(posX, posY)
            RECTANGLES.append(self.rectangle) 
            self.create = True
            
        
    def onMotion(self,e):
        if self.HasCapture():
            self.pos = self.clip(e.GetPositionTuple())
            posX = self.pos[0]/self.zoom
            posY = self.pos[1]
            
            if self.recSize:
                self.rec.width = posX - self.dragX
                self.recSize = False
            
            if self.catch:
                self.rec.X = max(0,posX - self.dragX)
                self.rec.Y = min(posY - self.dragY, GRID_SIZE[1] - SCROLLBAR) 
                
            if self.create: 
                if self.pos[0] - RECTANGLES[-1].X > 0:
                    RECTANGLES[-1].width = max(0,posX-RECTANGLES[-1].X)
                    
            self.Refresh()


    def onMouseLeftUp(self,e):
        if self.HasCapture():
            self.ReleaseMouse()
            self.pos = self.clip(e.GetPositionTuple())
            if self.create:
                self.create = False
                if self.pos[0] - RECTANGLES[-1].X > 0:
                    print "Append RECTANGLES:", RECTANGLES 
     
                else:     
                    RECTANGLES.pop()
                    print 
                    print "Remove RECTANGLES:", RECTANGLES 
                    print
                
            if self.catch:
                self.catch = False
                if self.rec.width <= 0:
                    RECTANGLES.remove(rec)
                    

    def onMouseRightDown(self,e):
        self.CaptureMouse()
        self.pos = self.clip(e.GetPositionTuple()) 
        posX = self.pos[0]/self.zoom
        posY = self.pos[1]        
        
        for rec in RECTANGLES:
            if rec.isInside((posX,posY)):
                print "ATTRAPPE"
                break
                
    def onMouseRightUp(self,e):
        if self.HasCapture():
            self.ReleaseMouse()
            self.pos = self.clip(e.GetPositionTuple())
            posX = self.pos[0]/self.zoom
            posY = self.pos[1]  
                      
            for rec in RECTANGLES:
                if rec.isInside((posX,posY)):
                    print "ERASE", rec
                    RECTANGLES.remove(rec)
                    wx.CallAfter(self.Refresh)
                    break


######## PAINT METHOD #######

    def onPaint(self,e):
        dc = wx.AutoBufferedPaintDC(self)
        
        # PANEL IN BACKGROUND #######      
        self.backGround(dc)
        
        # TIMELINE #####        
        self.timeLine(dc)
        
        # GRID #######   
        self.squares(dc)      

        # RECTANGLE #######  
        if RECTANGLES is not []:          
            for rec in RECTANGLES:
                rec.draw(dc,self.zoom,"#000099", "#0000ff")

            
######### GENERALS METHODS #######
    def clip(self,pos):

        pos = list(pos)
        if pos[0] < 0:
            pos[0] = 0
            
        elif pos[0] > GRID_SIZE[0]:
            pos[0] = GRID_SIZE[0]
            
            
        if pos[1] < TIMELINE_SIZE[1]:
            pos[1] = TIMELINE_SIZE[1]
            pos[1] = pos[1] - (pos[1] % GRID_STEP)
            
        elif pos[1] > GRID_SIZE[1] - SCROLLBAR:
            pos[1] = GRID_SIZE[1] - SCROLLBAR
            pos[1] = pos[1] - (pos[1] % GRID_STEP)
            
        else:
            pos[1] = pos[1] - (pos[1] % GRID_STEP)
            
        return tuple(pos)
            
    def setZoom(self,x):
        self.zoom = x
        


### comment je fais pour savoir que ma grille s'élargit vraiment 
### et que ce n'ai pas seulement mes lignes plus foncées 
### et les chiffres qui changent de place...????

    def backGround(self,dc):
        x, y = self.GetSize()        
        dc.SetBrush(wx.Brush("#000000"))
        dc.DrawRectangle(0,0, x,y)
        
    def timeLine(self,dc):
        dc.SetBrush(wx.Brush("#CCCCCC"))
        dc.DrawRectangle(0,0, TIMELINE_SIZE[0]*self.zoom,TIMELINE_SIZE[1])

        for i in range(TIME_TOTAL):
            dc.DrawText("%d:00" % (i), 
                        TIMELINE_POS[0]+((i*TIMELINE_MINUTE)*self.zoom),
                        TIMELINE_POS[1])

            
    def squares(self,dc):
        x, y = self.GetSize()         
        for i in range(0,x*self.zoom,GRID_STEP):
            dc.SetPen(wx.Pen("#333333",1))
            dc.DrawLine(0,TIMELINE_SIZE[1]+i, x,TIMELINE_SIZE[1]+i)      ### HORIZONTAL LINES
            dc.DrawLine(i*self.zoom,30, i*self.zoom,y)   ### VERTICAL LINES
            
        for i in range(0,x*self.zoom,TIMELINE_MINUTE):                 ### marqueur de minutes
            dc.SetPen(wx.Pen("#333333",3))
            dc.DrawLine(i*self.zoom,30, i*self.zoom,y)   ### VERTICAL LINES 
        
                