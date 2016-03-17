# encoding: utf-8

########################      GRID       #######
GRID_POS = (7,100)
GRID_SIZE = (1420,580)   
GRID_STEP = 20

#######################      TRACKNAME   #######
TRACK_TOTAL = 27
TRACKNAME_POS = (1,40)
TRACKNAME_SIZE = (60, GRID_SIZE[1])

#######################      TIMELINE    #######
TIMELINE_POS = (50,15)
TIMELINE_SIZE = (GRID_SIZE[0], 40)
TIME_TOTAL = 6  ### nombre total de minute de la grille ne peut dépasser.(Ce nombre comme tel est exclus. Lire comme un range de x valeur)
TIME_ABS = 13 ### facteur de multiplication de GRID_STEP pour un zoom de 1
TIMELINE_MINUTE = TIME_ABS*GRID_STEP
