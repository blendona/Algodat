import pandas as pd
import networkx as nx
import os



# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# with open(os.path.join(base_dir, 'data/sample/1.in')) as f:
#     lines = f.readlines()

# first_line = lines[0].split()
# num_words = int(first_line[0])
# num_pairs = int(first_line[1])

# # Read the words (nodes)
# words = [lines[i+1].strip() for i in range(num_words)]

# # Read the pairs (edges)
# pairs = []
# for i in range(num_pairs):
#     pair = lines[num_words + 1 + i].strip().split()
#     pairs.append(pair)


import sys

lines = sys.stdin.readlines()

first_line = lines[0].split()
num_words = int(first_line[0])
num_pairs = int(first_line[1])

words = [lines[i+1].strip() for i in range(num_words)]
pairs = [lines[num_words + 1 + i].strip().split() for i in range(num_pairs)]


def BFS(graph, start, goal):
    if(start == goal):
        print(0)
        return
    visited = {word: 0 for word in words}
    queue = [(start, 0)]
    visited[start] = 1
    while queue:
        vertex, length = queue.pop(0)
        for w in graph[vertex]:
            if visited[w] == 0:
                visited[w] = length + 1
                queue.append((w, length + 1))
                if w == goal:
                    #print("Found goal:", w, "Visited:", visited, "Start:", start)
                    print(length + 1)
                    return
    print("Impossible")
    return 

def isNeighbours(A, B):
    listA = list(A)[1:]
    listB = list(B)
    for x in listA:
        if x in listB:
            listB.remove(x) 
        else:
            return False
    return True

def allNeighbours(A):
    neighbours = []
    for i in range(len(words)):
        if isNeighbours(A, words[i]):
            if (A != words[i]):
                neighbours.append(words[i])
    return neighbours

def createGraph():
    graph = {}
    for i in range(len(words)):
        graph[words[i]] = allNeighbours(words[i])
    return graph

def main():
    graph = createGraph()
    for pair in pairs:
        BFS(graph, pair[0], pair[1])    


if __name__ == "__main__":
    main()


