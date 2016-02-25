# encoding: utf-8


RECTANGLES = []  ## Instance des rectangles

##########  DICTIONMARE ########

dictGPIO = {}

######## FONCTIONS ###########
    
# Enregistre une reference dans le dictionnaire.
def setGPIO(key):
    if key not in dictGPIO:
        dictGPIO[key] = {"RECT_START":[], "RECT_WIDTH":[], "RECT_STOP":[]}
        
# Recupere une reference dans le dictionnaire.
def getGPIO(key):
    return dictGPIO.get(key, None)
    
# Enleve les redonances dans les listes
def sort(lst):
    return sorted(lst)
    
# place en ordre les valeurs des listes
def order(lst):
    return list(sorted(set(lst)))