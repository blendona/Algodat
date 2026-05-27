import sys
import math
import os

def euclidean_distance(p1, p2):
    """Standard Euclidean distance between points p1 and p2.
    
    Parameters:
        p1, p2: tuples of (x, y) coordinates.
    Returns: 
        The distance between p1 and p2.
    """
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)

def brute_force_closest(points):
    """
    Checks every pair.
    Called only when for small amout of points.

    Parameters: 
        points: list of (x, y) tuples.
    Returns:
        min_dist: the minimum distance among all pairs in the list.
    """
    min_dist = math.inf
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = euclidean_distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
    return min_dist


def check_strip(strip_sorted_by_y, delta):
    """
    Implements the combine step (combining left and right halves).
    For each point p we walk forward in y-order and check all points q
    as long as (q.y - p.y) < delta. The box argument guarantees at most
    a few such points exist, so the inner loop does O(1) work per point, 
    so total strip work is O(n).

    Parameters: 
        strip_sorted_by_y: points with |x - dividing_x| < delta, sorted by y.
        delta: best distance found so far (from left and right halves).
    Returns:
        min_dist: the minimum distance among pairs in the strip, which may be better than delta.
    """
    min_dist = delta
    n = len(strip_sorted_by_y)

    for i in range(n):
        p = strip_sorted_by_y[i]        
        j = i + 1  #check points above p 

        # Walk forward while y-gap < current best distance
        # unnecessary checks are done for same side pairs, but harmless since the distance is larger than delta
        while j < n and (strip_sorted_by_y[j][1] - p[1]) < min_dist:
            dist = euclidean_distance(p, strip_sorted_by_y[j])
            if dist < min_dist:
                min_dist = dist
            j += 1

    return min_dist


def closest_pair_rec(px, py):
    """
    Recursive divide-and-conquer for closest pair. O(nlogn) time. 

    Parameters:
        px : points sorted by x
        py : the same points sorted by y 

    Returns:
        The minimum distance among all pairs in this subproblem.
    """
    n = len(px)

    # base case: brute force when small enough. O(1) time per call since n <= 3.
    if n <= 3:
        return brute_force_closest(px)

    mid = n // 2
    dividing_x = px[mid - 1][0]   # the dividing line

    # split points into left and right halves with px, O(n) time.
    left_half_px = px[:mid]
    right_half_px = px[mid:]

    # create a set for the left half points and check membership for each point in py (O(1)). 
    # not checking with points itself due to potential duplicates
    left_ids = {id(p) for p in left_half_px}
    left_half_py = [p for p in py if id(p) in left_ids]
    right_half_py = [p for p in py if not id(p) in left_ids]

    delta_left = closest_pair_rec(left_half_px,  left_half_py)
    delta_right = closest_pair_rec(right_half_px, right_half_py)

    delta = min(delta_left, delta_right)

    #since py is already sorted, building the strip takes O(n) time.
    strip = [p for p in py if abs(p[0] - dividing_x) < delta]

    delta_cross = check_strip(strip, delta)

    return min(delta, delta_cross)


def closest_pair(points):
    """
    Solve Closest Pair for a list of points. O(nlogn) time.
    
    Parameters: 
        points: list of (x, y) tuples.
    Returns:
        The minimum Euclidean distance.
    """
    if len(points) < 2:
        raise ValueError("Need at least 2 points.")

    # pre-sort once at the top level,  O(nlogn) time.
    px = sorted(points, key=lambda p: (p[0], p[1]))  # sorted by x, y as tiebreak
    py = sorted(points, key=lambda p: (p[1], p[0]))  # sorted by y, x as tiebreak

    return closest_pair_rec(px, py)


def main():
    data = sys.stdin.buffer.read().split()
    idx  = 0
    n = int(data[idx]); idx += 1
    points = []
    for _ in range(n):
        x = int(data[idx]); idx += 1
        y = int(data[idx]); idx += 1
        points.append((x, y))

    print(f"{closest_pair(points):.6f}")


if __name__ == "__main__":
    main()
