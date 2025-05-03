
import random
import time
import matplotlib.pyplot as plt
import numpy as np

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

def measure_algorithm_time(algorithm, *args, **kwargs):
    import time
    start = time.perf_counter()
    result = algorithm(*args, **kwargs)
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
    plt.figure(figsize=(10, 6))
    for algo in ["Ford-Fulkerson"]:
        for n, times in results.items():
            x_jitter = np.random.normal(loc=n, scale=0.2, size=len(times[algo]))
            plt.scatter(x_jitter, times[algo], alpha=0.5, label=f"{algo} (n={n})")

    plt.xlabel("Taille n du graphe", fontsize=12)
    plt.ylabel("Temps d'exécution (s)", fontsize=12)
    plt.title("⏱️ Complexité de l'algorithme Ford-Fulkerson", fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_iterations_vs_time(times, n):
    plt.figure(figsize=(10, 5))
    x_vals = list(range(1, len(times) + 1))  # 1 à k
    plt.plot(x_vals, times, marker='o', linestyle='-')
    plt.xlabel("Numéro de l’itération")
    plt.ylabel("Temps d’exécution (s)")
    plt.title(f"Temps d'exécution par itération – Ford-Fulkerson (n = {n})")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    results = run_complexity_tests()
    plot_results(results)
