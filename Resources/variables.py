# encoding: utf-8

RECTANGLES = []  ## Instance des rectangles

##########  DICTIONMARE ########

dictGPIO = {}

####### FONCTIONS ###########
   
# Enregistre une reference dans le dictionnaire.
def setGPIO(key):
    global dictGPIO
    if key not in dictGPIO:
        dictGPIO[key] = {"RECT_START":[], "RECT_WIDTH":[], "RECT_STOP":[]}
        
# Recupere une reference dans le dictionnaire.
def getGPIO(key):
    return dictGPIO.get(key, None)

# Met les instances Rect en ordre chronologique. De cette liste en ordre, le dictionnaire se rempli.    
def prepareDictGPIO():
    RECTANGLES.sort(key=lambda x: x[0])
    print RECTANGLES
      
    for rec in RECTANGLES:
        track_num = rec.getTrackNum()   ### valeur numerique représentant le numero de piste et la pin GPIO en même temps.
        rect_start = rec.getAbsStart()     ### coordonné du X apres le clip onMouseLeftUp
        rect_stop = rec.getAbsStop()       ### coordonné en X de la fin du rectangle (Valeur global dans la grid)
        rect_width = rec.getAbsWidth()     ### coordonné du X apres onMouseLeftUp (Longueur du rectangle)            
    
        setGPIO(track_num)
        dictGPIO[track_num]["RECT_START"].append(rect_start)   ### création du dictionnaire pour les récupérations de données pour le script RASPI
        dictGPIO[track_num]["RECT_WIDTH"].append(rect_width)
        dictGPIO[track_num]["RECT_STOP"].append(rect_stop)

# Reset le dictionnaire         
def clearDictGPIO():
    global dictGPIO
    if dictGPIO is not None:
        dictGPIO.clear()  