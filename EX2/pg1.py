import heapq

class Graph:
    def __init__(self):
        self.graph = {}
        self.heuristic = {}

    def add_node(self, node, h):
        if node not in self.graph:
            self.graph[node] = []
        self.heuristic[node] = h

    def add_edge(self, x, y, cost):
        if x not in self.graph:
            self.graph[x] = []
        if y not in self.graph:
            self.graph[y] = []
        self.graph[x].append((y, cost))
        self.graph[y].append((x, cost))

    def display_adjlist(self):
        print("\nAdjacency List:")
        for node in self.graph:
            print(node, "->", self.graph[node])

    def display_heuristic(self):
        print("\nHeuristic Values:")
        for node, h in self.heuristic.items():
            print(node, ":", h)

    def delete_node(self, node):
        if node in self.graph:
            del self.graph[node]
        else:
            print("Node does not exist.")
        for n in self.graph:
            self.graph[n] = [(neigh, c) for neigh, c in self.graph[n] if neigh != node]
        if node in self.heuristic:
            del self.heuristic[node]

    def delete_edge(self, x, y):
        if x in self.graph:
            self.graph[x] = [(neigh, c) for neigh, c in self.graph[x] if neigh != y]
        if y in self.graph:
            self.graph[y] = [(neigh, c) for neigh, c in self.graph[y] if neigh != x]

    def astar(self, start, goals):
        visited = set()
        pq = []
        parent = {}
        g_cost = {start: 0}

        heapq.heappush(pq, (self.heuristic[start], 0, start))
        print("\n\tA* Search Algorithm:")

        while pq:
            print("\nFringe:", [(f, n) for f, _, n in pq])
            f, g, current = heapq.heappop(pq)
            print(f"Expanding: {current}  g={g}, h={self.heuristic[current]}, f={f}")

            if current in goals:
                print("\nGoal Reached!")                
                path = []
                node = current
                while node is not None:
                    path.append(node)
                    node = parent.get(node, None)
                path.reverse()
                print("Path:", " -> ".join(path))
                print("Total Cost:", g)
                return

            if current in visited:
                continue
            visited.add(current)

            for neighbor, cost in self.graph[current]:
                if neighbor in visited:
                    continue
                new_g = g + cost
                if neighbor not in g_cost or new_g < g_cost[neighbor]:
                    g_cost[neighbor] = new_g
                    new_f = new_g + self.heuristic.get(neighbor, 0)
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_f, new_g, neighbor))

        print("\nNo solution found.")

g = Graph()
n = int(input("Enter number of nodes: "))
print("Enter Nodes with Heuristic (node h):")
for _ in range(n):
    node, h = input().split()
    g.add_node(node, int(h))

e = int(input("Enter number of edges: "))
print("Enter Edges (x y cost):")
for _ in range(e):
    x, y, cost = input().split()
    g.add_edge(x, y, int(cost))
g.display_adjlist()
g.display_heuristic()

while True:
    print("\n\t  Menu\n")
    print("0. Exit")
    print("1. A* Search")
    print("2. Add Node")
    print("3. Add Edge")
    print("4. Add/Update Heuristic value")
    print("5. Delete Node")
    print("6. Delete Edge")
    print("7. Display adjacency list")
    print("8. Display heuristic values")
    ch = int(input("\nEnter choice (0-8): "))
    if ch == 0:
        print("Exiting...")
        break
    elif ch == 1:
        start = input("Enter Start node: ")
        k = int(input("Enter number of goal nodes: "))
        print("Enter Goal nodes:")
        goals = set(input() for _ in range(k))
        g.astar(start, goals)
    elif ch == 2:
        node, h = input("Enter the node and heuristic value: ").split()
        g.add_node(node, int(h))
    elif ch == 3:
        n1 = input("Enter node 1: ")
        n2 = input("Enter node 2: ")
        cost = int(input(f"Enter edge cost between {n1} and {n2}: "))
        g.add_edge(n1, n2, cost)
    elif ch == 4:
        node = input("Enter node to add/update heuristic: ")
        h = int(input("Enter heuristic value: "))
        g.heuristic[node] = h
    elif ch == 5:
        node = input("Enter node to delete: ")
        g.delete_node(node)
    elif ch == 6:
        n1 = input("Enter node 1: ")
        n2 = input("Enter node 2: ")
        g.delete_edge(n1, n2)
    elif ch == 7:
        g.display_adjlist()
    elif ch == 8:
        g.display_heuristic()
    else:
        print("Invalid Choice.")
