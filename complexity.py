
import random
import time
import matplotlib.pyplot as plt
from functions import ford_fulkerson

def generate_random_flow_problem(n, with_cost=False):
    C = [[0]*n for _ in range(n)]
    D = [[0]*n for _ in range(n)] if with_cost else None

    edges_to_fill = (n * n) // 2
    filled_edges = 0

    while filled_edges < edges_to_fill:
        i, j = random.randint(0, n-1), random.randint(0, n-1)
        if i != j and C[i][j] == 0:
            C[i][j] = random.randint(1, 100)
            if with_cost:
                D[i][j] = random.randint(1, 100)
            filled_edges += 1

    return (C, D) if with_cost else (C, None)

def measure_algorithm_time(algorithm, graph, *args, **kwargs):
    start = time.perf_counter()
    result = algorithm(graph, *args, **kwargs, verbose=False)
    end = time.perf_counter()
    return end - start, result


def run_complexity_tests():
    sizes = [10, 20, 40, 100, 400, 1000]
    iterations = 100
    results = {}

    for n in sizes:
        times_ff = []

        for _ in range(iterations):
            C, _ = generate_random_flow_problem(n)
            graph_copy = [row[:] for row in C]
            duration, _ = measure_algorithm_time(ford_fulkerson, graph_copy)
            times_ff.append(duration)

        results[n] = {
            "Ford-Fulkerson": times_ff,
        }

        print(f"Taille {n} terminée")

    return results

def plot_results(results):
    for algo in ["Ford-Fulkerson"]:
        for n, times in results.items():
            plt.scatter([n]*len(times[algo]), times[algo], label=f"{algo}" if n == list(results.keys())[0] else "", alpha=0.3)

    plt.xlabel("Taille n du graphe")
    plt.ylabel("Temps d'exécution (s)")
    plt.title("Nuage de points - Complexité de Ford-Fulkerson")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    results = run_complexity_tests()
    plot_results(results)
