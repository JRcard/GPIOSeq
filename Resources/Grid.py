# encoding: utf-8
import wx
from constants import *
from variables import *
from widgets import *


class Grid(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size)#, style=wx.VSCROLL | wx.HSCROLL)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.pos = None

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onMouseRightDown)
        self.Bind(wx.EVT_RIGHT_UP,self.onMouseRightUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)  


######### EVENTUELLEMENT UNE CLASSE: TIMELINE
        for i in range(TIME_TOTAL):
            self.time = wx.StaticText(self, id=-1, 
                                      label="%d:00" % (i+1),
                                      pos=(TIMELINE_POS[0]+(i*TIMELINE_STEP),
                                      TIMELINE_POS[1]))
                                       
######### MOUSE METHODS #####
    def onMouseLeftDown(self,e):
        self.CaptureMouse()
        self.pos = self.clip(e.GetPositionTuple())        
     
        self.rectangle = Rectangle(self.pos[0],self.pos[1])     ### Creation du rectangle
        RECTANGLES.append(self.rectangle)                       ## ajout a la liste des RECTANGLES


    def onMotion(self,e):
        if self.HasCapture():
            self.pos = self.clip(e.GetPositionTuple())
            
            if self.pos[0] - RECTANGLES[-1].getStart() > 0:
                RECTANGLES[-1].setWidth(self.pos[0])
            
                self.Refresh()


    def onMouseLeftUp(self,e):
        if self.HasCapture():
            self.ReleaseMouse()
            self.pos = self.clip(e.GetPositionTuple())
    

            if self.pos[0] - RECTANGLES[-1].getStart() > 0:     ### si la souris bouge
            
### for rec in RECTANGLES: rec.getPatente..... puis ajout au dictionnaire.
### Cette section devrait etre dans export ou play..... 
### le dictionnaire devrait se remplir à la fin de la chaine. cela aidera à gerer les données des instances effacées.....

                self.track_num = RECTANGLES[-1].getTrackNum()   ### valeur numerique représentant le numero de piste et la pin GPIO en même temps.
                self.rect_start = RECTANGLES[-1].getStart()     ### coordonné du X apres le clip onMouseLeftUp
                self.rect_stop = RECTANGLES[-1].getStop()       ### coordonné en X de la fin du rectangle (Valeur global dans la grid)
                self.rect_width = RECTANGLES[-1].getWidth()     ### coordonné du X apres onMouseLeftUp (Longueur du rectangle)            
                

                setGPIO(self.track_num)
                dictGPIO[self.track_num]["RECT_START"].append(self.rect_start)   ### création du dictionnaire pour les récupérations de données pour le script RASPI
                dictGPIO[self.track_num]["RECT_WIDTH"].append(self.rect_width)
                dictGPIO[self.track_num]["RECT_STOP"].append(self.rect_stop)
                print "DICTIONNAIRE!!!!", dictGPIO
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

    def onMouseRightUp(self,e):
        if self.HasCapture():
            self.ReleaseMouse()
            self.pos = self.clip(e.GetPositionTuple())
            
            for rec in RECTANGLES:

                if rec.isInside(self.pos):     ### Volonté d'effacer l'instance et tous les données qui viennent avec........
                    #for rec in RECTANGLES:
                    print "ERASE", self.rectangle
                    RECTANGLES.remove(rec)
                       
                    self.Refresh()
                    
                else:
                    print "RELACHE"


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
            

                                    ############   Fonction qui devrait devenir des class..... ##########
    def backGround(self,dc):
        x, y = self.GetSize()        
        dc.SetBrush(wx.Brush("#000000"))
        dc.DrawRectangle(0,0, x,y)
        
    def timeLine(self,dc):
        dc.SetBrush(wx.Brush("#CCCCCC"))
        dc.DrawRectangle(0,0, TIMELINE_SIZE[0],TIMELINE_SIZE[1])
        
    def squares(self,dc):
        x, y = self.GetSize()         
        dc.SetPen(wx.Pen("#333333",1))
        for i in range(0,x,GRID_STEP):
            a = dc.DrawLine(0,40+i, x,40+i)   ### HORIZONTAL LINES
            b = dc.DrawLine(i,30, i,y)        ### VERTICAL LINES    