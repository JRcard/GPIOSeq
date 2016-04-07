# encoding: utf-8
import os

REMOTE_HOST = "thebat.local"
REMOTE_USER = "pi"
REMOTE_PASS = "protools"
REMOTE_DIR = "/home/pi"
LOCAL_HOST = "Jrcard@MacPro.local"
LOCAL_PASS = "protools10.30"
TEMPFILE = "tempGPIOSeq.py"
TEMPDIR = os.getcwd()
########################      GRID       #######
GRID_POS = (67,100)
GRID_SIZE = (1360,595)   
GRID_STEP = 20
SCROLLBAR = 15
#######################       TRACKNAME   #######
TRACK_TOTAL = 27
TRACKNAME_POS = (1,40)
TRACKNAME_SIZE = (60, GRID_SIZE[1])

#######################      TIMELINE    #######
TIMELINE_POS = (0,15)
TIMELINE_SIZE = (GRID_SIZE[0], 40)

TIME_TOTAL = 6  ### nombre total de minute de la grille ne peut dépasser.(Ce nombre comme tel est exclus. Lire comme un range de x valeur)
TIME_ABS = 20 ### facteur de multiplication de GRID_STEP pour un zoom de 1
TIMELINE_MINUTE = TIME_ABS * GRID_STEP       ### nbrs de pixel dans 1 minutes.
TIMELINE_UNIT = 60. / TIMELINE_MINUTE     ## valeur en sec de 1 pixel