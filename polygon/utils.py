import math
from typing import List, Tuple

def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def cross_product(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Calculate the cross product of two vectors."""
    return a[0]*b[1] - a[1]*b[0]

def orientation(p: Tuple[float, float], q: Tuple[float, float], r: Tuple[float, float]) -> int:
    """Determine the orientation of three points."""
    val = cross_product((q[0]-p[0], q[1]-p[1]), (r[0]-p[0], r[1]-p[1]))
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0
