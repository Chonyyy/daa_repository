from typing import List, Tuple, Dict
from random import randint
from collections import defaultdict as dd
from math import inf

class Edge:
    def __init__(self, cap: int, cost: int):
        self.cap = cap
        self.cost = cost

    def __repr__(self) -> str:
        return f'({self.cap}, {self.cost})'

def add_edge(graph: Dict[int, Dict[int, Edge]], v: int, u: int, cap: int, cost: int):
    graph[v][u] = Edge(cap, cost)
    graph[u][v] = Edge(0, -cost)

def create_residual_graph(a: List[int]) -> Tuple[Dict[int, Dict[int, Edge]], int, int]:
    graph = dd(lambda: dd(lambda: None))
    n = len(a)
    s = 0
    t = 4 * n + 1
    d = 4 * n + 2
    refer = {}
    modul = {}

    for i in range(n, 0, -1):
        value = a[i - 1]
        add_edge(graph, s, 4 * i - 1, 1, 0)
        add_edge(graph, 4 * i - 3, 4 * i - 1, 1, 0)
        add_edge(graph, 4 * i - 2, 4 * i - 1, 1, 0)
        add_edge(graph, 4 * i - 1, 4 * i, 1, -1)
        add_edge(graph, 4 * i, t, 1, 0)

        iequal_valid = igreater_valid = ilower_valid = imodule_valid = False
        try:
            ie = refer[value]
            iequal_valid = True
        except: pass
        try:
            ig = refer[value + 1]
            igreater_valid = True
        except: pass
        try:
            il = refer[value - 1]
            ilower_valid = True
        except: pass
        try:
            im = modul[value % 7]
            imodule_valid = True
        except: pass

        if iequal_valid: add_edge(graph, 4 * i - 2, 4 * ie - 2, 4, 0)
        if igreater_valid and (not iequal_valid or ig < ie): add_edge(graph, 4 * i, 4 * ig - 2, 1, 0)
        if ilower_valid and (not iequal_valid or il < ie): add_edge(graph, 4 * i, 4 * il - 2, 1, 0)
        if imodule_valid:
            add_edge(graph, 4 * i - 3, 4 * im - 3, 4, 0)
            add_edge(graph, 4 * i, 4 * im - 3, 1, 0)
        refer[value] = modul[value % 7] = i
    
    add_edge(graph, t, d, 4, 0)
    return graph, s, d

def bellman_ford(graph: Dict[int, Dict[int, Edge]], s: int) -> Dict[int, int]:
    d = dd(lambda: inf)
    d[s] = 0
    pi = dd(lambda: None)
    for _ in range(len(graph) - 1):
        for v1, edges in graph.items():
            for v2, p in edges.items():
                if p and p.cap > 0 and d[v1] + p.cost < d[v2]:
                    d[v2] = d[v1] + p.cost
                    pi[v2] = v1
    return pi

def find_path(graph: Dict[int, Dict[int, Edge]], s: int, t: int) -> Tuple[List[Tuple[int, int]], int]:
    pi = bellman_ford(graph, s)
    path = []
    cap = inf
    if pi[t] is not None:
        current = t
        while current != s:
            previous = pi[current]
            path.append((previous, current))
            cap = min(cap, graph[previous][current].cap)
            current = previous
    return path, cap

def min_cost_flow(a: List[int]) -> Tuple[Dict[int, Dict[int, int]], int]:
    graph, s, t = create_residual_graph(a)
    flow = dd(lambda: dd(lambda: 0))
    output = 0

    path, cap = find_path(graph, s, t)
    while path:
        for v1, v2 in path:
            if v2 < v1:
                if graph[v1][v2].cost == -1:
                    output -= 1
                flow[v2][v1] -= cap
                graph[v1][v2].cap -= cap
                graph[v2][v1].cap += cap
            else:
                if graph[v1][v2].cost == -1:
                    output += 1
                flow[v1][v2] += cap
                graph[v1][v2].cap -= cap
                graph[v2][v1].cap += cap
        path, cap = find_path(graph, s, t)
    
    return flow, output

def generate_random_list(n: int, min_value: int = -1000000, max_value: int = 1000000) -> List[int]:
    return [randint(min_value, max_value) for _ in range(n)]

def generate_all_melodies(nums: List[int]) -> List[Tuple[List[int], set[int]]]:
    from itertools import combinations

    results = []
    n = len(nums)
    
    # Generate combinations of all possible lengths
    for r in range(1, n + 1):
        for combo in combinations(enumerate(nums), r):
            melody = [x[1] for x in combo]
            if valid_melody(melody):
                indexes = {x[0] for x in combo}
                results.append((melody, indexes))
    
    return results

def valid_melody(melody: List[int]) -> bool:
    if len(melody) == 1:
        return True
    for index in range(len(melody) - 1):
        if (melody[index] % 7 != melody[index + 1] % 7) and abs(melody[index] - melody[index + 1]) != 1:
            return False
    return True

def count_notes(melodies: List):
    # Use set union to combine all elements
    notes = list(set().union(*melodies))
    return notes