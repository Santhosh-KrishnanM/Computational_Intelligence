from collections import deque
import heapq

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def delete_node(self, node):
        if node in self.graph:
            del self.graph[node]
        else:
            print("\nNode does not exist.")
        for i in self.graph:
            if node in self.graph[i]:
                self.graph[i].remove(node)

    def add_edge(self, x, y, z):
        if x not in self.graph:
            self.add_node(x)
        if y not in self.graph:
            self.add_node(y)
        self.graph[x].append((y,z))
        self.graph[y].append((x,z))

    def delete_edge(self, x, y):
        if x in self.graph and y in self.graph[x]:
            self.graph[x].remove(y)	 
        if y in self.graph and x in self.graph[y]:
            self.graph[y].remove(x)

    def display_adjlist(self):
        adjlist = []
        for i in self.graph:
            adjlist.append(self.graph[i])
        return adjlist

    def bfs(self, start, goal):
       fringe = deque([start])
       visited = set([start])
       search_path = [start]
       print("\nBFS Search:")
       while fringe:
          print("Fringe:", list(fringe))
          current = fringe.popleft()
          print("Expanding:", current)
          if current in goal:
             return search_path
          for neighbor, _ in self.graph.get(current, []):
             if neighbor not in visited:
                visited.add(neighbor)
                search_path.append(neighbor)
                fringe.append(neighbor)
       return search_path

    def dfs(self, start, goal):
       fringe = [start]
       visited = set([start])
       path_tracker = {start: [start]}
       print("\nDFS Search:")
       while fringe:
          print("Fringe:", fringe)
          current = fringe.pop()
          print("Expanding:", current)
          if current in goal:
             return path_tracker[current]
          for neighbor, _ in reversed(self.graph.get(current, [])):
             if neighbor not in visited:   
                visited.add(neighbor)
                path_tracker[neighbor] = path_tracker[current] + [neighbor]
                fringe.append(neighbor)
       return None

#print(result)
    def ucs_search(self, start, goals):
       pq = [(0, start)]
       visited = set()
       parent = {start: None}
       cost = {start: 0}
       print("\nUCS Search:")
       while pq:
          print("Fringe:", pq)
          c, u = heapq.heappop(pq)
          if u in visited:
             continue
          print(f"Expanding: {u} (cost={c})")
          visited.add(u)
          if u in goals:
             path = []
             while u:
                path.append(u)
                u = parent[u]
             print("Path:", " -> ".join(reversed(path)))
             print("Cost:", c)
             return
          for v, w in self.graph[u]:
             nc = c + w
             if v not in cost or nc < cost[v]:
                cost[v] = nc
                parent[v] = u
                heapq.heappush(pq, (nc, v))
    

g = Graph()

n = int(input("Enter number of nodes: "))
print("Enter Nodes:")
for i in range(n):
    node = input()
    g.add_node(node)

e = int(input("Enter number of edges: "))
print("Enter Edges (x y z):")
for i in range(e):
    x, y, z = input().split()
    g.add_edge(x, y, int(z))

alist = g.display_adjlist()

print("\nAdjacency List:\n", alist)

while True:
    print("\n\t----Menu----")
    print("0.Exit")
    print("1.BFS")
    print("2.DFS")
    print("3.UCS")
    print("4.Add Node")
    print("5.Add Edge")
    print("6.Delete Node")
    print("7.Delete Edge")
    print("8.Adjacency List")
    ch = int(input("\nEnter choice: "))    
    if ch == 1:
       start = input("Enter start node: ")
       k = int(input("Enter no. of goal nodes: "))
       goals = set()
       print("Enter Goal nodes: ")
       for i in range(k):
          goals.add(input())
       g.bfs(start, goals)
    elif ch == 2:
       start = input("Enter start node: ")
       k = int(input("Enter no. of goal nodes: "))
       goals = set()
       print("Enter Goal nodes: ")
       for i in range(k):
          goals.add(input())
       g.dfs(start, goals)
    elif ch == 3:
       start = input("Enter start node: ")
       k = int(input("Enter no. of goal nodes: "))
       goals = set()
       print("Enter Goal nodes: ")
       for i in range(k):
          goals.add(input())
       g.ucs_search(start, goals)
    elif ch == 0:
       print("\nExit\n")
       break
    elif ch == 4:
       print("Enter the node to add: ")
       node = input()
       g.add_node(node)
    elif ch == 5:
       n1 = input("Enter node 1: ")
       n2 = input("Enter node 2: ")
       g.add_edge(n1,n2)
    elif ch == 6:
       node = input("Enter the node to delete: ")
       g.delete_node(node)
    elif ch == 7:
       n1 = input("Enter node 1: ")
       n2 = input("Enter node 2: ")
       g.delete_edge(n1, n2)
    elif ch == 8:
       alist = g.display_adjlist()
       print("\nAdjacency List:\n", alist)
    else:
       print("\nInvalid Choice.")
