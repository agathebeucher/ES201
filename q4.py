import subprocess
# Tailles de cache L1 d'instructions et de données à tester (en KB)
'''
Explication à quoi correspond nb_elem_L1 par rapport à la taille des caches L1 :

    Pour chaque taille de cache donnée {1KB,2KB,4KB,8KB,16KB}, correspond un 'nb_elem_L1' qui dépend de l'associativité 
    et du nb de bloc, et qui correspond au premier argument à dans les config du cache le cache calculé (voir overleaf)

PAR EXEMPLE : pour 4KB, associativité de 1 et bloc size de 32, on a 128 nb d'elements et ils faut comme config :
il1:128:32:1:l 
'''

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
    
        # Afficher les résultats de la simulation
        print(f"Simulation avec cache L1 de {nsets} elements:")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())  # Affichage de la sortie de la simulation

def main():
    # Nb d'éléments en fonction des taille des caches L1
    nsets_L1 = [16,32,64,128,256]

    # Chemin vers le simulateur sim-outorder
    simulator_path = "sim-cache"
    
    # Programme de test à exécuter
    #test_program_dijkstra = "dijkstra/dijkstra_small.ss input.dat"
    #test_program_blowfish = "blowfish/bf.ss input_small.asc"
    test_program_blowfish = "blowfish/bf.ss"
    test_program_dijkstra = "dijkstra/dijkstra_small.ss"


    generate_result(simulator_path, test_program_dijkstra, "A7", nsets_L1)
    generate_result(simulator_path, test_program_dijkstra, "A15", nsets_L1)
    generate_result(simulator_path, test_program_blowfish, "A7", nsets_L1)
    generate_result(simulator_path, test_program_blowfish, "A15", nsets_L1)

if __name__ == "__main__":
    main()
