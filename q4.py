import subprocess
import matplotlib

# Utiliser un backend non interactif (sans interface graphique)
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Tailles de cache L1 d'instructions et de données à tester (en KB)
'''
Explication à quoi correspond nb_elem_L1 par rapport à la taille des caches L1 :

    Pour chaque taille de cache donnée {1KB,2KB,4KB,8KB,16KB}, correspond un 'nb_elem_L1' qui dépend de l'associativité 
    et du nb de bloc, et qui correspond au premier argument à dans les config du cache le cache calculé (voir overleaf)

PAR EXEMPLE : pour 4KB, associativité de 1 et bloc size de 32, on a 128 nb d'elements et ils faut comme config :
il1:128:32:1:l 
'''

# Nom de base du fichier pour enregistrer les résultats : à modifier à chaque fois
output_file_base = "essai3_"

utile = ["sim_inst_rate", "sim_IPC", "bpred_bimod.bpred_addr_rate", "bpred_bimod.bpred_dir_rate","sim_elapsed_time", "il1.accesses","il1.misses","il1.replacements","dl1.accesses","dl1.misses","dl1.replacements","ul2.accesses","ul2.misses","ul2.replacements"]
sim_inst_rate_values =[]
sim_IPC_values = []
bpred_addr_rate_values = []
bpred_dir_rate_values = []
sim_elapsed_time_values = []
il1_accesses_values = []
il1_misses_values = []
il1_replacement_values = []
dl1_accesses_values = []
dl1_misses_values = []
dl1_replacement_values = []
ul2_accesses_values = []
ul2_misses_values = []
ul2_replacement_values = []

res = [0 for j in range(4)]

def trouve_entier(liste_caracteres, mot):
    i = len(mot)
    while i < len(liste_caracteres) and liste_caracteres[i] == " ":
        i += 1
    deb = i 
    while i < len(liste_caracteres) and liste_caracteres[i] != " ":
        i += 1
    fin = i
    try:
        return float(''.join(liste_caracteres[deb:fin])) if deb < fin else None
    except ValueError:
        print(f"Erreur de conversion en nombre pour le mot '{mot}'")
        return None

def chercher_mot_dans_fichier(nom_fichier, mot_recherche):
    try:
        # Ouvrir le fichier en mode lecture
        with open(nom_fichier, 'r') as fichier:
            # Lire toutes les lignes du fichier
            lignes = fichier.read().splitlines()

            # Chercher le mot dans chaque ligne
            for numero_ligne, ligne in enumerate(lignes, 1):  # On commence la numérotation des lignes à partir de 1
                if mot_recherche in ligne:
                    print(f"Le mot '{mot_recherche}' a été trouvé dans le fichier à la ligne {numero_ligne}.")
                    return numero_ligne  # Ajout de la ligne pour retourner le numéro de la ligne

            # Si le mot n'est pas trouvé dans aucune ligne
            print(f"Le mot '{mot_recherche}' n'a pas été trouvé dans le fichier.")
            return None
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
        return None

tableaux_associés = {
    'sim_inst_rate': sim_inst_rate_values,
    'sim_IPC': sim_IPC_values,
    'bpred_bimod.bpred_addr_rate': bpred_addr_rate_values,
    'bpred_bimod.bpred_dir_rate': bpred_dir_rate_values,
    'sim_elapsed_time': sim_elapsed_time_values,
    'il1.accesses': il1_accesses_values,
    'il1.misses': il1_misses_values,
    'il1.replacements': il1_replacement_values,
    'dl1.accesses': dl1_accesses_values,
    'dl1.misses': dl1_misses_values,
    'dl1.replacements': dl1_replacement_values,
    'ul2.accesses': ul2_accesses_values,
    'ul2.misses': ul2_misses_values,
    'ul2.replacements': ul2_replacement_values
}

# Créer un dictionnaire associant des références de tableaux à leurs noms
tableaux_vers_noms = {id(tableau): nom for nom, tableau in tableaux_associés.items()}

# Fonction pour obtenir le nom d'un tableau à partir de sa référence
def obtenir_nom_tableau(ref_tableau):
    return tableaux_vers_noms.get(id(ref_tableau), None)

# Fonction pour obtenir un tableau à partir de son nom
def obtenir_tableau_par_nom(nom_tableau):
    return tableaux_associés.get(nom_tableau, None)

def obtenir_tableau_caracteres_par_ligne(nom_fichier, numero_ligne):
    try:
        # Ouvrir le fichier en mode lecture
        with open(nom_fichier, 'r') as fichier:
            # Lire toutes les lignes du fichier
            lignes = fichier.read().splitlines()

            # Vérifier si le numéro de ligne est valide et si des lignes existent
            if lignes and 0 < numero_ligne <= len(lignes):
                # Récupérer la ligne correspondante
                ligne = lignes[numero_ligne - 1]

                # Créer un tableau avec chaque caractère de la ligne
                tableau_caracteres = list(ligne)
                return tableau_caracteres
            else:
                print(f"Numéro de ligne {numero_ligne} invalide ou fichier vide.")
                return []  # Retourner une liste vide dans ce cas
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
        return []  # Retourner une liste vide en cas d'erreur de fichier non trouvé

