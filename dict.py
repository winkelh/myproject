graph = {
    "A": {"B": 3, "C": 3},
    "B": {"A": 3, "D": 3.5, "E": 2.8},
    "C": {"A": 3, "E": 2.8, "F": 3.5},
    "D": {"B": 3.5, "E": 3.1, "G": 10},
    "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
    "F": {"G": 2.5, "C": 3.5},
    "G": {"F": 2.5, "E": 7, "D": 10},
}

nodes =  {node: {"visited": False, "distance": float("inf")} for node in graph}

print(nodes)

visited = set()
visited.add("A")
visited.add("B")
visited.add("C")
visited.add("A")
print(visited)

list = [1, 2, 3, 4, 5, 6, 7, 8, 11, 10]
while list:
    i = list.pop()
    print(i)

