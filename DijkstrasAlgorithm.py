from typing import Dict
from typing import KeysView
from collections import deque

class Graph:
    NOT_APPLICABLE = 'n/a' 

    def __init__(self, graph: Dict = None) -> None:
        self.graph = graph if graph is not None else {}

    def add_node(self, name: str) -> None:
        self.graph[name] = {"neighbors": {}}

    def add_edge(self, start_node: str, end_node: str, weigth: int) -> None:
        edge_id = start_node + "_" + end_node
        self.graph[start_node]["neighbors"][end_node] = weigth
        self.graph[end_node]["neighbors"][start_node] = weigth
        
    def add_node_set(self, data: Dict) -> None:
        self.graph.update(data)

    def get_nodes(self) -> KeysView:
        return self.graph.keys()
        
    def get_graph(self) -> Dict:
        return self.graph

    def find_nearest_node(self, nodes: Dict) -> str:
        nearest_node = Graph.NOT_APPLICABLE
        smallest_known_distance = float('inf')
        
        for node in nodes.keys():
            if not nodes[node]['visited']:
                if nodes[node]['distance_to_start'] < smallest_known_distance:
                    nearest_node            = node
                    smallest_known_distance = nodes[node]['distance_to_start']
                
        return nearest_node
        
    def process_route(self, start_node: str, end_node: str) -> Dict:
        nodes = {}
        previous_node = ""
        
        # initialize the nodes with distance_to_start and visited status
        for node in self.graph.keys():
            nodes[node] = {
                "distance_to_start": float('inf'),
                "visited": False,
                "previous_node": "",
                
            }
        nodes[start_node]["distance_to_start"] = 0

        # Walk through the nodes, start with the start node and walk through its unvisited neighbors.
        current_node = start_node
        while current_node != Graph.NOT_APPLICABLE:
            current_node_distance_to_start = nodes[current_node]["distance_to_start"]
            for neighbor in self.graph[current_node]["neighbors"]:
                edge_weight = self.graph[current_node]["neighbors"][neighbor]
                if current_node_distance_to_start + edge_weight < nodes[neighbor]["distance_to_start"]: 
                    nodes[neighbor]["distance_to_start"] = current_node_distance_to_start + edge_weight
                    nodes[neighbor]["previous_node"]     = current_node

            nodes[current_node]["visited"] = True

            # Now initialize the next current node
            current_node = self.find_nearest_node(nodes)

        return nodes
        
    def find_shortest_route(self, start_node: str, end_node: str) -> int:
        nodes = self.process_route(start_node, end_node)
        shortest_route = nodes[end_node]["distance_to_start"]
        return shortest_route

    def find_route(self, nodes: {}, end_node: str) -> []:
        route = deque([end_node])
        previous_node = nodes[end_node]["previous_node"]
        while previous_node:
            route.appendleft(previous_node)
            previous_node = nodes[previous_node]["previous_node"]
        return route

"""

ed = Graph()
ed.add_node("A")
ed.add_node("B")
ed.add_node("C")
ed.add_node("D")
ed.add_node("E")
ed.add_node("F")
ed.add_node("G")
ed.add_node("H")
ed.add_node("I")
ed.add_node("J")
ed.add_node("K")
ed.add_node("L")
print(f"List of the nodes: {ed.get_nodes()}")

ed.add_edge("A", "B", 10)
ed.add_edge("A", "C", 15)
ed.add_edge("B", "C", 18)
ed.add_edge("B", "D", 12)
ed.add_edge("C", "D", 13)
ed.add_edge("B", "E",  5)
ed.add_edge("B", "E",  5)
ed.add_edge("D", "I", 13)
ed.add_edge("E", "F",  8)
ed.add_edge("F", "D",  7)
ed.add_edge("F", "G", 11)
ed.add_edge("F", "H", 12)
ed.add_edge("G", "H",  6)
ed.add_edge("G", "J", 25)
ed.add_edge("H", "D", 17)
ed.add_edge("H", "I",  7)
ed.add_edge("H", "K", 21)
ed.add_edge("I", "L", 23)
ed.add_edge("J", "K", 11)
ed.add_edge("K", "L", 10)
print(f"Dump of the edges: {ed.get_graph()}")


#print(f"Graph: {ed.get_graph()}")
#print(f"Nodes: {ed.get_nodes()}")

start_node = "C"
end_node = "G"
n = ed.process_route(start_node, end_node)
print(f"Dump of intelligence learned: {n}")

for node in n:
    print(f"nodes: {node}")

print(f"The shortest distance from start node {start_node} to end node {end_node} is {ed.find_shortest_route(start_node, end_node)}")
print(f"The route taken was: {ed.find_route(n, end_node)}")

print(f"End of program.")
"""