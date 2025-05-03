from functions import (
    generate_random_flow_problem,
    ford_fulkerson,
    push_relabel,
    min_cost_max_flow
)
from complexity import measure_algorithm_time
import matplotlib.pyplot as plt
from functions_max_flow import *
import time

def plot_all_algorithms(results, n, k):
    plt.figure(figsize=(10, 6))
    for algo, times in results.items():
        plt.plot(range(1, k+1), times, label=algo)
    plt.xlabel("Numéro d'itération")
    plt.ylabel("Temps d'exécution (s)")
    plt.title(f"Comparaison des temps d'exécution pour n={n}, k={k}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def run_tests(n, k):
    times = {
        "Ford-Fulkerson": [],
        "Push-Relabel": [],
        "Min-Cost Max-Flow": []
    }

    print(f"\n🔬 Étude de complexité sur {k} itérations pour un graphe de taille {n}...")
    start_total = time.perf_counter()
    for i in range(k):
        print(f"\r⏳ Lancement des {k} itérations: {i+1}/{k}", end="")

        cap, cost = generate_random_flow_problem(n)

        # Ford-Fulkerson
        cap_ff = [row[:] for row in cap]
        t_ff, result_ff = measure_algorithm_time(ford_fulkerson, cap_ff, 0, n-1)
        max_flow_ff = result_ff[0]
        times["Ford-Fulkerson"].append(t_ff)

        # Push-Relabel
        cap_pr = [row[:] for row in cap]
        t_pr, max_flow_pr = measure_algorithm_time(push_relabel, cap_pr, 0, n-1)
        times["Push-Relabel"].append(t_pr)

        # Min-Cost Max-Flow
        cap_mc = [row[:] for row in cap]
        cost_mc = [row[:] for row in cost]
        target_flow = max_flow_ff // 2 if max_flow_ff > 0 else 1  # éviter division par 0
        t_mc, _ = measure_algorithm_time(min_cost_max_flow, cap_mc, cost_mc, 0, n-1, target_flow)
        times["Min-Cost Max-Flow"].append(t_mc)

    end_total = time.perf_counter()
    print(f"\n✅ Test terminé en {end_total - start_total:.2f} secondes.")
    return times

def print_max_per_algorithm(times):
    print("\n📈 Temps maximal observé pour chaque algorithme :")
    for algo, tlist in times.items():
        print(f" - {algo} : {max(tlist):.4f} s")

if __name__ == "__main__":
    print("Tapez 'test' pour tester un graphe aléatoire ou 'complexité' pour lancer une étude de complexité :")
    mode = input().strip().lower()

    if mode == "complexité":
        try:
            n = int(input("👉 Entrez la taille n du graphe : "))
            k = int(input("👉 Entrez le nombre d’itérations k : "))
        except ValueError:
            print("❌ Veuillez entrer des entiers valides.")
        else:
            results = run_tests(n, k)
            print_max_per_algorithm(results)
            plot_all_algorithms(results, n, k)

    elif mode == "graphe":
        imported_data = graph_import("graphs/graph1.txt")
        graph = imported_data[0]
        flow_type = imported_data[1]
        if flow_type == 1:
            print("problème de flot à cout minimal")
        else:
            print("problème de flot maximal") #méthode F-F ou pousser-réétiqueter

        print_graph_to_matrix_of_values(graph)

        if flow_type == 2:  # flot max
            print_graph_to_matrix_of_values(graph)
            print("\n =========== ford fulkerson ===========\n")
            ff_mat = ford_fulkerson(graph)[1]
            compute_flow_matrix(graph, ff_mat)
            print("\n =========== push-label ===========\n")
            pl = push_relabel(graph,0,len(graph)-1)
            print('\n valeurs du poussé réétiqueté : ' + str(pl))

    else:
        print("❌ Mode inconnu. Tapez 'test' ou 'complexité'.")
