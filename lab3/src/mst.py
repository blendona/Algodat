import sys


def make_sets(n):
    """
    Initialise n single sets.
    Nodes are 1-indexed (matching the problem input).
    size: number of nodes in the tree with one arbitrary root
    """
    #parent[i] = i means i is its own root
    parent = list(range(n + 1))

    #size[i] = 1 because each set starts with one element
    size = [1] * (n + 1)
    return parent, size


def find(v, parent):
    """
    Find the root of v's set. Uses path compression to flatten the tree for efficiency.
    Returns:
    root: the root of the set containing v.

    """
    root = v

    #loop over the path to find the root 
    while parent[root] != root:
        root = parent[root]

    #path compression
    while parent[v] != v:
        next_v = parent[v]
        parent[v] = root
        v = next_v

    return root


def union(u, v, parent, size):
    """
    Merge the sets containing u and v if they do not already belong to the same set.
    Uses union by size to keep trees shallow for efficiency.
    Returns:
    True if a union was performed.
    False if u and v already belong to the same set. 

    """
    root_u = find(u, parent)
    root_v = find(v, parent)

    #already in the same set
    if root_u == root_v:
        return False

    #union by size: attach smaller tree under larger tree
    if size[root_u] < size[root_v]:
        root_u, root_v = root_v, root_u

    parent[root_v] = root_u
    size[root_u] += size[root_v]

    return True


def kruskal(n, edges):
    """
    Kruskal's algorithm to find the weight of the minimum spanning tree.
    Sort edges by weight, then iterate through them, adding to the MST if they connect two different sets.
    
    Returns:
    total_weight: the total weight of the MST.
    
    """

    #sort the edges by weight
    edges.sort(key=lambda e: e[2])

    parent, size = make_sets(n)

    total_weight = 0
    edges_added = 0

    for u, v, w in edges:
        #add edge if it connects two different sets
        if union(u, v, parent, size):
            total_weight += w
            edges_added += 1

            #stop early if we have added n-1 edges (a spanning tree is complete)
            if edges_added == n - 1:
                break

    return total_weight


def main():
    data = sys.stdin.buffer

    n, m = map(int, data.readline().split())

    edges = []

    for _ in range(m):
        u, v, w = map(int, data.readline().split())
        edges.append((u, v, w))

    print(kruskal(n, edges))


if __name__ == "__main__":
    main()