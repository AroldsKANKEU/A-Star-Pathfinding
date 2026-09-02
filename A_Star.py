# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 05:36:32 2026

@authors: AROLD'S KANKEU 
"""



##############################################################################
#############################IMPORTANT########################################
##############################################################################
'''
#Note pour le lecteur: Nous ne savons pas quel IDE vous utiliser
# mais le travail a été fait avec Spyder, alors si vous voulez exécuter ou
# évaluer le code en effectuant plusieurs tests, si vous faites la simulation 
#sur run, vous aurez un message d’erreur car le noyau vous indiquera que vous
# ne l’avez pas fournie les villes de départ et d’arrivée, il va falloir que 
#vous allez dans command line option dans l’onglet run qui se trouve la barre
# de menu et insérer les deux villes . Alors, pour faire facile, il vous suffit
# d’aller dans le terminal et saisir %run tp1.py Arad Bucharest pour la trace 1
# et %run tp1.py Timisoara Neamt pour la trace 2 et puis vous les exécuter 
#chacun à son tour pour avoir l’historique affiché dans le terminal.
'''




# Nous commençons par importer la bibliothèque 'math'. 
# Elle est fournie avec Python et ne nécessite aucune installation supplémentaire.
# Nous l'utilisons principalement pour accéder à la fonction hypot().
# Cette fonction nous permet de calculer la distance à vol d'oiseau (distance euclidienne)
# entre deux points géographiques, en utilisant le théorème de Pythagore.
# Ce calcul est essentiel pour notre heuristique h(n)
import math 

# Nous importons également le module 'sys', qui est un autre module standard de Python.
# Celui-ci nous permet d'interagir avec l'interpréteur et le système d'exploitation.
# Nous l'utilisons principalement à deux fins dans notre programme :
# 1. Récupérer les arguments que l'on passe  dans la ligne de commande
#    (par exemple, "Arad" et "Bucharest") via la liste sys.argv.
# 2. Forcer l'arrêt du programme avec un message d'erreur (sys.exit(1))
#    si nous oublions de fournir les deux villes nécessaires.

import sys ##utilisé pour récupérer les arguments de la ligne de commande (sys.argv) afin de lancer le programme avec les villes de départ et d'arrivée.

# ------------------------------------------------------------
# 1. DÉFINITION DU GRAPHE (Distances routières en km)
# ------------------------------------------------------------
# Nous définissons ici la structure de données représentant notre réseau routier.
# Il s'agit d'un dictionnaire Python imbriqué (un dictionnaire de dictionnaires).
# 
# - La clé principale est le nom d'une ville.
# - La valeur associée est un autre dictionnaire qui contient les villes voisines
#   accessibles directement depuis cette ville, ainsi que la distance réelle en kilomètres
#   pour parcourir cette route.
# 
## Cette structure est idéale pour notre algorithme car elle nous permet d'accéder
## aux voisins d'une ville en O(1), c'est-à-dire en un temps constant, ce qui est très efficace.
graph = {
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Zerind': {'Oradea': 71, 'Arad': 75},
    'Arad': {'Zerind': 75, 'Timisoara': 118, 'Sibiu': 140},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilela': 146, 'Pitesti': 138},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilela': 80},
    'Rimnicu Vilela': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilela': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
}

# ------------------------------------------------------------
# 2. COORDONNÉES pour l'heuristique (Distance à vol d'oiseau)
#    (Les valeurs sont approximatives et mises à l'échelle pour 
#     garantir que l'heuristique reste ADMISSIBLE)
# ------------------------------------------------------------

# Nous définissons ici les coordonnées approximatives de chaque ville
# sur un plan cartésien (x, y). Ces coordonnées nous permettent
# de calculer la distance à vol d'oiseau (distance euclidienne)
# entre deux villes quelconques.
#
# Pourquoi ces valeurs ?
# - L'échelle utilisée ici n'a pas besoin d'être parfaitement réaliste
#   (ce ne sont pas des coordonnées GPS exactes).
# - Nous avons simplement veillé à ce que la distance calculée soit
#   toujours inférieure ou égale à la distance routière réelle.
#   Cette condition, appelée "admissibilité", est essentielle pour
#   garantir que notre algorithme A* trouve bien le chemin optimal.
# - Les valeurs ont été choisies en respectant les positions relatives
#   des villes sur la carte (ex: Oradea est à l'ouest, Bucharest à l'est).
#
coords = {
    'Oradea': (100, 300),
    'Zerind': (170, 310),
    'Arad': (200, 270),
    'Timisoara': (150, 200),
    'Lugoj': (190, 210),
    'Mehadia': (210, 180),
    'Drobeta': (230, 190),
    'Craiova': (280, 200),
    'Sibiu': (300, 300),
    'Rimnicu Vilela': (350, 270),
    'Fagaras': (380, 310),
    'Pitesti': (390, 230),
    'Bucharest': (450, 200),
    'Giurgiu': (430, 130),
    'Urziceni': (490, 210),
    'Vaslui': (580, 280),
    'Iasi': (620, 330),
    'Neamt': (590, 380),
    'Hirsova': (550, 230),
    'Eforie': (560, 180),
   # 'Tulcea': (600, 220)
}

# ------------------------------------------------------------
# 3. FONCTIONS UTILITAIRES
# ------------------------------------------------------------

# Fonction heuristique : calcule la distance à vol d'oiseau (Euclidienne)
# entre un nœud (ville courante) et le but (ville destination).
# Cette distance est utilisée comme estimation h(n) dans notre algorithme A*.
# Nous utilisons la fonction hypot() du module math, qui applique le théorème
# de Pythagore : sqrt((x1-x2)² + (y1-y2)²).
#
# - Elle nous fournit une estimation du coût restant pour atteindre le but.
# - En étant toujours inférieure ou égale au coût réel (admissibilité),
#   elle garantit que l'algorithme A* trouvera bien le chemin optimal.
# - Elle respecte également l'inégalité triangulaire, ce qui la rend cohérente
#   et améliore les performances de la recherche


def heuristic(node, goal):
    """Calcule la distance Euclidienne (vol d'oiseau) entre node et goal."""
    x1, y1 = coords[node] # Nous récupérons les coordonnées (x, y) du nœud courant.
    x2, y2 = coords[goal] # Nous récupérons les coordonnées (x, y) de la destination.
    return math.hypot(x1 - x2, y1 - y2)  # Calcul direct de l'hypoténuse (distance à vol d'oiseau).


# Fonction de transformation d'un nom de ville en index (première lettre).
#Il nous a été demandé dans l'énoncé d'afficher la premiere lettre de chaque ville 
#comme identififant. Cela garantit que la trace de l'algo reste lisible et sans 
#confusion
def get_index(city_name):
    """
    Retourne l'index à afficher.
    Pour lever l'ambiguïté Timisoara/Tulcea (les deux commencent par T),
    j'utilise 'Ti' et 'Tu' dans l'affichage.
    """
    if city_name == 'Timisoara':
        return 'Ti'
   # elif city_name == 'Tulcea':
   #    return 'Tu'
    else:
      return city_name[0]  # Pour toutes les autres villes, nous retournons la première lettre (ex: 'A' pour Arad).

# Fonction de formatage d'un nœud pour l'affichage de la trace.
# Cette fonction est essentielle pour produire une sortie conforme aux
# spécifications de l'énoncé. Elle construit une chaîne de caractères
# au format : "Index : f = g+h, parent = ParentIndex".
# 
# Par ex: pour la ville d'Arad (départ), avec g=0, h=260, parent=None,
# elle produit : "A : f = 0+260=260, parent = None".

# Nous utilisons l'option de formatage :.0f pour arrondir les nombres flottants
# à des entiers dans l'affichage, ce qui rend la trace plus propre et plus
# facile à lire

def format_node(node, g_score, parent, goal):
    """Formate un nœud comme demandé : 'index : f = g+h, parent'"""
    h_val = heuristic(node, goal)               # Calcul de l'heuristique h(n).
    f_val = g_score + h_val                     # Calcul de f(n) = g(n) + h(n).
    parent_display = get_index(parent) if parent else "None"   # Affichage du parent (ou "None" pour le départ).
    return f"{get_index(node)} : f = {g_score:.0f}+{h_val:.0f}={f_val:.0f}, parent = {parent_display}"


# ------------------------------------------------------------
# 4. ALGORITHME A* AVEC TRACE DÉTAILLÉE
# ------------------------------------------------------------

# Nous définissons ici la fonction principale de notre résolveur.
# Elle prend en entrée la ville de départ (start) et la ville de destination (goal),
# et retourne le chemin optimal trouvé par l'algorithme A*.

# ------------------------------------------------------------
#  4. ALGORITHME A* AVEC TRACE DÉTAILLÉE ET STOCKAGE DES PARENTS
# ------------------------------------------------------------

# Cette fonction est le cœur de notre programme. Elle implémente l'algorithme A*
# pour trouver le chemin le plus court entre une ville de départ (start) et une
# ville de destination (goal). Nous avons choisi de stocker les parents de chaque
# nœud dans un dictionnaire dédié afin de pouvoir reconstruire facilement et
# proprement le chemin final, une fois le but atteint.


def a_star_final(start, goal):
    
    # ------------------------------------------------------------------
    # 4.1 STRUCTURES DE DONNÉES (Les "ingrédients" de l'algorithme)
    # ------------------------------------------------------------------

    # Structure "Open" (la frontière de recherche) :
    # Nous utilisons un dictionnaire pour sa rapidité d'accès (O(1)).
    # - Clé : le nom de la ville
    # - Valeur : une liste contenant [g_score, parent]
    #   * g_score : le coût réel du chemin parcouru depuis le départ jusqu'à cette ville.
    #   * parent : la ville précédente sur le chemin (None pour la ville de départ).
    # 
   
    # Que de choisir une liste, nous avons choisit un dictionnaire parce qu'il 
    # nous permet de retrouver ou de mettre à jour un nœud
    # instantanément, sans avoir à parcourir toute la liste. Cela rend
    # notre programme plus efficace, même si le graphe est petit.
    # 
    # Au lancement de l'algorithme, la seule ville que nous connaissons
    # est la ville de départ. Son coût g est de 0 (nous n'avons encore rien
    # parcouru) et elle n'a pas de parent, d'où la valeur None.
    
    open_dict = {start: [0, None]}
    
    # Structure "Closed" (les nœuds déjà explorés) :
    # Nous utilisons un ensemble (set) plutôt qu'une liste. Cette structure
    # de données est particulièrement efficace pour les tests d'appartenance
    # (vérifier rapidement si un nœud a déjà été traité). Elle nous permet
    # d'éviter de tourner en rond en revenant sur nos pas.
    # 
    # Note technique : Un ensemble en Python est une collection non ordonnée
    # d'éléments uniques. La recherche d'un élément s'y fait en temps constant,
    # ce qui est idéal pour notre algorithme qui doit vérifier à chaque étape
    # si un voisin a déjà été exploré.
    
    closed_set = set()
    
    # Structure "Parents" (l'arbre généalogique de nos découvertes) :
    # Ce dictionnaire  enregistre, pour chaque ville découverte, la ville
    # qui l'a précédée sur le chemin (son "parent").
    # 
    # Nous avons besoin d'un dictionnaire en plus de open_dict parce que open_dict
    # ne stocke le parent que tant que le nœud est dans la
    # frontière. Une fois qu'un nœud est retiré de open pour être développé,
    # nous perdons cette information. Le dictionnaire 'parents' conserve
    # cette information de manière permanente, ce qui nous permettra,
    # à la fin de la recherche, de remonter de la destination jusqu'au départ
    # pour reconstituer l'itinéraire complet.
    # 
    # Nous l'initialisons avec la ville de départ, qui n'a évidemment pas de parent.
    
    parents = {start: None}  # Dictionnaire pour retracer le chemin
    
    # Nous initialisons le compteur d'itérations à 0.
    # Ce compteur est simplement un outil visuel pour suivre l'évolution
    # de la recherche dans la trace que nous allons afficher.
    
    iteration = 0

# Nous commençons par afficher un en-tête clair et bien délimité.
# La première partie du message indique les villes que l'on cherche à relier.
# La ligne de 60 signes '=' permet de séparer visuellement l'en-tête
# du reste de la trace, ce qui rend la lecture plus agréable.

    print(f"Recherche du chemin de {start} à {goal}\n" + "="*60)

 # ------------------------------------------------------------------
 # 4.3 BOUCLE PRINCIPALE DE L'ALGORITHME A*
 # ------------------------------------------------------------------

    # Tant qu'il reste des nœuds à explorer dans la frontière (Open),
    # nous poursuivons la recherche. Si Open devient vide, cela signifie
    # qu'aucun chemin n'existe entre le départ et la destination.

    while open_dict:
        
 # ------------------------------------------------------------------
        # 4.3.1 COMPTAGE ET SÉLECTION DU MEILLEUR NŒUD
 # ------------------------------------------------------------------

 # Nous incrémentons le compteur d'itérations pour numéroter
 # chaque étape de la recherche dans la trace finale.       
        
        iteration += 1
        
 # Sélection du nœud le plus prometteur dans Open :
 # Nous utilisons la fonction min() pour trouver la ville qui possède
 # la plus petite valeur de f(n) = g(n) + h(n).
 # 
 # Explication détaillée du paramètre 'key' :
 # La fonction lambda (fonction anonyme) que nous passons à min() prend
 # chaque ville x (clé du dictionnaire) et retourne un tuple de deux nombres :
 #   - Le premier nombre est f(n) = g + h (le coût total estimé).
 #   - Le deuxième nombre est g(n) (le coût réel parcouru).
        
#On utilise ce tuple car:
# En cas d'égalité de f entre deux villes, Python utilise le deuxième
# élément du tuple comme critère de départage (tie-break). Il choisira
# alors la ville ayant le plus petit g, ce qui est une bonne pratique
# pour l'efficacité de A* (cela permet de privilégier les chemins
# déjà les plus courts en cas d'égalité de promesse).    
        
        current = min(open_dict.keys(), key=lambda x: (open_dict[x][0] + heuristic(x, goal), open_dict[x][0]))
        
# Une fois le meilleur nœud identifié, nous le retirons définitivement
# de la liste Open pour le traiter dans cette itération.
# La méthode pop() supprime la clé du dictionnaire et retourne la
# valeur associée. Nous décompressons immédiatement cette valeur
# (qui est une liste [g_score, parent]) dans les variables
# current_g et current_parent.        

        current_g, current_parent = open_dict.pop(current)
        
        # Mise à jour du parent dans le dictionnaire de traces

# ------------------------------------------------------------------
        # 4.3.2 STOCKAGE DURABLE DU PARENT (CORRECTION MAJEURE)
# ------------------------------------------------------------------

# Nous mettons à jour notre dictionnaire "parents" qui enregistre
# l'historique complet des relations parent-enfant.
# 
# Pourquoi avons-nous besoin de cette étape alors que le parent
# était déjà stocké dans open_dict ?
# Parce que nous venons de retirer ce nœud de open_dict. Si nous ne
# le sauvegardions pas ailleurs, nous perdrions cette information
# de parenté, ce qui nous empêcherait de reconstruire le chemin
# final. Ce dictionnaire "parents" sert donc de mémoire permanente.
# 
# Nous vérifions d'abord si le parent n'est pas None.
# Si current_parent est None, cela signifie que nous traitons la
# ville de départ (qui n'a pas de parent). Dans ce cas, nous ne
# faisons rien pour éviter d'écraser l'entrée existante.
        if current_parent is not None:
           parents[current] = current_parent

# ------------------------------------------------------------------
        # 4.3.3 AFFICHAGE DU NŒUD COURANT (TRACE DE RÉSOLUTION)
# ------------------------------------------------------------------
 # Nous calculons la valeur f(n) pour le nœud courant.
 
        current_f = current_g + heuristic(current, goal)
# Nous affichons le numéro de l'itération pour structurer la trace
        print(f"\n--- Itération {iteration} ---")
        
# Nous préparons l'affichage du parent.
# Si le parent existe, nous utilisons get_index() pour obtenir sa
# première lettre. Sinon, nous affichons "None" pour indiquer
# qu'il s'agit du point de départ.        
        
        parent_display = get_index(current_parent) if current_parent else "None"

# Nous affichons la ligne dédiée au nœud courant en respectant le format demandé par l'énoncé :
# "Index : g=..., h=..., f=..., parent=..."

        print(f"Traitement de : {get_index(current)} (g={current_g:.0f}, h={heuristic(current, goal):.0f}, f={current_f:.0f}, parent={parent_display})")
        
       
# ------------------------------------------------------------------
        # 4.3.4 AFFICHAGE DE LA LISTE Open (LA FRONTIÈRE DE RECHERCHE)
# ------------------------------------------------------------------

# Nous affichons maintenant l'état de la liste Open, qui contient
# toutes les villes découvertes mais pas encore explorées.
#

# Nous affichons Open a chaque itération parce que c'est une exigence de l'énoncé. 
#Cela permet de voir comment la frontière de recherche évolue au fur et à 
#mesure que l'algorithme explore de nouveaux chemins.

        if open_dict:
            
# Nous créons une liste temporaire qui contiendra les chaînes
# de caractères formatées pour chaque ville dans Open.
            open_items = []
# Nous parcourons chaque entrée du dictionnaire open_dict.
# La syntaxe 'for node, (g, p) in open_dict.items()' permet de
# décompresser directement les valeurs (g et p) sans avoir à
# utiliser d'index.
            for node, (g, p) in open_dict.items():
                
# Calcul de l'heuristique h(n) pour ce nœud.
                h = heuristic(node, goal)
# Calcul de f(n) = g(n) + h(n), qui est l'estimation du coût total du chemin passant par ce nœud.

                f = g + h

 # Nous préparons l'affichage du parent en utilisant la fonction get_index() 
 #pour obtenir sa première lettre. Si le parent n'existe pas (None), nous affichons "None"                

                p_display = get_index(p) if p else "None"
                
# Nous construisons la chaîne de caractères en respectant rigoureusement le format 
# demandé par l'énoncé : "Index : f = g+h, parent = ParentIndex"
# On utilise :.0f pour arrondir les nombres  à des entiers, car les décimales 
# ne sont pas utiles dans la trace (elles alourdiraient inutilement l'affichage).
            open_items.append(f"{get_index(node)} : f = {g:.0f}+{h:.0f}={f:.0f}, parent = {p_display}")
          
# Nous trions la liste open_items par ordre alphabétique.

# - L'énoncé  nous demande une trace complète, mais ne précise pas l'ordre d'affichage de Open.
# - Le tri par f est déjà fait dans la sélection du meilleur
#   nœud (étape 4.3.1). Ici, pour l'affichage, un tri alphabétique rend 
# la trace plus lisible et prévisible sans impacter la logique.
            
            open_items.sort()
# Nous affichons la liste Open sous forme de chaîne de caractères.
            print("Open : " + str(open_items))
# Si Open est vide, cela signifie qu'il ne reste plus de nœud à explorer.
# L'algorithme est donc sur le point de se terminer (soit parce qu'il a trouvé la solution, soit parce qu'il a échoué).

        else:
            print("Open : []")
        
# ------------------------------------------------------------------
# 4.3.5 AFFICHAGE DE LA LISTE Closed (NŒUDS DÉJÀ EXPLORÉS)
# ------------------------------------------------------------------

# Nous affichons ensuite la liste Closed, qui contient toutes les
# villes que nous avons déjà développées (c'est-à-dire dont les
# voisins ont été générés).
#
# Nous utilisons une compréhension de liste (list comprehension)
# pour construire une liste des indices (premières lettres) des
# villes dans Closed. La fonction sorted() garantit un affichage
# trié par ordre alphabétique.
# 
# Pourquoi n'affichons-nous que les indices et pas les valeurs
# de g, h et f comme pour Open ?
# Parce que l'énoncé demande que chaque nœud traité soit affiché
# au moment où il est retiré de Open (étape 4.3.3). À ce moment-là,
# nous avons déjà affiché toutes ses informations (g, h, f, parent).
# Les afficher à nouveau ici serait redondant et alourdirait
# inutilement la trace. L'affichage des seuls indices permet de
# voir rapidement quelles villes ont été "fermées" sans surcharger
# la sortie.
        
        print("Closed : " + str([get_index(node) for node in sorted(closed_set)]))
       
#------------------------------------------------------------------
# 4.3.6 VÉRIFICATION DE L'ARRÊT (BUT ATTEINT)
# ------------------------------------------------------------------

# Nous vérifions si le nœud que nous venons de traiter est la ville de destination (goal).

# Pourquoi cette vérification est-elle placée ici, après
# avoir retiré le nœud de Open ?
# Parce que dans l'algorithme A*, la première fois que nous
# retirons un nœud de Open et que ce nœud correspond au but,
# nous avons la certitude mathématique que c'est le chemin optimal
# (à condition que notre heuristique soit admissible, ce qui est
# le cas ici avec la distance à vol d'oiseau).
# 
# Si nous avions vérifié avant de le retirer de Open, nous aurions
# risqué de sélectionner un chemin qui n'est pas encore optimal.
        
        if current == goal:
# Nous affichons un message de succès bien visible.
            print("\n" + "="*60)
            print(">>> SOLUTION TROUVÉE !")

# ------------------------------------------------------------------
# 4.3.7 RECONSTRUCTION DU CHEMIN FINAL
# ------------------------------------------------------------------

# Nous allons maintenant reconstruire l'itinéraire complet.
# Pour cela, nous utilisons le dictionnaire 'parents' que nous avons
# soigneusement alimenté à chaque étape de la recherche.
# 
# Ce dictionnaire fonctionne comme une chaîne de liens :
# parents['Bucharest'] = 'Pitesti'
# parents['Pitesti'] = 'Rimnicu Vilela'
# parents['Rimnicu Vilela'] = 'Sibiu'
# parents['Sibiu'] = 'Arad'
# parents['Arad'] = None
#
# Notre stratégie consiste à :
# 1. Partir de la ville destination (current).
# 2. Remonter de parent en parent jusqu'à atteindre None.
# 3. Inverser la liste obtenue pour avoir l'ordre chronologique
# (de la ville de départ à la ville d'arrivée).

# Nous initialisons une liste vide qui contiendra le chemin.

            path = []
# Nous commençons par le nœud courant (la destination).
            node = current

# Nous remontons la chaîne des parents.
# Tant que le nœud n'est pas None, nous l'ajoutons à la liste
# et nous passons à son parent.
# 
# Exemple visuel du parcours :
# node = 'Bucharest' → on ajoute 'Bucharest'
# node = parents['Bucharest'] = 'Pitesti' → on ajoute 'Pitesti'
# ... etc.

            while node is not None:
                path.append(node)
                node = parents.get(node)

# À ce stade, path contient le chemin dans l'ordre inverse
# (de la destination vers le départ).
# Par exemple : ['Bucharest', 'Pitesti', 'Rimnicu Vilela', 'Sibiu', 'Arad']
# 
# Nous utilisons la méthode reverse() pour inverser la liste
# et obtenir l'ordre correct :
# ['Arad', 'Sibiu', 'Rimnicu Vilela', 'Pitesti', 'Bucharest']

            path.reverse()
            
# ------------------------------------------------------------------
# 4.3.8 AFFICHAGE DÉTAILLÉ DE LA SOLUTION TROUVÉE
# ------------------------------------------------------------------

# Nous affichons maintenant l'itinéraire complet, avec les coûts
# réels (kilométrages) entre chaque ville et la distance totale.

            print("\n--- Solution Finale ---")

# Nous initialisons une variable qui accumulera la distance totale
# du parcours, exprimée en kilomètres.
            total_cost = 0

# Nous parcourons la liste 'path' qui contient les villes dans
# l'ordre chronologique (du départ à l'arrivée).
# La boucle s'arrête à l'avant-dernier élément (len(path) - 1)
# car nous avons besoin de la ville suivante pour calculer le coût.
            
            for i in range(len(path) - 1):
 # Nous récupérons la ville actuelle (src) et la ville suivante (dst).
                
                src = path[i]
                dst = path[i+1]
# Nous lisons la distance entre ces deux villes directement
# dans notre dictionnaire 'graph'.                
                cost = graph[src][dst]
                
# Nous ajoutons ce coût à notre accumulateur.
                total_cost += cost

# Nous affichons la transition avec son coût en kilomètres.
# Exemple : "Arad -> Sibiu : 140 km"

                print(f"{src} -> {dst} : {cost} km")
# Une fois la boucle terminée, nous affichons la distance totale
# du trajet, ainsi que le chemin complet sous une forme lisible.            

            print(f"\nDistance totale : {total_cost} km")
            print(f"Chemin complet : {' -> '.join(path)}")
# Nous retournons la liste 'path' au programme appelant.
# Cette liste contient l'intégralité de la solution trouvée.

            return path
        
# ------------------------------------------------------------------
# 4.3.9 MISE À JOUR DE Closed (LE NŒUD EST MAINTENANT EXPLORÉ)
# ------------------------------------------------------------------

# Nous ajoutons le nœud courant à l'ensemble closed_set.
# Pourquoi le faisons-nous ici, après avoir vérifié que ce n'est pas le but ?
# Parce que nous savons maintenant que ce nœud a été complètement
# développé (nous avons examiné tous ses voisins plus bas).
# 
# Nous utilisons la méthode add() d'un ensemble. Cela ajoute l'élément
# s'il n'est pas déjà présent. S'il est déjà présent, l'opération
# ne fait rien (c'est une propriété des ensembles : ils n'acceptent
# pas les doublons).
        
        closed_set.add(current)
       
# ------------------------------------------------------------------
# 4.3.10 EXPANSION DES VOISINS (DÉCOUVERTE DE NOUVEAUX CHEMINS)
# ------------------------------------------------------------------

# Pour chaque voisin de la ville courante, nous allons évaluer
# si le chemin passant par la ville courante est meilleur que
# le chemin déjà connu pour atteindre ce voisin.
# 
# La méthode graph.get(current, {}) est une façon sécurisée
# d'accéder aux voisins. Si 'current' n'est pas dans le graphe
# (ce qui est impossible dans notre cas), elle retourne un
# dictionnaire vide pour éviter une erreur.
        
        for neighbor, cost in graph.get(current, {}).items():
         
# Nous vérifions d'abord si ce voisin fait déjà partie de
# l'ensemble closed_set. Si c'est le cas, cela signifie que
# nous l'avons déjà développé. Nous ne le re-développons pas
# car un chemin qui passe par un nœud déjà exploré ne peut pas
# être meilleur que le chemin déjà trouvé (propriété de A*
# avec une heuristique admissible).
            
            if neighbor in closed_set:
                continue
# Nous calculons le coût 'g' pour arriver à ce voisin en passant
# par le nœud courant.
            
            tentative_g = current_g + cost
# Nous vérifions si le voisin n'a jamais été découvert
# (c'est-à-dire qu'il n'est pas dans open_dict).           
            
            if neighbor not in open_dict:

# C'est la première fois que nous voyons ce voisin.
# Nous l'ajoutons donc à open_dict avec son coût g calculé
# et la ville courante comme parent.
                
                open_dict[neighbor] = [tentative_g, current]
                
# Nous enregistrons également cette relation parent-enfant
# dans notre dictionnaire permanent 'parents'

                parents[neighbor] = current  # On stocke le parent ici
            else:

# Le voisin est déjà dans open_dict. Nous devons vérifier si le chemin que nous
# venons de trouver est meilleur que celui qui est déjà enregistré.
                
                if tentative_g < open_dict[neighbor][0]:
                    
# Le nouveau chemin est meilleur ! Nous mettons à jour open_dict avec le nouveau
# coût g et le nouveau parent.

                    open_dict[neighbor] = [tentative_g, current]
# Nous mettons également à jour le dictionnaire 'parents'pour refléter cette amélioration.

                    parents[neighbor] = current  # Mise à jour du parent si meilleur chemin
 # ------------------------------------------------------------------
 # 4.3.11 FIN DE LA BOUCLE : RETOUR À L'ÉTAPE 4.3
 # ------------------------------------------------------------------

 # La boucle while se poursuit. Si elle se termine sans avoir trouvé de solution (c'est-à-dire si open_dict devient vide), cela signifie
 # que le graphe ne permet pas de relier la ville de départ à la ville de destination.
    
 # ------------------------------------------------------------------
# 4.3.12 CAS D'ÉCHEC (AUCUN CHEMIN TROUVÉ)
# ------------------------------------------------------------------

# Si nous sortons de la boucle while sans avoir rencontré le 'return path',
# cela signifie que nous avons exploré tous les nœuds possibles sans
# trouver la destination.   
    
# ------------------------------------------------------------------
# 4.3.12 CAS D'ÉCHEC (AUCUN CHEMIN TROUVÉ)
# ------------------------------------------------------------------

# Si nous sortons de la boucle while sans avoir rencontré le 'return path',
# cela signifie que nous avons exploré tous les nœuds possibles sans
# trouver la destination.
    
    print("Échec : Aucun chemin trouvé.")

# Nous retournons None pour indiquer l'absence de solution.
    return None


# ------------------------------------------------------------
# 6. LANCEMENT DU PROGRAMME (POINT D'ENTRÉE)
# ------------------------------------------------------------

# Cette condition est un standard en Python. Elle permet de distinguer
# deux cas d'utilisation de notre fichier :
# 1. Si le fichier est exécuté directement (par exemple, en cliquant sur
#    "Run" dans Spyder, ou en tapant 'python tp1.py' dans le terminal),
#    le bloc de code en dessous de cette condition sera exécuté.
# 2. Si le fichier est importé comme un module dans un autre programme
#    (ex: 'import tp1'), ce bloc ne sera pas exécuté.
# 
# Cela nous permet à la fois d'utiliser notre programme en ligne de commande
# et de le réutiliser comme une bibliothèque si besoin.

if __name__ == "__main__":
    
# ------------------------------------------------------------------
# 6.1 RÉCUPÉRATION DES ARGUMENTS DE LA LIGNE DE COMMANDE
# ------------------------------------------------------------------

# Nous utilisons le module 'sys' (importé en début de fichier) pour
# accéder à la liste des arguments passés lors de l'exécution du script.
# sys.argv est une liste qui contient :
# - sys.argv[0] : le nom du script lui-même (ex: 'tp1.py')
# - sys.argv[1] : le premier argument (la ville de départ)
# - sys.argv[2] : le deuxième argument (la ville de destination)
# - etc.
# 
# Nous ou autre utilisateur devons lancer le programme avec la commande: ex python tp1.py <VilleDepart> <VilleDestination>
    
    if len(sys.argv) < 3:
        
# Si une autre personne manipule notre code et ne fourni pas les deux arguments nécessaires,
# nous affichons un message d'usage pour lui indiquer comment utiliser correctement le programme.
        
        print("Usage: python tp1.py <VilleDepart> <VilleDestination>")
        print("Exemple: python tp1.py Arad Bucharest")
        
# Nous quittons alors le programme avec un code d'erreur (1).
# Le code 1 est une convention qui indique au système d'exploitation
# que le programme s'est terminé à cause d'une erreur (par opposition
# à un code 0 qui signifierait "succès").
        sys.exit(1)
# Nous récupérons maintenant les deux arguments passés par l'utilisateur.
# L'utilisateur doit saisir les noms complets des villes (ex: 'Arad', 'Bucharest'), car notre dictionnaire 'graph'
# utilise ces noms complets comme clés.
    
    start_city = sys.argv[1]
    goal_city = sys.argv[2]

# ------------------------------------------------------------------
# 6.2 VALIDATION DES VILLES SAISIES
# ------------------------------------------------------------------

# Avant de lancer l'algorithme, nous vérifions que les villes fournies
# par l'utilisateur existent bien dans notre graphe.
# 
# Pourquoi cette vérification est-elle importante ?
# - Si l'utilisateur fait une faute de frappe (ex: 'Aradd' au lieu de 'Arad'),
#   l'algorithme planterait avec une erreur KeyError.
# - Cette validation permet d'afficher un message d'erreur clair et
#   compréhensible, plutôt qu'une trace d'exception technique.
# 
# Nous utilisons l'opérateur 'not in' pour vérifier si la ville n'est
# pas une clé du dictionnaire 'graph'
    
    if start_city not in graph or goal_city not in graph:
 # Si l'une des deux villes est introuvable, nous affichons un message d'erreur explicite.        
 
        print("Erreur : Ville non trouvée dans le graphe.")
        
# Nous quittons le programme avec un code d'erreur (1) pour signaler que l'exécution n'a pas abouti.
        sys.exit(1)

#------------------------------------------------------------------
# 6.3 LANCEMENT EFFECTIF DE L'ALGORITHME A*
# ------------------------------------------------------------------

# Toutes les vérifications sont passées avec succès !
# Nous pouvons maintenant appeler notre fonction principale
# a_star_final() en lui passant la ville de départ et la ville
# de destination.
# 
# Cette fonction se charge de :
# - Exécuter l'algorithme A*.
# - Afficher la trace complète de la recherche (Open et Closed
#   à chaque itération).
# - Afficher le chemin final avec les coûts détaillés.
# 
# Le résultat retourné par la fonction est un chemin (une liste de villes)
# ou None si aucun chemin n'existe. Dans notre cas, nous n'avons pas
# besoin de stocker ce résultat dans une variable, car l'affichage
# est déjà géré à l'intérieur de la fonction.

    a_star_final(start_city, goal_city)
    
    
    
##Nous remercions toute autre suggestion ou toute critique apportée a ce code afin de
## faire de lui une réference pour l'implementation d'un algorithme A* dans un graphe