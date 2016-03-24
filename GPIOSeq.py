#!/usr/bin/env python
# encoding: utf-8

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
    
# Un frame, un panel avec des bouton et un menu semi fonctionelle. Les fonctions sont créées pour tout
# mais ils n'ont pas tous des actions concrètes.

# Une grid correcte sur lequel je suis en train de travailler un zoom. Voir Scene, Grid et widgets

# La gestion des rectangles est encore à travailler... j'aimerais les déplacer... ils devraient etre plus autonome....

# Mon fichier export fonctionne bien. Je voudrais maintenant le pousser automatiquement en appuyant sur "PLAY".
# Lorsque j'appui sur "play" un fichier se créer et se met dans mon dossier document. (Voir Constants.py pour les valeurs de préferences)
# je n'ai pas réussit a faire fonctionner correctment les commandes a envoyé au Raspi par ssh. (voir Scene: methode onConnect et onPlay
