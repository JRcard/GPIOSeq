# encoding: utf-8
import wx
from constants import *
from variables import *
from widgets import *


class Grid(wx.Panel):
    def __init__(self, parent, pos, size, zoom=1):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        ### la scrollbar apparait mais ne fonctionne pas....
        self.scroll = wx.ScrollBar(self, -1, pos=(TRACKNAME_POS[0],TRACKNAME_POS[1]+(27*GRID_STEP)),
                                   size=(GRID_SIZE[0],15), style=wx.SB_HORIZONTAL)
        
        self.pos = None
        self.zoom = zoom
        
        self.Bind(wx.EVT_SCROLL, self.onScroll)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onMouseRightDown)
        self.Bind(wx.EVT_RIGHT_UP,self.onMouseRightUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)  
                                      
                                      
        for i in range(TRACK_TOTAL):
            self.track = Track(self,-1, 
                               "GPIO%02d" % (i+1), 
                               pos=(TRACKNAME_POS[0],TRACKNAME_POS[1]+(i*GRID_STEP)), 
                               size=(59,19))
                                                        
######### MOUSE METHODS #####
    def onMouseLeftDown(self,e):
        self.CaptureMouse()
        self.pos = self.clip(e.GetPositionTuple()) 
        
        self.rectangle = Rectangle(self.pos[0], self.pos[1])     ### Creation du rectangle
        RECTANGLES.append(self.rectangle)                       ### ajout a la liste des RECTANGLES 
        

    def onMotion(self,e):
        if self.HasCapture():
            self.pos = self.clip(e.GetPositionTuple())
            
            if self.pos[0] - RECTANGLES[-1].getX() > 0:
                RECTANGLES[-1].setWidth(self.pos[0])
            
                self.Refresh()


    def onMouseLeftUp(self,e):
        if self.HasCapture():
            self.ReleaseMouse()
            self.pos = self.clip(e.GetPositionTuple())
    
            if self.pos[0] - RECTANGLES[-1].getX() > 0:     ### si la souris bouge
                print "Append RECTANGLES:", RECTANGLES 
 
            else:     
                RECTANGLES.pop()       ### les coordonnées créer avec le onMouseLeftDown s'efface
                print 
                print "Remove RECTANGLES:", RECTANGLES 
                print
                               

    def onMouseRightDown(self,e):
        self.CaptureMouse()
        self.pos = self.clip(e.GetPositionTuple()) 
        
        for rec in RECTANGLES:
            if rec.isInside(self.pos):      ## determine si le curseur a cliqué dans un rectangle
                print "ATTRAPPE"
                break
                
    def onMouseRightUp(self,e):
        if self.HasCapture():
            self.ReleaseMouse()
            self.pos = self.clip(e.GetPositionTuple())
            
            for rec in RECTANGLES:
                if rec.isInside(self.pos):
                    print "ERASE", rec
                    RECTANGLES.remove(rec)
                    wx.CallAfter(self.Refresh)
                    break
                    
#                else:
#                    print "RELACHE"

                    
                    

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
                rec.draw(dc)
               
    def onScroll(self,e):
        thumbPos = self.scroll.GetThumbPosition()
        self.scroll.SetScrollbar(thumbPos,GRID_SIZE[0]/self.zoom,GRID_SIZE[0]*self.zoom,GRID_SIZE[0]/self.zoom)
            
            
            
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
            
        elif pos[1] > GRID_SIZE[1]:
            pos[1] = GRID_SIZE[1]
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
            dc.DrawLine(TRACKNAME_SIZE[0]+i,30, TRACKNAME_SIZE[0]+i,y)   ### VERTICAL LINES
            
        for i in range(0,x,(TIMELINE_MINUTE*self.zoom)):                 ### marqueur de minutes
            dc.SetPen(wx.Pen("#333333",3))
            dc.DrawLine(TRACKNAME_SIZE[0]+i,30, TRACKNAME_SIZE[0]+i,y)   ### VERTICAL LINES 
        
                