def generate_result(simulator_path, test_program, cortex, nsets_L1):
    
    # Affichage du test et du Cortex choisi
    print(f"Test benchmark : {test_program}, pour cortex : {cortex}")
    
    if cortex=="A7":
        # Spécifications du cache L2 unifié
        cache_L2_config = "ul2:64:32:8:l"
    
    elif cortex=="A15":
        # Spécifications du cache L2 unifié
        cache_L2_config = "ul2:512:64:16:l"

    # Boucle sur les tailles de cache L1
    for nsets in nsets_L1:
        command = f"{simulator_path} -cache:il1 "
        if cortex=='A7':
            command += f"il1:{nsets}:32:2:l -cache:dl1 "
            command += f"dl1:{nsets}:32:2:l "
        elif cortex=='A15':
            command += f"il1:{nsets}:64:2:l -cache:dl1 "
            command += f"dl1:{nsets}:64:2:l "
        command += f"-cache:dl2 {cache_L2_config} {test_program}"

        # Générer le nom du fichier de sortie pour cette taille de cache
        output_file = f"{output_file_base}{nsets}.txt"
    
        # Afficher les résultats de la simulation
        with open(output_file, 'w') as output_file_handle:
            print(f"Simulation avec cache L1 de {nsets} elements:")
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            # Écrire les résultats de la simulation dans le fichier
            output_file_handle.write(f"Simulation avec cache L1 de {nsets}KB:\n")
            output_file_handle.write(f"Résultats de la simulation: {stderr.decode()}\n")

        for recherche in utile: 
            numero_ligne_trouvee = chercher_mot_dans_fichier(output_file, recherche)
            tableau_caracteres = obtenir_tableau_caracteres_par_ligne(output_file, numero_ligne_trouvee)
            trouve = trouve_entier(tableau_caracteres, recherche)
            tableau_resultat = obtenir_tableau_par_nom(recherche)
            tableau_resultat.append(trouve)

def plot_graph(abscisses, ordonnees_listes, plusieurs, labels, titre, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    if plusieurs: 
        for i, ordonnees in enumerate(ordonnees_listes):
            label_value = labels[i] if labels else f"Série {i + 1}"
            plt.plot(abscisses, ordonnees, label=label_value)
    else:
        for i, ordonnees in enumerate(ordonnees_listes):
            label_value = labels[i] if labels else f"Série {i + 1}"
            plt.plot(abscisses, ordonnees_listes, label=None)

    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.savefig(titre + ".png")  # Sauvegarde le graphique au lieu de l'afficher
    plt.close()

def main():
    # Nb d'éléments en fonction des taille des caches L1
    nsets_L1 = [16,32,64,128,256]

    # Chemin vers le simulateur sim-outorder
    simulator_path = "sim-outorder"
    
    # Programme de test à exécuter
    #test_program_dijkstra = "dijkstra/dijkstra_small.ss input.dat"
    #test_program_blowfish = "blowfish/bf.ss input_small.asc"
    test_program_blowfish = "blowfish/bf.ss"
    test_program_dijkstra = "dijkstra/dijkstra_small.ss"

    generate_result(simulator_path, test_program_dijkstra, "A7", nsets_L1)
    #generate_result(simulator_path, test_program_dijkstra, "A15", nsets_L1)
    #generate_result(simulator_path, test_program_blowfish, "A7", nsets_L1)
    #generate_result(simulator_path, test_program_blowfish, "A15", nsets_L1)

    abscisses=[1,2,4,8,16]

    labels = ["sim_inst_rate", "sim_IPC", "bpred_bimod.bpred_addr_rate", "bpred_bimod.bpred_dir_rate", "sim_elapsed_time"]
    ordonnees_listes = [sim_inst_rate_values, sim_IPC_values, bpred_addr_rate_values, bpred_dir_rate_values, sim_elapsed_time_values]

    for i, label in enumerate(labels):
        print(abscisses)
        print(ordonnees_listes[i])
        plot_graph(abscisses, ordonnees_listes[i], False,None, "Graphique des " + obtenir_nom_tableau(ordonnees_listes[i]) + " en fonction de la taille du cache L1, blowfish, cortex = A15.","Taille du cache L1", obtenir_nom_tableau(ordonnees_listes[i])) 

    labels = ["accesses", "misses","replacement"]

    plot_graph(abscisses, [il1_accesses_values,il1_misses_values,il1_replacement_values], True, labels, "Graphique de Hiérarchie mémoire il1 en fonction de la taille du cache L1, blowfish, cortex = A15.", "Taille du cache L1", "Hiérarchie mémoire")
    plot_graph(abscisses, [dl1_accesses_values,dl1_misses_values,dl1_replacement_values], True,labels, "Graphique de Hiérarchie mémoire dl1 en fonction de la taille du cache L1, blowfish, cortex = A15.", "Taille du cache L1", "Hiérarchie mémoire")
    plot_graph(abscisses, [ul2_accesses_values,ul2_misses_values,ul2_replacement_values], True,labels, "Graphique de Hiérarchie mémoire ul2 en fonction de la taille du cache L1, blowfish, cortex = A15.", "Taille du cache L1", "Hiérarchie mémoire")

if __name__ == "__main__":
    main()