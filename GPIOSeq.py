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

# Une grid correcte qui aura besoin de remaniment... Les pistes devraient etre dynamique pour pouvoir leur donner un nom par exemple. (DONE)
# Sinon la grid remplis bien son rôle, c'est à dire qu'elle accepte bien les dessins de rectangle et chaque rectangle créé remplis des listes de valeur. 
# Des types de valeur, j'en ai plus que moins pour l'instant car je ne sais pas encore quel type de donnée sera le plus simple à utiliser. (TYPE DICT.)

# La gestion des rectangles est encore à travailler.... je ne réussit pas à en effacer....
# je souhaite pouvoir effacer le rectangle d'un clic droite. Cependant il se passe quelque chose seulement si je clic sur le dernier rectangle créé.
# Quand je lache la souris dans le rectangle, une instance remplace celle qui aurais du être effacé...

# Ensuite sur le plan des rectangles lorsque je réussirai à les effacers j'essairai des déplacer...

# Pour la génération d'un fichier python par un "Export" ça fonctionne bien. Il me reste a élaborer le script pour qu'il marche sur le RASPI. 
# Pour ça j'aurai besoin de comprendre comment il peut y avoir plusieurs évènements qui roulent en même temps. Car jusqu'à maintenant mon expérience
# avec la programmation des GPIO etait plutôt linéaire

