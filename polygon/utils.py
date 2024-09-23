import math
from typing import List, Tuple
from random import randint
# BUG: Matplotlib not working with vscode ???
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

def generate_convex_polygon(n: int) -> List[Tuple[int, int]]:
    """Generate a strictly convex polygon with `n` vertices."""
    angles = sorted([randint(0, 360) for _ in range(n)])
    polygon = [(math.cos(math.radians(angle)), math.sin(math.radians(angle))) for angle in angles]
    return polygon

def generate_possible_cuts(n: int) -> List[Tuple[int, int]]:
    """Generate all possible valid cuts (non-adjacent vertices) in a convex polygon with `n` vertices."""
    cuts = []
    for i in range(n):
        for j in range(i+2, n):  # Ensure non-adjacency
            if (i == 0 and j == n-1):  # Skip the last adjacency case (0, n-1)
                continue
            cuts.append((i, j))
    return cuts

def polygon_area(polygon: List[Tuple[int, int]]) -> float:
    """Calculate the area of the polygon using the Shoelace formula."""
    n = len(polygon)
    area = 0
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i+1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

def get_cut_indexes(polygon: List[Tuple[int, int]], cut_points: List[Tuple[int, int]]):
    return polygon.index(cut_points[0]), polygon.index(cut_points[1])

def apply_cut(polygon: List[Tuple[int, int]], cut_points: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    """Simulate a single cut and return the resulting sub-polygons."""
    if not(cut_points[0] in polygon and cut_points[1] in polygon):
        return [polygon]
    i, j = get_cut_indexes(polygon, cut_points)
    if i > j:
        i, j = j, i
    first_polygon = polygon[i:j+1]
    second_polygon = polygon[:i+1] + polygon[j:]
    return [first_polygon, second_polygon]

def calculate_smallest_region_area(polygon: List[Tuple[int, int]], cuts: List[Tuple[int, int]]) -> float:
    """Apply a series of cuts and return the area of the smallest region formed."""
    regions = [polygon]
    for cut in cuts:
        new_regions = []
        for region in regions:
            cut_points = [polygon[cut[0]], polygon[cut[1]]]
            new_regions.extend(apply_cut(region, cut_points))
        regions = new_regions

    min_area = math.inf
    minimal_region = polygon
    for region in regions:
        region_area = polygon_area(region)
        if region_area < min_area:
            min_area = region_area
            minimal_region = region
    return min_area, minimal_region
    return min(polygon_area(region) for region in regions)

def all_subareas(polygon: List[Tuple[int, int]], cuts: List[Tuple[int, int]]) -> List[int]:
    """Apply a series of cuts and return the area of the smallest region formed."""
    regions = [polygon]
    for cut in cuts:
        new_regions = []
        for region in regions:
            cut_points = [polygon[cut[0]], polygon[cut[1]]]
            new_regions.extend(apply_cut(region, cut_points))
        regions = new_regions

    areas = []
    for region in regions:
        region_area = polygon_area(region)
        areas.append(region_area)
    return areas

def segments_intersect(s1: Tuple[int, int], s2: Tuple[int, int]) -> bool:
    """
    Check if two segments intersect based on vertex indices.
    The segments should not share any common vertices, and their indices should overlap in a circular manner.
    """
    p1, q1 = sorted(s1)  # Sort the first segment's indices
    p2, q2 = sorted(s2)  # Sort the second segment's indices

    # Check if segment 1 is strictly between the endpoints of segment 2
    if (p1 > p2 and p1 < q2) and (q1 < p2 or q1 > q2):
        return True  # Segments intersect in terms of vertex order

    if (p2 > p1 and p2 < q1) and (q2 < p1 or q2 > q1):
        return True  # Segments intersect in terms of vertex order

    return False  # No intersection

def plot_polygon_with_cuts(vertices: list, cuts: list, min_cut: list = None): 
    """
    Plot the polygon and the cuts. Highlight the minimum-area cut.
    
    Parameters:
    - vertices: A list of tuples representing the vertices of the polygon.
    - cuts: A list of tuples representing the cuts (pairs of vertex indices).
    - min_cut: A tuple representing the cut corresponding to the minimum area region.
    """
    # Create a matplotlib figure
    fig, ax = plt.subplots()

    # Convert vertices to a numpy array for easy indexing
    vertices = np.array(vertices)
    
    # Plot the polygon
    polygon_shape = Polygon(vertices, closed=True, edgecolor='black', fill=None, lw=2, label='Polygon')
    ax.add_patch(polygon_shape)

    # Plot the cuts
    for cut in cuts:
        p1, p2 = vertices[cut[0]], vertices[cut[1]]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b--', lw=2, label="Cut" if cut == cuts[0] else "")
    
    # Highlight the minimum-area cut
    if min_cut:
        region = np.array(min_cut)
        region_shape = Polygon(region, closed=True, edgecolor='red', fill=True, facecolor='salmon', lw=2, label='Min. Area')
        ax.add_patch(region_shape)

    # Plot the vertices
    ax.plot(vertices[:, 0], vertices[:, 1], 'go', label='Vertices')

    # Annotate vertices
    for i, (x, y) in enumerate(vertices):
        ax.text(x, y, f'  {i}', color="black", fontsize=12)

    # Set plot limits, labels, and legend
    ax.set_xlim(vertices[:, 0].min() - 1, vertices[:, 0].max() + 1)
    ax.set_ylim(vertices[:, 1].min() - 1, vertices[:, 1].max() + 1)
    ax.set_aspect('equal', 'box')
    plt.title('Polygon with Cuts (Min Area Highlighted)')
    plt.legend(loc='upper left')
    plt.grid(True)

    # Show the plot
    plt.show()