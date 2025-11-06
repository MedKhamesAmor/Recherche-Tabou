import random
from collections import deque

def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisins(solution):
    voisins = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution.copy()
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins

def tabu_search(matrice_distances, nombre_iterations, taille_tabu):
    nombre_villes = len(matrice_distances)
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)

    meilleure_solution = solution_actuelle.copy()
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)

    tabu_list = deque(maxlen=taille_tabu)

    for _ in range(nombre_iterations):
        voisins = generer_voisins(solution_actuelle)
        voisins = [voisin for voisin in voisins if voisin not in tabu_list]

        if not voisins:
            break

        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

        tabu_list.append(solution_actuelle.copy())

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle.copy()
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance

# Matrice des distances
matrice_distances = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]

# Paramètres de la recherche Tabu
nombre_iterations = 1000
taille_tabu = 50

# Exécution de l'algorithme
meilleure_solution, meilleure_distance = tabu_search(matrice_distances, nombre_iterations, taille_tabu)

# Affichage des résultats
print("Meilleure solution trouvée (Tabu Search):", meilleure_solution)
print("Distance minimale:", meilleure_distance)