# encoding: utf-8


RECTANGLES = []  ## Instance des rectangles
RECTS = []       ## Rectangle sans l'instance

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
    
# place en ordre les valeurs des listes
#def sort(lst):
#    return sorted(lst)
    
# Enleve les redonances dans les listes
#def order(lst):
#    return list(sorted(set(lst)))
    

def prepareDictGPIO():
    RECTANGLES.sort(key=lambda x: x[0])
    print RECTANGLES
#    for rec in RECTANGLES:
#        RECTS.append(rec.getAll())
#    print "RECTS", RECTS        
    for rec in RECTANGLES:
        track_num = rec.getTrackNum()   ### valeur numerique représentant le numero de piste et la pin GPIO en même temps.
        rect_start = rec.getStart()     ### coordonné du X apres le clip onMouseLeftUp
        rect_stop = rec.getStop()       ### coordonné en X de la fin du rectangle (Valeur global dans la grid)
        rect_width = rec.getWidth()     ### coordonné du X apres onMouseLeftUp (Longueur du rectangle)            
    
        setGPIO(track_num)
        dictGPIO[track_num]["RECT_START"].append(rect_start)   ### création du dictionnaire pour les récupérations de données pour le script RASPI
        dictGPIO[track_num]["RECT_WIDTH"].append(rect_width)
        dictGPIO[track_num]["RECT_STOP"].append(rect_stop)

        
def clearDictGPIO():                  #### dictionnaire ne reset pas!!!!!
    global dictGPIO
    if dictGPIO != None:
        dictGPIO.clear()  