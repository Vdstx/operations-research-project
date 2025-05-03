from functions import *
from complexity import (
    generate_random_flow_problem,
    measure_algorithm_time,
    plot_results
)
import json
from tqdm import trange

def save_results_json(results, filename="results.json"):
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\n📁 Résultats sauvegardés dans {filename}")

def save_results_markdown(results, filename="results.md"):
    with open(filename, "w") as f:
        f.write("# Résultats des tests de complexité - Ford-Fulkerson\\n\\n")
        for n, data in results.items():
            f.write(f"## Taille n = {n}\\n")
            f.write(f"- Temps max : {max(data['Ford-Fulkerson']):.4f} s\\n")
            f.write("- Temps pour chaque itération :\\n")
            for i, t in enumerate(data["Ford-Fulkerson"]):
                f.write(f"  - Itération {i+1}: {t:.4f} s\\n")
            f.write("\\n")
    print(f"📄 Résultats sauvegardés dans {filename}")

def custom_test(n, k):
    print(f"\n⏳ Lancement de {k} itérations pour un graphe de taille {n}...")
    times_ff = []
    for i in trange(k, desc="Progression"):
        C, _ = generate_random_flow_problem(n)
        graph_copy = [row[:] for row in C]
        duration, _ = measure_algorithm_time(ford_fulkerson, graph_copy)
        times_ff.append(duration)

    max_time = max(times_ff)
    print(f"\n📈 Temps max observé pour n = {n} : {max_time:.4f} s")
    return {n: {"Ford-Fulkerson": times_ff}}

if __name__ == "__main__":
    print("Souhaitez-vous tester un graphe (1) ou faire l'étude de complexité (2) ?")
    choix = input("Entrez 1 ou 2 : ")

    if choix == "1":
        imported_data = graph_import("graphs/graph1.txt")
        graph = imported_data[0]
        flow_type = imported_data[1]

        if flow_type == 1:
            print("problème de flot à coût minimal")
        else:
            print("problème de flot maximal")  # méthode F-F ou pousser-réétiqueter

        print_graph_to_matrix_of_values(graph)

        if flow_type == 2:  # flot max
            print_graph_to_matrix_of_values(graph)
            ff_mat = ford_fulkerson(graph)[1]
            compute_flow_matrix(graph, ff_mat)

    elif choix == "2":
        print("\n🔬 Étude de complexité de Ford-Fulkerson")
        try:
            taille = int(input("👉 Entrez la taille n du graphe (ex : 10, 100, 1000) : "))
            repetitions = int(input("👉 Entrez le nombre d’itérations (ex : 10, 50, 100) : "))
        except ValueError:
            print("❌ Entrée invalide. Veuillez entrer des entiers valides.")
        else:
            results = custom_test(taille, repetitions)
            plot_results(results)
            save_results_json(results)
            save_results_markdown(results)