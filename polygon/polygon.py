from pydantic import List, Tuple

class Polygon:
    def __init__(self, vertices: List[Tuple[float, float]]):
        self.vertices = vertices

    def area(self) -> float:
        """Calculate the area of the polygon using Shoelace formula."""
        n = len(self.vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i][0] * self.vertices[j][1]
            area -= self.vertices[j][0] * self.vertices[i][1]
        return abs(area) / 2.0

    def centroid(self) -> Tuple[float, float]:
        """Calculate the centroid of the polygon."""
        n = len(self.vertices)
        cx = cy = 0.0
        for i in range(n):
            j = (i + 1) % n
            cx += self.vertices[i][0] * self.vertices[j][1]
            cy += self.vertices[i][1] * self.vertices[j][0]
        return ((cx / (3 * n)), (cy / (3 * n)))

    def contains(self, point: Tuple[float, float]) -> bool:
        """Check if a point lies inside the polygon."""
        n = len(self.vertices)
        inside = False
        ptype = 0
        for i in range(n+1):
            j = (i + 1) % (n + 1)
            if self.orientation(point, self.vertices[i], self.vertices[j]) > 0:
                if ptype >= 2 and self.orientation(point, self.vertices[i], self.vertices[j]) <= 0:
                    return False
                ptype = 1
            elif self.orientation(point, self.vertices[i], self.vertices[j]) < 0:
                if ptype <= 1 and self.orientation(point, self.vertices[i], self.vertices[j]) >= 0:
                    return False
                ptype = 2
        return True


class Cut:
    def __init__(self, vertex1: int, vertex2: int):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def intersects(self, cut: 'Cut') -> bool:
        """Check if two cuts intersect."""
        return self.vertex1 == cut.vertex1 or self.vertex1 == cut.vertex2 or \
               self.vertex2 == cut.vertex1 or self.vertex2 == cut.vertex2

    def area(self, polygon: Polygon) -> float:
        """Calculate the area of the triangle formed by the cut."""
        return polygon.area()
