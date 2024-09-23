from graph import *
from typing import *
import time

def backtrack_solver(g: Graph) -> tuple[bool, list[int]]:
    edges = g.get_edges()
    degrees = {k: 0 for k in g.get_vertices()}
    edges_selection = [False] * len(edges)
    return bottom_up_backtrack(edges, degrees, edges_selection)


def bottom_up_backtrack(
    edges: list,
    degrees: dict[Any, int],
    edges_selection: list[bool],
    actual_index: int = 0,
) -> tuple[bool, list[int]]:
    all_valid = all(valor in (0, 3) for valor in degrees.values())
    at_least_one_connection = any(valor > 0 for valor in degrees.values())
    if all_valid and at_least_one_connection:
        return True, edges_selection
    if actual_index == len(edges):
        return False, None

    x, y = edges[actual_index]
    if degrees[x] < 3 and degrees[y] < 3:
        degrees[x] += 1
        degrees[y] += 1
        edges_selection[actual_index] = True

        solved, solution = bottom_up_backtrack(edges, degrees, edges_selection, actual_index + 1)
        if solved:
            return True, solution

        degrees[x] -= 1
        degrees[y] -= 1
        edges_selection[actual_index] = False
        return bottom_up_backtrack(edges, degrees, edges_selection, actual_index + 1)

    return False, None


def get_edges(edges: list, edges_mask: list[bool]) -> list:
    if len(edges) != len(edges_mask):
        raise Exception("The edge list and edge mask have different lengths")

    result = []
    for i in range(len(edges)):
        if edges_mask[i]:
            result.append(edges[i])
    return result


def draw_graph_and_solution(g: Graph, edge_solution: list):
    # TODO: Check for errors
    edge_color_map2 = {edge:"green" for edge in edge_solution}
    edge_width_map2 = {edge:4 for edge in edge_solution}
    draw_two_graphs(
        g,
        g,
        edge_color_map2=edge_color_map2,
        edge_width_map2=edge_width_map2,
    )

now = time.time()
print("generating graph")
g = generate_random_graph(10, 30)

print(f"graph generated: {(time.time() - now)} seconds")
now = time.time()
solved, solution = backtrack_solver(g)
print(f"backtrack finished {(time.time() - now)} seconds")
if solved:
    print(f"Solution founded")
    new_edges = get_edges(g.get_edges(), solution)
    draw_graph_and_solution(g, new_edges)
else:
    print("Solution not found")
