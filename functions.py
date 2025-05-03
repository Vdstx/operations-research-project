import random
from collections import deque
import collections

def generate_random_flow_problem(n, max_capacity=20, max_cost=10):
    C = [[0]*n for _ in range(n)]
    D = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < 0.3:
                C[i][j] = random.randint(1, max_capacity)
                D[i][j] = random.randint(1, max_cost)
    return C, D

def ford_fulkerson(graph, s, t, verbose=False):
    n = len(graph)
    residual = [row[:] for row in graph]
    parent = [-1] * n
    max_flow = 0
    flow_matrix = [[0]*n for _ in range(n)]

    def bfs():
        nonlocal parent
        visited = [False] * n
        queue = deque([s])
        visited[s] = True
        while queue:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and residual[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
        return visited[t]

    while bfs():
        path_flow = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = parent[v]

        v = t
        while v != s:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            flow_matrix[u][v] += path_flow
            v = parent[v]

        max_flow += path_flow

    return max_flow, flow_matrix

import collections

from collections import deque

from collections import deque

def push_relabel(graph, source, sink):
    n = len(graph)
    height = [0] * n
    excess = [0] * n
    flow = [[0] * n for _ in range(n)]

    def push(u, v):
        send = min(excess[u], graph[u][v] - flow[u][v])
        flow[u][v] += send
        flow[v][u] -= send
        excess[u] -= send
        excess[v] += send
        if excess[v] > 0 and v != source and v != sink and v not in active:
            active.append(v)

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

    active = deque([i for i in range(n) if i != source and i != sink and excess[i] > 0])

    while active:
        u = active.popleft()
        old_height = height[u]
        discharge(u)
        if excess[u] > 0 and height[u] > old_height:
            active.append(u)

    return sum(flow[source][v] for v in range(n))




def min_cost_max_flow(cap, cost, source, sink, target_flow):
    n = len(cap)
    flow = [[0]*n for _ in range(n)]
    total_flow = 0
    total_cost = 0

    def bellman_ford():
        dist = [float('inf')] * n
        in_queue = [False] * n
        parent = [-1] * n
        dist[source] = 0
        queue = deque([source])
        in_queue[source] = True
        while queue:
            u = queue.popleft()
            in_queue[u] = False
            for v in range(n):
                if cap[u][v] - flow[u][v] > 0 and dist[v] > dist[u] + cost[u][v]:
                    dist[v] = dist[u] + cost[u][v]
                    parent[v] = u
                    if not in_queue[v]:
                        queue.append(v)
                        in_queue[v] = True
        return dist, parent

    while total_flow < target_flow:
        dist, parent = bellman_ford()
        if parent[sink] == -1:
            break

        increment = target_flow - total_flow
        v = sink
        while v != source:
            u = parent[v]
            increment = min(increment, cap[u][v] - flow[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += increment
            flow[v][u] -= increment
            total_cost += increment * cost[u][v]
            v = u

        total_flow += increment

    return total_flow, total_cost