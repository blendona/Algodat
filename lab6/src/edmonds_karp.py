import sys
from collections import deque


def add_edge(graph, u, v, capacity):
    """
    Add a directed residual edge u -> v.

    Parameters:
        graph: adjacency list of the flow network
        u: from node    
        v: to node
        capacity: initial capacity of the edge
    
    graph[u] contains edges of the form:
        [to, reverse_index, capacity]
    The reverse edge starts with capacity 0.
    """
    forward = [v, len(graph[v]), capacity]  # edge from u to v, reverse index is len(graph[v]) since we will append the reverse edge to graph[v]
    backward = [u, len(graph[u]), 0]        # reverse edge from v to u, reverse index is len(graph[u]) since we will append the forward edge to graph[u]

    graph[u].append(forward)
    graph[v].append(backward)


def bfs_find_path(graph, source, sink):
    """
    Finds an augmenting path from source to sink using Breadth First Search (BFS).
    
    Parameters:
        graph: adjacency list of the flow network
        source: starting node
        sink: target node   
    Returns:
        parent: an array where parent[v] = (previous_node, edge_index) 
            tells us how we reached v
        bottleneck: the minimum residual capacity along the path found. 
            If no path exists, bottleneck = 0.
    """
    n = len(graph)
    parent = [None] * n
    parent[source] = (-1, -1)       # source has no parent

    queue = deque()
    queue.append((source, 10**30))  # at source possible flow is infinite

    while queue:
        u, flow_so_far = queue.popleft()

        for edge_index, edge in enumerate(graph[u]):
            v, reverse_index, capacity = edge

            # if we can push flow through this edge and v is not visited yet.
            if capacity > 0 and parent[v] is None:
                parent[v] = (u, edge_index)
                new_flow = min(flow_so_far, capacity)

                if v == sink:       # augmenting path found, return immediately with bottleneck flow
                    return parent, new_flow

                queue.append((v, new_flow))

    return parent, 0


def max_flow(graph, source, sink, limit=None):
    """
    Ford-Fulkerson using BFS to find augmenting paths.
    If limit is given, we stop early once flow >= limit.
    This is useful when we only need to check if max-flow is at least C.

    Parameters:
        graph: adjacency list of the flow network
        source: starting node
        sink: target node
        limit: if not None, stop once flow >= limit
    Returns: 
        flow: total flow from source to sink
    """
    flow = 0

    while True:
        parent, bottleneck = bfs_find_path(graph, source, sink)

        if bottleneck == 0:
            break       # no more augmenting paths, max flow reached

        flow += bottleneck

        # walk backwards from sink to source and update residual capacities
        v = sink

        while v != source:
            u, edge_index = parent[v]
            edge = graph[u][edge_index]

            reverse_index = edge[1]

            # decrease forward residual capacity
            edge[2] -= bottleneck

            # increase backward residual capacity
            graph[v][reverse_index][2] += bottleneck

            v = u

        if limit is not None and flow >= limit:     # saves time during binary search when we only care if flow >= C
            return flow

    return flow


def build_graph(n, routes, removal_time, removed_count):
    """
    Build the flow network after removing the first removed_count routes.
    A route is kept if its removal time is greater than removed_count.

    Parameters:
        n: number of nodes
        routes: list of (u, v, capacity) for each route
        removal_time: list where removal_time[i] is the step at which route i is removed
        removed_count: how many routes have been removed so far
    Returns:
        graph: adjacency list of the flow network
    """
    graph = [[] for _ in range(n)]

    for index, (u, v, capacity) in enumerate(routes):
        if removal_time[index] > removed_count:     # condition for keeping the route
            # the graph is undirected, we model it as two directed edges
            add_edge(graph, u, v, capacity)
            add_edge(graph, v, u, capacity)

    return graph


def compute_flow(n, routes, removal_time, removed_count, required_flow=None):
    """
    Build the flow network after removing removed_count routes, then compute the max flow.
    Parameters:
        n: number of nodes
        routes: list of (u, v, capacity) for each route
        removal_time: list where removal_time[i] is the step at which route i is removed
        removed_count: how many routes have been removed so far
        required_flow: if not None, we can stop early once flow >= required_flow
    Returns: 
        flow: the max flow from source to sink after removing removed_count routes 
    """
    source = 0
    sink = n - 1

    graph = build_graph(n, routes, removal_time, removed_count)
    return max_flow(graph, source, sink, required_flow)


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0

    n = int(data[pos])
    pos += 1

    m = int(data[pos])
    pos += 1

    required_flow = int(data[pos])
    pos += 1

    p = int(data[pos])
    pos += 1

    routes = []

    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        capacity = int(data[pos + 2])
        pos += 3

        routes.append((u, v, capacity))

    plan = []

    for _ in range(p):
        route_index = int(data[pos])
        pos += 1
        plan.append(route_index)

    # removal_time[i] tells us at which step route i is removed
    # if route i is never removed, it gets p + 1, (initally all routes)
    removal_time = [p + 1] * m

    for step, route_index in enumerate(plan, start=1): # the removal order given by the plan
        removal_time[route_index] = step

    # binary search the maximum number of routes we can remove
    # efficient way to find the max amount of routes we can remove while still maintaining required_flow.
    # without having to compute the flow for every possible number of removed routes.
    low = 0
    high = p

    while low < high:
        mid = (low + high + 1) // 2

        # after removing mid routes, can we still achieve at least required_flow?
        flow = compute_flow(
            n,
            routes,
            removal_time,
            mid,
            required_flow
        )

        if flow >= required_flow:
            low = mid
        else:
            high = mid - 1


    removed_routes = low

    # Now compute the actual final max-flow
    final_flow = compute_flow(
        n,
        routes,
        removal_time,
        removed_routes,
        None
    )

    print(removed_routes, final_flow)


if __name__ == "__main__":
    main()