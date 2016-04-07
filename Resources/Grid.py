# encoding: utf-8
import wx
from constants import *
from variables import *
from widgets import *
        
class Grid(wx.Panel):
    def __init__(self, parent, pos, size, zoom=1):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.regCursor = wx.StockCursor(wx.CURSOR_ARROW)
        self.sizeCursor = wx.StockCursor(wx.CURSOR_SIZEWE)
        self.moveCursor = wx.StockCursor(wx.CURSOR_SIZING)
        self.eraseCursor = wx.StockCursor(wx.CURSOR_NO_ENTRY)

        self.zoom = zoom
        self.pos = None
        self.create = False
        self.recMove = False
        self.recErase = False
        self.recSize = False
        self.newRec = None
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
        
#        self.SetSizer(self.sizer)


######### MOUSE METHODS #####
    def onMouseLeftDown(self,e):
        self.CaptureMouse()
        self.pos = self.clip(e.GetPositionTuple())
        posX = self.pos[0] / self.zoom
        posY = self.pos[1]

        self.onRec(posX,posY)

        if self.rec == None:
            self.rectangle = Rectangle(posX, posY) 
            self.newRec = self.rectangle
            self.create = True

        elif self.rec is not None and self.recSizeContains(posX):
            self.recSize = True
            self.SetCursor(self.sizeCursor)
            self.dragX = posX - self.rec.width
            print "catch to resize!", self.rec

        elif self.rec is not None and not self.recErase:
            self.recMove = True
            self.SetCursor(self.moveCursor)
            self.dragX = posX - self.rec.X
            self.dragY = posY - self.rec.Y
            print "catch to move!", self.rec


    def onMotion(self,e):
        self.pos = self.clip(e.GetPositionTuple())
        posX = self.pos[0] / self.zoom
        posY = self.pos[1]

        if not self.HasCapture():

            self.onRec(posX,posY)

            if self.rec is not None and self.recSizeContains(posX):
                self.SetCursor(self.sizeCursor)

            elif self.rec is not None:
                self.SetCursor(self.moveCursor)

            else:
                self.SetCursor(self.regCursor)

            
        elif self.HasCapture():

            if self.create: 
                if self.pos[0] - self.newRec.X <= 0:
                    self.create = False
                    self.newRec = None
                else:
                    self.newRec.width = max(0, posX - self.newRec.X)

            elif self.recSize:
                self.rec.width = max(1, posX - self.dragX)

            elif self.recMove and not self.recErase:
                self.rec.X = max(0, posX - self.dragX)
                self.rec.Y = min(posY - self.dragY, GRID_SIZE[1] - SCROLLBAR)

            elif self.recErase and not self.rec.ContainsXY(posX,posY):
                self.SetCursor(self.regCursor)

            elif self.recErase and self.rec.ContainsXY(posX,posY):
                self.SetCursor(self.eraseCursor)


            self.Refresh()


    def onMouseLeftUp(self,e):
        if self.HasCapture():
            self.ReleaseMouse()
            self.pos = self.clip(e.GetPositionTuple())
            if self.create:
                self.create = False
                if self.pos[0]/self.zoom - self.newRec.X > 0:
                    RECTANGLES.append(self.newRec)
                    self.newRec = None
                    print "Append RECTANGLES:", RECTANGLES 
                    print

                elif self.newRec in RECTANGLES:
                    RECTANGLES.remove(self.newRec)
                    print 
                    print "Remove RECTANGLES:", RECTANGLES 
                    print

            elif self.recSize:
                self.recSize = False
                self.SetCursor(self.regCursor)
                print "Resized RECTANGLES:", RECTANGLES

            elif self.recMove:
                self.recMove = False
                print "Moved RECTANGLES:", RECTANGLES

            self.Refresh()


    def onMouseRightDown(self,e):
        self.CaptureMouse()
        self.pos = self.clip(e.GetPositionTuple())
        posX = self.pos[0]/self.zoom
        posY = self.pos[1]

        self.onRec(posX,posY)
        print "ATTRAPPE", self.rec

        if self.rec is not None:
            self.recErase = True
            self.SetCursor(self.eraseCursor)

    def onMouseRightUp(self,e):
        if self.HasCapture():
            self.ReleaseMouse()
            self.pos = self.clip(e.GetPositionTuple())
            posX = self.pos[0]/self.zoom
            posY = self.pos[1]


            if self.recErase and self.rec.ContainsXY(posX,posY):
                self.recErase = False
                print "ERASE", self.rec
                RECTANGLES.remove(self.rec)
                print
                print "Erased RECTANGLES:", RECTANGLES
                self.rec = None
                self.SetCursor(self.regCursor)
                wx.CallAfter(self.Refresh)

            else:
                self.recErase = False
                print "ECHAPPE", self.rec


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
        if self.newRec is not None:
            self.newRec.draw(dc,self.zoom,"#aa0000", "#000000")
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

        elif pos[1] > GRID_SIZE[1] - (SCROLLBAR+GRID_STEP):
            pos[1] = GRID_SIZE[1] - (SCROLLBAR+GRID_STEP)
            pos[1] = pos[1] - (pos[1] % GRID_STEP)

        else:
            pos[1] = pos[1] - (pos[1] % GRID_STEP)

        return tuple(pos)
        
    def setZoom(self,z):
        self.zoom = z
        
    def recSizeContains(self,posX):
        if posX >= self.rec.X + (self.rec.width - 4) and posX <= self.rec.X + self.rec.width:
            return True

        else:
            return False

    def onRec(self,posX,posY):
        for rec in RECTANGLES:
            if rec.ContainsXY(posX, posY):
                self.rec = rec
                break
            else:
                self.rec = None


