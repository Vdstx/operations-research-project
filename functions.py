from collections import deque
import copy

def graph_import(link):
    with open(link, 'r') as f:
        lines = f.readlines()
    graph = []
    type_of_problem = 1 if len(lines) > int(lines[0]) + 1 else 2
    for line in lines[1:]:
        values = list(map(int, line.split()))
        graph.append(values)
    return (graph, type_of_problem)

def print_graph_to_matrix_of_values(liste_adjacence):
    n = len(liste_adjacence)
    matrice = [['*' for _ in range(n)] for _ in range(n)]
    print("La matrice de capacité")
    header = "    " + "  ".join(str(i) if i > 0 and i < n-1 else "s" if i == 0 else "t" for i in range(n))
    col_width = max(len(str(n)), 2)
    separator = "   " + "-" * (n * (col_width + 1))
    print(header)
    print(separator)
    for i in range(n):
        row = f"{i if (i > 0 and i < n-1) else 's' if i == 0 else 't'} | " + "  ".join(
            matrice[i][j] if j < len(matrice[i]) else ' * ' for j in range(n))
        print(row)

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

def compute_flow_matrix(original_graph, residual_graph):
    n = len(original_graph)
    matrice = [['*' for _ in range(n)] for _ in range(n)]
    print("La matrice de capacité")
    for i in range(n):
        for j in range(len(original_graph[i])):
            if original_graph[i][j] != 0:
                matrice[i][j] = str(original_graph[i][j] - residual_graph[i][j]) + '/' + str(original_graph[i][j])
    header = "    " + "  ".join(str(i) if i > 0 and i < n - 1 else "s" if i == 0 else "t" for i in range(n))
    col_width = max(len(str(n)), 2)
    separator = "   " + "-" * (n * (col_width + 1))
    print(header)
    print(separator)
    for i in range(n):
        row = f"{i if (i > 0 and i < n - 1) else 's' if i == 0 else 't'} | " + "  ".join(
            matrice[i][j] if j < len(matrice[i]) else ' * ' for j in range(n))
        print(row)