from functions import (
    generate_random_flow_problem,
    ford_fulkerson,
    push_relabel,
    min_cost_max_flow,
    graph_import,
    print_graph_to_matrix_of_values,
    compute_flow_matrix
)
from complexity import measure_algorithm_time
from tqdm import trange
import json
import time
import matplotlib.pyplot as plt

def save_results_json(results, filename="results.json"):
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\n📁 Résultats sauvegardés dans {filename}")

def plot_all_algorithms(times_dict, n):
    plt.figure(figsize=(10, 5))
    for algo, times in times_dict.items():
        plt.plot(range(1, len(times) + 1), times, marker='o', linestyle='-', label=algo)
    plt.xlabel("Itération")
    plt.ylabel("Temps d'exécution (s)")
    plt.title(f"Comparaison des temps d'exécution – n = {n}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def run_single_full_test(n):
    C, D = generate_random_flow_problem(n)
    durations = {}

    C1 = [row[:] for row in C]
    durations["Ford-Fulkerson"], _ = measure_algorithm_time(
        ford_fulkerson, graph=C1, s=0, t=len(C1)-1, verbose=False
    )

    C2 = [row[:] for row in C]
    durations["Push-Relabel"], _ = measure_algorithm_time(
        push_relabel, graph=C2, source=0, sink=len(C2)-1
    )

    C3 = [row[:] for row in C]
    D3 = [row[:] for row in D]
    durations["Flot à coût min"], _ = measure_algorithm_time(
        min_cost_max_flow, graph=C3, cost=D3, source=0, sink=len(C3)-1
    )

    return durations

def custom_test(n, k):
    print(f"\n🔬 Étude de complexité sur {k} itérations pour un graphe de taille {n}...")
    start_time = time.perf_counter()

    algo_times = {
        "Ford-Fulkerson": [],
        "Push-Relabel": [],
        "Flot à coût min": []
    }

    for _ in trange(k, desc=f"⏳ Lancement des {k} itérations"):
        result = run_single_full_test(n)
        for algo in algo_times:
            algo_times[algo].append(result[algo])

    total_time = time.perf_counter() - start_time
    print(f"\n🕒 Temps total pour {k} itérations : {total_time:.4f} s\n")

    for algo in algo_times:
        max_time = max(algo_times[algo])
        avg_time = sum(algo_times[algo]) / len(algo_times[algo])
        print(f"⏱️ {algo:<20} | Max : {max_time:.4f} s | Moyenne : {avg_time:.4f} s")

    return {n: algo_times}

if __name__ == "__main__":
    print("Souhaitez-vous tester un graphe (1) ou faire l’étude de complexité (2) ?")
    choix = input("Entrez 1 ou 2 : ")

    if choix == "1":
        imported_data = graph_import("graphs/graph1.txt")
        graph, flow_type = imported_data
        if flow_type == 1:
            print("problème de flot à coût minimal")
        else:
            print("problème de flot maximal")
        print_graph_to_matrix_of_values(graph)
        if flow_type == 2:
            ff_mat = ford_fulkerson(graph)[1]
            compute_flow_matrix(graph, ff_mat)

    elif choix == "2":
        try:
            taille = int(input("👉 Entrez la taille n du graphe (ex : 10, 100, 1000) : "))
            repetitions = int(input("👉 Entrez le nombre d’itérations (ex : 10, 50, 100) : "))
        except ValueError:
            print("❌ Entrée invalide. Veuillez entrer des entiers valides.")
        else:
            results = custom_test(taille, repetitions)
            plot_all_algorithms(results[taille], taille)
            save_results_json(results)