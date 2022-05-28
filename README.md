# Test IMKI labyrinthe par Yoann ZAMORA


Pour résoudre ce problème, j'ai adopté ici une architecture très simple: une seule classe est crée, la classe Environnement.

1 - Les objets de cette classe sont d'abord définis par une grille (en fait le labyrinthe) possédant 16 pièces (0 ou 1 (si sortie ou trésor)) 
    et des séparations entre ces pièces représentées par des murs "passant" ou non (-1 ou 0).
    Ainsi la grille ou matrice possède 16 pièces (avec l'entrée et la sortie qui sont fixes) et 33 murs (laissant ou ne laissant pas passer) pour 
    un total de 49 cases. Conservant cette structure, ces labyrinthes sont générés aléatoirement:
    
  ![Labyrinthe_soluble](https://user-images.githubusercontent.com/98098119/170832952-5b116cc6-7150-4131-9aa9-498025a96186.png)
    
Des coordonnées (x,y) sont également associés à chaque environnement instancié. Les pièces avec l'entrée, la sortie
et le trésor sont grisées, les murs sont en noirs et les pièces et les murs "passant" (laissant passer) sont blancs.

Les actions pour se déplacer dans l'environnement (haut, bas, gauche, droite) font également parties des environnements instanciés.


2 - La démarche est de même, tout sauf ardue à bien comprendre.

Pour générer une infinité de labyrinthes solubles selon les besoins du problèmes posés : un chemin du starting point à l'end point ET un chemin du starting point au trésor, j'ai décidé de vérifier séparément que le premier existe (effaçant le trésor) puis que le second existe également (effaçant la sortie).
Ainsi je conclue simplement, si les deux pseudos-labyrinthes sont solubles alors le labyrinthe complet l'est aussi (puisque le starting point doit être liés à la fois au trésor et à la sortie selon l'énoncé).
Pour vérifier qu'un chemin existe, je fais en sorte que la recherche de la pièce (trésor ou sortie) continue jusqu'à ce que celle-ci soit trouvée OU que le nombre de boucle effectuée par l'algorithme dépasse un nombre arbitrairement grand d'itération. Ainsi, si le nombre de boucle atteint ce nombre maximal, c'est que le chemin (pour ce labyrinthe de taille relativement réduite) est inatteignable. À noter qu'une méthode de la classe Environnement pour qu'un mur ne soit pas franchissable.

La recherche de la pièce s'effectue en utilisant une méthode de renforcement (Q-learning) avec "beaucoup" d'exploration pour trouver la pièce recherchée. L'objectif ici n'est pas d'optimiser la Q-table mais simplement de savoir si un chemin "valide" existe. On ne cherche donc pas à relancer l'algorithme jusqu'à ce que la Q-table soit bien complétée mais l'on met tout de même en place la méthode pour le faire le cas échéant. C'est pourquoi, à chaque itération, je mets à jour la Q-table  à l'aide de l'équation de Bellman mise à jour:

![image](https://user-images.githubusercontent.com/98098119/170833991-d6f57136-f195-4cad-bf40-7e1d2d940c55.png)


Je lance ainsi tout ce programme jusqu'à obtenir un labyrinthe soluble entièrement, puis j'affiche et je sauvegarde son image autant de fois que l'on veut (à l'infini):


![image](https://user-images.githubusercontent.com/98098119/170834296-988c9d59-8408-4da3-ae6d-462b91a7cb22.png)
