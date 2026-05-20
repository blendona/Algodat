"""
Lab 6: Railway Planning
=======================
Problem:
  - We have a railway network (undirected graph) with N nodes and M edges.
  - We must keep the max flow from node 0 (Minsk) to node N-1 (Lund) >= C.
  - We are given P edges to remove, in order. Remove each edge if the
    resulting max flow is still >= C. Stop as soon as we cannot remove.
  - Output: how many edges we removed, and the final max flow.

Algorithm: Edmonds-Karp (Ford-Fulkerson with BFS path finding)
  - This is the version from Lecture 7: find augmenting paths using BFS.
  - Time complexity: O(V * E^2), but since capacities are small (<=100)
    and we may rerun after each removal, we keep it simple and correct.

Key ideas from the lecture slides:
  - Residual graph: for each edge (u,v) with capacity c and flow f,
      forward edge (u,v) has residual capacity c - f  (room to increase)
      backward edge (v,u) has residual capacity f      (room to decrease)
  - Augmenting path: any path s->t in the residual graph
  - Ford-Fulkerson: keep finding augmenting paths until none exist
  - When no augmenting path exists: we have maximum flow (max-flow min-cut theorem)

Since the graph is UNDIRECTED, edge (u,v,cap) means flow can go
either direction, but total flow on the edge <= cap.
We model this by giving each undirected edge two directed residual slots.
"""

from collections import deque


# ---------------------------------------------------------------------------
# Residual graph representation
# ---------------------------------------------------------------------------
# We use an adjacency list of edges stored in a flat list.
# Each edge is stored as [to, capacity, reverse_edge_index].
# For each undirected edge (u, v, cap) we add:
#   graph[u] -> [v, cap, ...]   (forward)
#   graph[v] -> [u, cap, ...]   (forward the other way, same cap since undirected)
#   Both point to each other as their "reverse" edge.
#
# This naturally handles the undirected case: the "backward" edge for u->v
# is the v->u entry, and they share their remaining capacity symmetrically.

class MaxFlow:
    """
    Edmonds-Karp maximum flow (Ford-Fulkerson + BFS).
    
    Lecture 7 recap:
      - Build residual graph Gf
      - While there is an s-t path in Gf (found by BFS):
          find the bottleneck delta (min residual cap on path)
          push delta units along the path (update forward and backward edges)
      - Return total flow pushed
    """

    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]  # adjacency list

    def add_edge(self, u, v, cap):
        """
        Add an undirected edge (u, v) with capacity cap.
        Returns the index into graph[u] where the forward edge was appended,
        so we can later 'remove' the edge by zeroing its capacity.
        """
        # Forward: u -> v (capacity cap)
        forward_idx = len(self.graph[u])
        # Backward: v -> u (capacity cap, since undirected)
        backward_idx = len(self.graph[v])

        # Each entry: [neighbor, remaining_capacity, index_of_reverse_in_neighbor_list]
        self.graph[u].append([v, cap, backward_idx])
        self.graph[v].append([u, cap, forward_idx])

        return forward_idx  # caller stores this to locate the edge later

    def _bfs(self, s, t):
        """
        BFS on the residual graph to find a path from s to t.
        Returns (parent_node, parent_edge_idx) arrays if path found, else None.
        parent_edge_idx[v] = index in graph[parent[v]] of the edge used to reach v
        """
        visited = [-1] * self.n          # visited[v] = parent of v (-1 = unvisited)
        parent_edge = [-1] * self.n      # which edge index led to v
        visited[s] = s
        queue = deque([s])

        while queue:
            u = queue.popleft()
            if u == t:
                break
            for idx, (v, cap, _) in enumerate(self.graph[u]):
                if cap > 0 and visited[v] == -1:   # residual capacity > 0
                    visited[v] = u
                    parent_edge[v] = idx
                    queue.append(v)

        if visited[t] == -1:
            return None, None   # no path found -> max flow reached
        return visited, parent_edge

    def max_flow(self, s, t):
        """
        Run Edmonds-Karp and return the maximum flow from s to t.
        MODIFIES the residual capacities in self.graph.
        """
        total_flow = 0

        while True:
            parent, parent_edge = self._bfs(s, t)
            if parent is None:
                break  # no augmenting path -> done

            # Find the bottleneck (delta = min residual capacity along path)
            delta = float('inf')
            v = t
            while v != s:
                u = parent[v]
                edge_idx = parent_edge[v]
                delta = min(delta, self.graph[u][edge_idx][1])
                v = u

            # Update residual capacities along the path
            # forward edge: decrease remaining capacity by delta
            # backward edge: increase remaining capacity by delta (allows "undo")
            v = t
            while v != s:
                u = parent[v]
                edge_idx = parent_edge[v]
                rev_idx = self.graph[u][edge_idx][2]

                self.graph[u][edge_idx][1] -= delta   # forward: less room
                self.graph[v][rev_idx][1] += delta    # backward: more room

                v = u

            total_flow += delta

        return total_flow


# ---------------------------------------------------------------------------
# Build a fresh MaxFlow graph from the current set of active edges
# ---------------------------------------------------------------------------
def build_and_solve(n, edges, removed_set, s, t):
    """
    Build a new MaxFlow instance with all edges except those in removed_set,
    then return the max flow.
    
    edges: list of (u, v, cap) indexed 0..M-1
    removed_set: set of edge indices that have been removed
    """
    mf = MaxFlow(n)
    for i, (u, v, cap) in enumerate(edges):
        if i not in removed_set:
            mf.add_edge(u, v, cap)
    return mf.max_flow(s, t)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def solve():
    import sys
    data = sys.stdin.read().split()
    idx = 0

    N = int(data[idx]); idx += 1   # number of nodes
    M = int(data[idx]); idx += 1   # number of edges
    C = int(data[idx]); idx += 1   # required minimum flow
    P = int(data[idx]); idx += 1   # number of planned removals

    edges = []
    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        c = int(data[idx]); idx += 1
        edges.append((u, v, c))

    plan = []
    for _ in range(P):
        plan.append(int(data[idx])); idx += 1

    source = 0
    sink   = N - 1

    # We try removing edges one by one and recompute max flow each time.
    # This is O(P * V * E^2) which is fine given the problem constraints.
    removed = set()
    num_removed = 0

    for edge_idx in plan:
        # Tentatively remove this edge
        removed.add(edge_idx)
        flow = build_and_solve(N, edges, removed, source, sink)

        if flow >= C:
            # Safe to remove — keep it gone
            num_removed += 1
        else:
            # Cannot remove this edge — put it back and stop
            removed.discard(edge_idx)
            break

    # Compute the final max flow with all successfully removed edges gone
    final_flow = build_and_solve(N, edges, removed, source, sink)

    print(num_removed, final_flow)


if __name__ == "__main__":
    solve()