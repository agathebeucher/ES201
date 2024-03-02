import matplotlib.pyplot as plt

# Tailles des caches (en bytes)
cache_sizes = [0, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 1073741824]

# Surface des caches L1 pour Cortex-A7 (en mm^2)
surface_cache_L1_A7 = [0, 0.65, 1.22, 2.3, 3.78, 6.91, 9.87, 16.84, 32.58, 212.95]

# Surface des caches L1 pour Cortex-A15 (en mm^2)
surface_cache_L1_A15 = [0, 1.29, 1.86, 2.94, 4.42, 7.55, 10.51, 17.48, 33.22, 213.59]

# Surface totale des Cortex (Cortex-A7 + L2 inclus) (en mm^2)
total_surface_A7 = [0.33, 1.29, 1.86, 2.94, 4.42, 7.55, 10.51, 17.48, 33.22, 213.59]
total_surface_A15 = [1.88, 2.84, 3.41, 4.49, 5.97, 9.10, 12.06, 19.03, 34.77, 215.14]

# Affichage des données
plt.plot(cache_sizes, total_surface_A7, label='Total C-A7')
plt.plot(cache_sizes, total_surface_A15, label='Total C-A15')
plt.xlabel('Taille des caches (Bytes)')
plt.ylabel('Surface totale (mm^2)')
plt.title('Surface totale des Cortex en fonction de la taille des caches')
plt.legend()
plt.grid(True)
plt.xscale('log')  # Mettre l'échelle logarithmique sur l'axe x pour mieux visualiser les données
plt.show()