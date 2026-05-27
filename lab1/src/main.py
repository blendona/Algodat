import sys


# # This code is for reading the input from a file. 
# # I have commented it out when we run the script since the script seemd to crash when we read in the files this way

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# with open(os.path.join(base_dir, 'data/sample/1.in')) as f:
#     lines = f.readlines()

# first_line = lines[0].split()
# num_words = int(first_line[0])
# num_pairs = int(first_line[1])

# # Read the words (nodes)
# words = [lines[i+1].strip() for i in range(num_words)]

# # Read the pairs that we want to find the shortest path between (start and goal)
# pairs = []
# for i in range(num_pairs):
#     pair = lines[num_words + 1 + i].strip().split()
#     pairs.append(pair)


# This code is used to read in the files when we run the script. 
# We can run the script with the command "./check_solution.sh python3 src/main.py in the terminal.
lines = sys.stdin.readlines()

first_line = lines[0].split()
num_words = int(first_line[0])
num_pairs = int(first_line[1])

# Read the words (nodes)
words = [lines[i+1].strip() for i in range(num_words)]

# Read the pairs that we want to find the shortest path between (start and goal)
pairs = [lines[num_words + 1 + i].strip().split() for i in range(num_pairs)]

# The BFS function that we will use to find the shortest path between the start and goal nodes.
# 1: If the start and goal are the same, we can return 0 since we are already at the goal.
# 2: We use a queue to keep track of the nodes we need to visit and a visited dictionary to keep track of the nodes we have already visited and their distance from the start node.
# 3: We loop until the queue is empty, and for each node we visit, we check its neighbors. If a neighbor has not been visited, we add it to the queue and mark it as visited with the distance from the start node. If we reach the goal node, we can return the distance. If we exhaust the queue without finding the goal node, we can return "Impossible".
def BFS(graph, start, goal):
    # 1
    if(start == goal):
        print(0)
        return
    # 2
    visited = {word: 0 for word in words}
    queue = [(start, 0)]
    visited[start] = 1
    # 3
    while queue:
        vertex, length = queue.pop(0)
        for w in graph[vertex]:
            if visited[w] == 0:
                visited[w] = 1
                queue.append((w, length + 1))
                if w == goal:
                    print(length + 1)
                    return
    print("Impossible")
    return 

# We check if two words are neigbours
def isNeighbours(A, B):
    listA = list(A)[1:]
    listB = list(B)
    for x in listA:
        if x in listB:
            listB.remove(x) 
        else:
            return False
    return True

# We create a list of all the neighbours for a give word A
def allNeighbours(A):
    neighbours = []
    for i in range(len(words)):
        if isNeighbours(A, words[i]):
            if (A != words[i]):
                neighbours.append(words[i])
    return neighbours

# We create a graph where the keys are the words and the values are lists of their neighbours.
def createGraph():
    graph = {}
    for i in range(len(words)): 
        graph[words[i]] = allNeighbours(words[i])
    return graph

# We create the graph and then we call the BFS function for each pair of start and goal nodes to find the shortest path between them.
def main():
    graph = createGraph()
    for pair in pairs:
        BFS(graph, pair[0], pair[1])    

# We call the main function to run the script.
if __name__ == "__main__":
    main()


