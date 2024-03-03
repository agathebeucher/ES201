import os
import matplotlib
matplotlib.use('Agg')  # Utiliser le backend non interactif pour matplotlib
import matplotlib.pyplot as plt

taille_L1_A7 = [1024, 2048, 4096, 8192, 16384]
taille_L1_A15= [2048, 4096, 8192, 16384,32768]

def calcul_surface_L1(cortex, taille_L1):
    surface_L1_tab= []
    surface_totale=[]
    taille_cache=0.0

    if cortex == 'A7' :
        surface_L2 = 0.48
        bloc = 32
    if cortex == 'A15' :
        surface_L2 = 0.42
        bloc = 64
        
    # Ouvre le fichier 'cache.cfg', cherche le block size et le change
    with open("cache.cfg", "r") as file:
        lines = file.readlines()
    for index, line in enumerate(lines):
        if "-block size (bytes)" in line:
            lines[index] = f"-block size (bytes) {bloc}\n" 
            break
    with open("cache.cfg", "w") as file:
        file.writelines(lines)

    # Pour chaque taille de L1, change config.sfg avec cette taille
    for taille in taille_L1:
        with open("cache.cfg", "r") as file:
            lines = file.readlines()
        for index, line in enumerate(lines):
            if "-size (bytes)" in line:
                lines[index] = f"-size (bytes) {taille}\n"
                break
        with open("cache.cfg", "w") as file:
            file.writelines(lines)

        # Execute cacti et enregistre la sortie terminal
        output_terminal = os.popen("./cacti -infile cache.cfg").read()

        for line in output_terminal.split("\n"):
            if "Cache height x width (mm):" in line:
                dimensions = line.split(":")[1].strip()
                dimensions = dimensions.split("x")
                surface_L1 = float(dimensions[0].strip()) * float(dimensions[1].strip())

        # Enregistrement de la donnée lu de la surface de L1
        surface_L1_tab.append(surface_L1)

        # Calculate the total area
        surface_totale = [L1 + surface_L2 for L1 in surface_L1_tab]

    return surface_L1_tab,surface_totale

# Cortex-A15
Cortex_1 = 'A15'
A15_L1, A15_surface_totale = calcul_surface_L1(Cortex_1, taille_L1_A15)
print("Cortex A15 : taille_L1_A15", taille_L1_A15,"Surfaces des caches L1", A15_L1, "Surfaces totales :", A15_surface_totale)

# Cortex-A7
Cortex_2 = 'A7'
A7_L1, A7_surface_totale = calcul_surface_L1(Cortex_2,taille_L1_A7)
print("Cortex A7 : taille_L1_A7",taille_L1_A7,"Surfaces des caches L1", A7_L1, "Surfaces totales :", A7_surface_totale)


# Tracer les graphes des surfaces totales en fonction de la taille de L1
plt.figure(figsize=(10, 6))
plt.plot(taille_L1_A7, A7_surface_totale, marker='o', label='Cortex A7')
plt.plot(taille_L1_A15, A15_surface_totale, marker='o', label='Cortex A15')
plt.xlabel('Taille du cache L1 (octets)')
plt.ylabel('Surface totale du cache (mm2)')
plt.title('Surface totale du cache en fonction de la taille du cache L1')
plt.grid(True)
plt.legend()
plt.savefig('/home/b/beucher/ES201/surface_totale_vs_taille_L1.png')

# Tracer les graphes des surfaces L1 en fonction de la taille de L1
plt.figure(figsize=(10, 6))
plt.plot(taille_L1_A7, A7_L1, marker='o', label='Cortex A7')
plt.plot(taille_L1_A15, A15_L1, marker='o', label='Cortex A15')
plt.xlabel('Taille du cache L1 (octets)')
plt.ylabel('Surface du cache L1 (mm2)')
plt.title('Surface du cache L1 en fonction de la taille du cache L1')
plt.grid(True)
plt.legend()
plt.savefig('/home/b/beucher/ES201/surface_L1_vs_taille_L1.png')


