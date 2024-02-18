import subprocess
# Tailles de cache L1 d'instructions et de données à tester (en KB)
cache_sizes = [1, 2, 4, 8, 16]

# Spécifications du cache L2 unifié
cache_l2_config = "ul2:1024:64:4:l"

# Chemin vers le simulateur sim-outorder
simulator_path = "sim-outorder"

# Programme de test à exécuter
test_program = "dijkstra/dijkstra_small.ss input_small.asc"

# Boucle sur les tailles de cache L1
for size in cache_sizes:
    # Générer le fichier de configuration pour cette taille de cache
    config_file = f"config_cache_{size}KB.ini"
    with open(config_file, 'w') as f:
        f.write(f"-cache:il1 ")
        f.write(f"il1:{size}:32:1:l ")
        f.write(f"-cache:dl1 ")
        f.write(f"dl1:{size}:32:1:l ")
        f.write(f"-cache:il2 dl2 ")
        f.write(f"-cache:dl2 {cache_l2_config}")

    # Exécuter la simulation avec cette configuration
    command = f"{simulator_path} -config {config_file} {test_program}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Afficher les résultats de la simulation
    print(f"Simulation avec cache L1 de {size}KB:")
    if stderr:
        print("Erreur lors de la simulation:", stderr.decode())
    else:
        print("Résultats de la simulation:", stdout.decode())
    # Supprimer le fichier de configuration après la simulation
    subprocess.run(["rm", config_file])