### comment je fais pour savoir que ma grille s'élargit vraiment 
### et que ce n'ai pas seulement mes lignes plus foncées 
### et les chiffres qui changent de place...????

    def backGround(self,dc):
        x, y = self.GetSize()
        dc.SetBrush(wx.Brush("#000000"))
        dc.DrawRectangle(0,0, x,y)

    def timeLine(self,dc):
        dc.SetBrush(wx.Brush("#CCCCCC"))
        dc.DrawRectangle(0,0, TIMELINE_SIZE[0],TIMELINE_SIZE[1])

        for i in range(TIME_TOTAL):
            dc.DrawText("%d:00" % (i), 
                        TIMELINE_POS[0]+((i*TIMELINE_MINUTE)*self.zoom),
                        TIMELINE_POS[1])

    def squares(self,dc):
        x, y = self.GetSize()
        for i in range(0,x*self.zoom,GRID_STEP):
            dc.SetPen(wx.Pen("#333333",1))
            dc.DrawLine(0,TIMELINE_SIZE[1]+i, x,TIMELINE_SIZE[1]+i)      ### HORIZONTAL LINES
            dc.DrawLine(i*self.zoom,30, i*self.zoom,y-SCROLLBAR)   ### VERTICAL LINES

        for i in range(0,x*self.zoom,TIMELINE_MINUTE):                 ### marqueur de minutes
            dc.SetPen(wx.Pen("#333333",3))
            dc.DrawLine(i*self.zoom,30, i*self.zoom,y-SCROLLBAR)   ### VERTICAL LINES 
            

class ScrollGrid(wx.ScrolledWindow):
    def __init__(self, parent, pos, size):
        wx.ScrolledWindow.__init__(self, parent, pos=pos, size=size)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.grid = Grid(self, pos=GRID_POS, size=GRID_SIZE)

        self.sizer.Add(self.grid)
        self.SetSizer(self.sizer)

        self.SetScrollRate(GRID_STEP,GRID_STEP)
        self.EnableScrolling(1,0)
        
    def setZoom(self,z):
        self.grid.zoom = z