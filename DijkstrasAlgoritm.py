from typing import Dict
from typing import KeysView


class Graph:
    def __init__(self, graph: Dict = None) -> None:
        self.graph = graph if graph is not None else {}

    def add_node(self, name: str) -> None:
        self.graph[name] = {"visited": False, "neighbors": {}}

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
        
    def find_shortest_route(self, start_node: str, end_node: str) -> Dict:
        # initialize the nodes with distance and visited status
        unvisited_nodes = set(self.graph.keys())
        nodes = {}
        for node in unvisited_nodes:
            nodes[node] = {
                "distance": float('inf'),
                "visited": False
            }
        nodes[start_node]["distance"] = 0

        # Walk through the nodes
        current_node = self.graph[start_node]
        self.graph[start_node]["visited"] = True
        for neighbor in self.graph[start_node]["neighbors"]:
            distance = self.graph[start_node]["neighbors"][neighbor]
            self.graph[neighbor]["visited"] = True
            if distance < self.graph[start_node]["neighbors"][neighbor]: 
                self.graph[start_node]["neighbors"][neighbor] = distance
            print(f"neighbor: {neighbor}; distance: {distance}")
        return nodes
        

ed = Graph()
ed.add_node("A")
ed.add_node("B")
ed.add_node("C")
ed.add_node("D")

ed.add_edge("A", "B", 10)
ed.add_edge("A", "C", 15)
ed.add_edge("B", "C", 18)
ed.add_edge("B", "D", 12)
ed.add_edge("C", "D", 13)
print(f"Dump of the edges: {ed.get_graph()}")


#print(f"Graph: {ed.get_graph()}")
#print(f"Nodes: {ed.get_nodes()}")
n = ed.find_shortest_route("A", "D")
print(f"Shortest route: {n}")


