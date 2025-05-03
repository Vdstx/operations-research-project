from collections import deque
import copy
import math
import collections
import random

def graph_import(link):
    with open(link, 'r') as f:
        lines = f.readlines()
    graph = []
    type_of_problem = 1 if len(lines) > int(lines[0]) + 1 else 2
    for line in lines[1:]:
        values = list(map(int, line.split()))
        graph.append(values)
    return (graph, type_of_problem)

def generate_random_flow_problem(n, max_capacity=20, max_cost=10):
    C = [[0]*n for _ in range(n)]
    D = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < 0.3:
                C[i][j] = random.randint(1, max_capacity)
                D[i][j] = random.randint(1, max_cost)
    return C, D

def ford_fulkerson(graph, s=0, t=None, verbose=True):
    n = len(graph)
    if t is None:
        t = n - 1

    max_flow = 0
    residual = copy.deepcopy(graph)
    iteration = 1

    while True:
        if verbose:
            print(f"\\n🌀 Itération {iteration} :")
        parent = [-1] * n
        flow, path = bfs(residual, s, t, parent)

        if flow == 0:
            if verbose:
                print("❌ Aucun chemin améliorant trouvé. L'algorithme s'arrête.")
            break

        if verbose:
            print(f"✔️ Chaîne améliorante trouvée : {' → '.join(map(str, path))}")
            print(f"🔁 Valeur de flot pour cette chaîne : {flow}")

        u = t
        while u != s:
            v = parent[u]
            residual[v][u] -= flow
            residual[u][v] += flow
            u = v

        max_flow += flow

        if verbose:
            print("📊 Graphe résiduel mis à jour :")
            print_graph_to_matrix_of_values(residual)

        iteration += 1

    if verbose:
        print(f"\\n🌊 Flot maximal trouvé : {max_flow}")
    return max_flow, residual

def bfs(residual, s, t, parent):
    n = len(residual)
    visited = [False] * n
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and residual[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)
                if v == t:
                    path = []
                    curr = t
                    while curr != -1:
                        path.append(curr)
                        curr = parent[curr]
                    path.reverse()
                    min_capacity = min(residual[parent[v]][v] for v in path[1:])
                    return min_capacity, path
    return 0, []

def push_relabel(graph, source=0, sink=None):
    n = len(graph)
    if sink is None:
        sink = n - 1
    height = [0] * n
    excess = [0] * n
    flow = [[0] * n for _ in range(n)]

    def push(u, v):
        send = min(excess[u], graph[u][v] - flow[u][v])
        flow[u][v] += send
        flow[v][u] -= send
        excess[u] -= send
        excess[v] += send

    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            if graph[u][v] - flow[u][v] > 0:
                min_height = min(min_height, height[v])
        if min_height < float('inf'):
            height[u] = min_height + 1

    def discharge(u):
        while excess[u] > 0:
            for v in range(n):
                if graph[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
                    push(u, v)
                    if excess[u] == 0:
                        break
            else:
                relabel(u)

    height[source] = n
    for v in range(n):
        if graph[source][v] > 0:
            flow[source][v] = graph[source][v]
            flow[v][source] = -graph[source][v]
            excess[v] = graph[source][v]
            excess[source] -= graph[source][v]

    active = collections.deque([i for i in range(n) if i != source and i != sink and excess[i] > 0])
    while active:
        u = active.popleft()
        old_height = height[u]
        discharge(u)
        if excess[u] > 0 and height[u] > old_height:
            active.append(u)

    return sum(flow[source][v] for v in range(n))

def bellman_ford(graph, cost, source, sink):
    n = len(graph)
    distance = [math.inf] * n
    parent = [-1] * n
    distance[source] = 0

    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if graph[u][v] > 0 and distance[u] + cost[u][v] < distance[v]:
                    distance[v] = distance[u] + cost[u][v]
                    parent[v] = u
    return distance, parent

def min_cost_max_flow(graph, cost, source=0, sink=None):
    n = len(graph)
    if sink is None:
        sink = n - 1
    flow = 0
    min_cost = 0
    residual = [row[:] for row in graph]

    while True:
        distance, parent = bellman_ford(residual, cost, source, sink)
        if distance[sink] == math.inf:
            break

        increment = math.inf
        v = sink
        while v != source:
            u = parent[v]
            increment = min(increment, residual[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= increment
            residual[v][u] += increment
            min_cost += increment * cost[u][v]
            v = u

        flow += increment

    return flow, min_cost

def print_graph_to_matrix_of_values(liste_adjacence):
    n = len(liste_adjacence)
    print("La matrice de capacité")
    header = "    " + "  ".join(str(i) if i > 0 and i < n-1 else "s" if i == 0 else "t" for i in range(n))
    separator = "   " + "-" * (n * 3)
    print(header)
    print(separator)
    for i in range(n):
        row = f"{i if (i > 0 and i < n-1) else 's' if i == 0 else 't'} | " + "  ".join(
            str(liste_adjacence[i][j]) if j < len(liste_adjacence[i]) else '*' for j in range(n))
        print(row)

def compute_flow_matrix(original_graph, residual_graph):
    n = len(original_graph)
    print("La matrice de flot")
    header = "    " + "  ".join(str(i) if i > 0 and i < n - 1 else "s" if i == 0 else "t" for i in range(n))
    separator = "   " + "-" * (n * 3)
    print(header)
    print(separator)
    for i in range(n):
        row = f"{i if (i > 0 and i < n - 1) else 's' if i == 0 else 't'} | " + "  ".join(
            str(original_graph[i][j] - residual_graph[i][j]) + '/' + str(original_graph[i][j])
            if original_graph[i][j] > 0 else '*'
            for j in range(n))
        print(row)