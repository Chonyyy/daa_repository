import sys
from pydantic import BaseModel
from typing import List, Tuple
from itertools import combinations
from utils import generate_convex_polygon, generate_possible_cuts, calculate_smallest_region_area, segments_intersect, plot_polygon_with_cuts, all_subareas

FIXED_CASES = [
    ([(0.6946583704589973, 0.7193398003386511), (0.6819983600624985, 0.7313537016191705), (0.40673664307579976, -0.9135454576426011), (0.6156614753256585, -0.7880107536067218), (0.6946583704589973, -0.7193398003386512)], 2),
    ([(0.898794046299167, 0.4383711467890774), (-0.22495105434386503, 0.9743700647852352), (-0.9563047559630354, -0.29237170472273677), (-0.46947156278589075, -0.882947592858927), (-0.3907311284892738, -0.9205048534524403)], 3),
    ([(-0.981627183447664, -0.19080899537654472), (-0.8829475928589269, -0.46947156278589086), (-0.2923717047227371, -0.9563047559630353), (0.559192903470747, -0.8290375725550416), (0.6156614753256585, -0.7880107536067218), (0.8290375725550418, -0.5591929034707466), (0.9335804264972015, -0.35836794954530077), (0.9659258262890683, -0.2588190451025207)], 4),
]


# Define input case structure
class InputCase(BaseModel):
    n: int  # Number of vertices
    k: int  # Number of cuts

def cuts_do_not_intersect(cuts: List[Tuple[int, int]], polygon: List[Tuple[int, int]]) -> bool:
    """
    This function checks if any of the cuts intersect at a point other than the polygon's vertices.
    """
    def do_intersect(cut1, cut2):
        # Check if two cuts (segments) intersect at any point other than the polygon vertices
        # cut1 and cut2 are tuples of vertex indices (e.g., (i, j) where i and j are vertices in the polygon)
        return segments_intersect(cut1, cut2)

    # Check for pairwise intersections between the selected cuts
    for cut1, cut2 in combinations(cuts, 2):
        if do_intersect(cut1, cut2):
            return False
    return True

def brute_force_solution(polygon: List[Tuple[int, int]], cuts: List[Tuple[int, int]], k: int) -> float:
    from itertools import combinations
    max_min_area = 0
    max_minimal_region = []
    solution_cuts = []
    for selected_cuts in combinations(cuts, k):
        # Check if the selected cuts are valid (i.e., they do not intersect except at vertices)
        if cuts_do_not_intersect(selected_cuts, polygon):
            # plot_polygon_with_cuts(polygon, selected_cuts)
            min_area, minimal_region = calculate_smallest_region_area(polygon, selected_cuts)
            if min_area > max_min_area:
                # plot_polygon_with_cuts(polygon, selected_cuts)
                print(selected_cuts)
                max_min_area = min_area
                max_minimal_region = minimal_region
                solution_cuts = selected_cuts
    return max_min_area, solution_cuts, max_minimal_region

def calculate_all_possible_areas(polygon: List[Tuple[int, int]], possible_cuts: List[Tuple[int, int]], k: int) -> List[float]:
    areas = set()
    for selected_cuts in combinations(possible_cuts, k):
        new_areas = all_subareas(polygon, selected_cuts)
        areas = sorted(set.union(set(areas), set(new_areas)))
    return areas

def find_area(x1, y1, x2, y2, x3, y3):
    return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

def cuts_for_area(N, X, Y, M):
    best = [[0] * N for _ in range(N)]
    cuts = [[0] * N for _ in range(N)]
    
    for length in range(2, N + 1):
        for i in range(N - length + 1):
            j = i + length - 1
            for k in range(i + 1, j + 1):
                area = find_area(X[i], Y[i], X[k], Y[k], X[j], Y[j])
                total_area = best[i][k] + best[k][j] + area
                total_cuts = cuts[i][k] + cuts[k][j]
                
                if total_area >= M:
                    total_cuts += 1
                    total_area = 0
                
                if cuts[i][j] < total_cuts or (cuts[i][j] == total_cuts and best[i][j] < total_area):
                    cuts[i][j] = total_cuts
                    best[i][j] = total_area
    
    return cuts[0][N - 1] - 1

def solution(polygon: List[Tuple[int, int]], possible_cuts: List[Tuple[int, int]], k: int) -> float:
    possible_areas = calculate_all_possible_areas(polygon, possible_cuts, k)

    N = len(polygon)
    X ,Y = zip(*polygon)
    
    low, high = 0, len(possible_areas) - 1 
    
    while low + 1 < high:
        mid = int((low + high) // 2)
        current_area = possible_areas[mid]  # Get the mid area value
        
        # Check if we can make `k` cuts such that the minimum area is >= current_area
        if cuts_for_area(N, X, Y, current_area) >= k:
            low = mid  # Move search to the right half
        else:
            high = mid  # Move search to the left half

    return possible_areas[low]  # Return the maximum possible smallest area
    # print(low)

def solve_input_case(input_case: InputCase) -> float:
    polygon = generate_convex_polygon(input_case.n)
    plot_polygon_with_cuts(polygon, [])
    cuts = generate_possible_cuts(input_case.n)
    solution_area = solution(polygon, cuts, k)
    print(solution_area)
    return solution_area

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <n> <k>")
        sys.exit(1)

    n = int(sys.argv[1])
    k = int(sys.argv[2])
    result = solve_input_case(InputCase(n=n, k=k))
    # print("Result:", result)
