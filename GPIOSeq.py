#!/usr/bin/env python
# encoding: utf-8

##################################### PEXPECT DOIT ÊTRE INSTALLÉ POUR EXECUTER LE CODE SOURCE. 

import wx, os
from Resources.TOP_FRAME import *


class MyApp(wx.App):
    
    def OnInit(self):
        frame = SeqFrame(None, "GPIOSeq")
        self.SetTopWindow(frame)
        return True
        

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()


###### OU J'EN SUIS:
# grid de 3 miniutes, avec zoom fonctionel;
# Prochaine étape: scrollbar!!!!!..... voir Scene.py et Grid.py 
# Et une barre de temps déffilante au moment où la sequence est enclanché.
# Les rectangles sont autonomes. Ils peuvent être effacés, agrandis et déplacés. 
# Petit extra: le curseur de la souris change de forme selon la fonction qu'il effectura. 
# Prochaine étape: pouvoir agir sur un groupe de rectangle.

# La gestion des préférences de connection est fonctionnel.
# La connection au raspi est fonctionelle. PEXPECT DOIT ÊTRE INSTALLÉ POUR EXECUTER LE CODE SOURCE. 
# Une gestion minimal pour guider l'utilisateur dans l'ordre des procedures pour la connection a été mise en place. 
# Ex. S'il appuie sur "play" avant d'être connecté un message apparaît. S'il veut se connecter et qu'il n'a pas entrer ces préférences, le panneau apparaît, etc...
# Il en reste beaucoup à faire au niveau de tous les messages possibles d'erreur de connection qui devront être rendu visible à l'utilisateur.
# À ce sujet, voir: Pref.py
# Une fois connecté, le bouton "play" fonctionne. Le raspberry agit rapidement. 
# Prochaine étape: réussir à arrêter le processus en cours...
# Il y a une création de fichiers temporaires pour l'envoi vers le raspi, mais il ne se crée pas au bon endroit. Facile à résoudre.

# Voilà pour le moment ce que j'ai pu faire en un peu plus de 3 mois.

