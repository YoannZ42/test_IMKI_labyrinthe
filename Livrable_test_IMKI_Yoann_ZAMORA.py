# -*- coding: utf-8 -*-
"""
Created on Tue May 24 19:45:40 2022

@author: zamor
"""


# Librairies utiles

import numpy as np
from random import randint, uniform
import matplotlib.pyplot as plt
from PIL import Image


# Définition de la classe Environnement

class Environnement(object):
            
    
    def __init__(self):
        super(Environnement, self).__init__()
               
        # On détermine un labyrinthe aléatoire en décidant (aléatoirement) si les murs laissent passer (0) ou non (-1)
        murs = [randint(-1,0) for k in range(33)]     
        
        self.grille = [
            [0, murs[0], 0, murs[1], 0, murs[2], 0],
            [murs[3], murs[4], murs[5], murs[6], murs[7], murs[8], murs[9]],
            [0, murs[10], 0, murs[11], 0, murs[12], 0],
            [murs[13], murs[14], murs[15], murs[16], murs[17], murs[18], murs[19]],
            [0, murs[20], 0, murs[21], 0, murs[22], 0],
            [murs[23], murs[24], murs[25], murs[26], murs[27], murs[28], murs[29]],
            [0, murs[30], 0, murs[31], 0, murs[32], 1]
        ]
        
        
        # Position de départ
        self.y = 0
        self.x = 0
        
        # Les différentes actions possibles
        self.actions = [
            [-1, 0], # haut
            [1, 0], # bas
            [0, -1], # gauche
            [0, 1] # droite
        ]

        
    # réinitialisation de l'environnement et on renvoie l'état initial
    def reinit(self):
        self.y = 0
        self.x = 0
        return (self.y*7+self.x+1)
    
    
    # On avance d'un pas en fonction de la position dans la grille et de l'action prise (haut, bas, gauche, droite ) 
    # et on renvoie l'état nouveau et la récompense de la nouvelle position
    def avance(self, action):
        self.y = max(0, min(self.y + self.actions[action][0],6))
        self.x = max(0, min(self.x + self.actions[action][1],6))
        return (self.y*7+self.x+1) , self.grille[self.y][self.x]


    
    # Est-ce que l'on a touché au but ? On vérifie la position dans l'environnement
    def termine(self):
        return self.grille[self.y][self.x] == 1
    
    
    
    # Est-on dans un mur dans le prochain état ? On vérifie la position dans l'environnement
    def est_mur(self, action):        
        position_y = max(0, min(self.y + self.actions[action][0],6))
        position_x = max(0, min(self.x + self.actions[action][1],6))        
        return self.grille[position_y][position_x] == -1
    
    
    
    # On affiche l'environnement avec les "box" en blanc, les murs en blanc ou noir (laissent ou pas passer) et le 
    # point de départ, la sortie et le trésor en gris
    def affiche(self):
        
        plt.figure()
        plt.grid('on')
        nb_lignes, nb_colonnes = np.array(self.grille).shape
        ax = plt.gca()
        ax.set_xticks(np.arange(0.5, nb_lignes, 1))
        ax.set_yticks(np.arange(0.5, nb_colonnes, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        affichage = np.copy(np.array(self.grille))
        
        # On modifie une copie du labyrinthe (affichage) simplement pour des besoins d'affichage
        for ligne in range(affichage.shape[0]):
            for col in range(affichage.shape[0]):
                if affichage[ligne,col] == 0:
                    affichage[ligne,col] = 3
                else:
                    affichage[ligne,col] = 1
                    
        # Affichage en gris du point de départ, de la sortie et du trésor
        affichage[6, 6] = 2
        affichage[4, 2] = 2
        affichage[0, 0] = 2

        # Affichage
        img = plt.imshow(affichage, interpolation='none', cmap='gray')
        
        # Sauvegarde de l'image du labyrinthe
        plt.savefig('Labyrinthe_soluble.png')
        
        return img
    
    
    
# On prend l'action en fonction du fait que l'on fasse de l'exploration ou de l'exploitation
def prise_d_action(etat, Q, exploration):
    if uniform(0, 1) < exploration: # Doit-on faire de l'exploration ou de l'exploitation ?
        action = randint(0, 3)  # On prend une action aléatoire dans le cas de l'exploration
    else: # dans le cas de l'exploitation
        action = np.argmax(Q[etat]) # ici je sélectionne l'action qui maximise la Q-fonction
    return action  # elle retourne l'action 







if __name__ == '__main__':
    
    message = "Le labyrinthe est insoluble !"
    
    while message == "Le labyrinthe est insoluble !":
    
        env = Environnement() # On instancie l'environnement
        etat = env.reinit()  # On initialise l'environnement et on prend l'état initial
        nb_boucle_max = 400000   # Nombre max de boucle pour arrêter la recherche en cas de labyrinthe insoluble

        # On initialise la Q-table avec tous les états à 0 pour toutes les actions
        Q = [[0,0,0,0] for i in range(50)]
        # Dans le cas de notre exercice, on choisit 90% d'exploration pour trouver le plus rapidement possible la sortie
        exploration = 0.9


        # Pour optimiser la Q-table, il faudrait chercher en boucle la sortie (et trésor). Or il nous intéresse simplement ici
        # de savoir qu'une sortie existe, donc nous ne lançons qu'une seule boucle tout en nous laissant la possiblité
        # de changer cela en modifiant le "1" à l'intérieur de la paranthèse


        ################ Nous prenons ici simplement en compte l'entrée et la sortie (pas le trésor)

        for _ in range(1):
            etat = env.reinit() # On réinitialise l'environnement
            nb_boucle_sortie = 0

            # Tant que la sortie n'est pas trouvée ou que le nombre de boucles n'atteint pas un nombre max, la recherche continue
            while (not env.termine() and nb_boucle_sortie < nb_boucle_max):

                action = prise_d_action(etat, Q, exploration)

                if not env.est_mur(action):
                    # On réalise l'action dans l'environnement et on retourne l'état suivant et la récompense 
                    etat_1, recompense = env.avance(action)  
                    # ici on sélectionne bien l'exploitation à 100% pour ne pas faire de l'exploration et calculer l'action suivante
                    action_1 = prise_d_action(etat_1, Q, 0.0)  
                    # On met à jour la Q-table
                    Q[etat][action] = Q[etat][action] + 0.1*(recompense + 0.9*Q[etat_1][action_1] - Q[etat][action])
                    etat = etat_1
                nb_boucle_sortie += 1



        ################ Nous prenons ici simplement en compte l'entrée et le trésor (pas la sortie)

        # On initialise une autre Q-table avec tous les états à 0 pour toutes les actions, 
        # pour la recherche du trésor et non de la sortie
        Q1 = [[0,0,0,0] for i in range(50)]

        for _ in range(1):
            etat = env.reinit() # On réinitialise l'environnement
            env.grille[4][2] = 1 # On met en place le trésor 
            env.grille[6][6] = 0 # On enlève la sortie pour que la recherche se concentre uniquement sur le trésor
            nb_boucle_tresor = 0
            while (not env.termine() and nb_boucle_tresor < nb_boucle_max):

                action = prise_d_action(etat, Q1, exploration)

                if not env.est_mur(action):
                    etat_1, recompense = env.avance(action)  
                    action_1 = prise_d_action(etat_1, Q1, 0.0)  
                    Q1[etat][action] = Q1[etat][action] + 0.1*(recompense + 0.9*Q1[etat_1][action_1] - Q1[etat][action])
                    etat = etat_1
                nb_boucle_tresor += 1



        # Si le nombre de boucle maximal a été atteint soit pour la recherche du trésor soit pour la recherche de la sortie
        # soit pour les deux, alors le labyrinthe est insoluble

        if (nb_boucle_sortie == nb_boucle_max) or (nb_boucle_tresor == nb_boucle_max):
            message = "Le labyrinthe est insoluble !"

        else:
            message = "Le labyrinthe est soluble !"

        
        
    # On affiche et sauvegarde le labyrinthe complet
    print(message)
    env.affiche()
    Image.open('Labyrinthe_soluble.png').show()
   