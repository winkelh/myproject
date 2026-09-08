from typing import Dict
from typing import KeysView


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
        smallest_known_distance: float('inf')
        
        for node in nodes.keys():
            if not nodes[node]['visited']:
                if nodes[node]['distance_to_start'] < smallest_known_distance:
                    nearest_node            = node
                    smallest_known_distance = nodes[node]['distance_to_start']
                
        return nearest_node
        
    def find_shortest_route(self, start_node: str, end_node: str) -> Dict:
        nodes = {}
        # initialize the nodes with distance_to_start and visited status
        for node in self.graph.keys():
            nodes[node] = {
                "distance_to_start": float('inf'),
                "visited": False,
            }
        nodes[start_node]["distance_to_start"] = 0

        # Walk through the nodes, start with the start node and walk through its unvisited neighbors.
        current_node = start_node
        while current_node != Graph.NOT_APPLICABLE:
            for neighbor in self.graph[current_node]["neighbors"]:
                current_node_distance_to_start = nodes[current_node]["distance_to_start"]
                edge_weight                    = self.graph[start_node]["neighbors"][neighbor]
                neighbor_distance_to_start     = nodes[neighbor]["distance_to_start"]
                if current_node_distance_to_start + edge_weight < neighbor_distance_to_start: 
                    nodes[neighbor]["distance_to_start"] = current_node_distance_to_start + edge_weight
                print(f"Debug: Start Node: {current_node} current node distance to start: {current_node_distance_to_start}; Neighbor node: {neighbor} Edge weigth: {edge_weight} / distance to start: {nodes[neighbor]["distance_to_start"]}")
                
                self.graph[current_node]["visited"] = True
                # Now initialize the next current node
            current_node = self.find_nearest_node(nodes)

        return nodes
        

ed = Graph()
ed.add_node("A")
ed.add_node("B")
ed.add_node("C")
ed.add_node("D")
print(f"List of the nodes: {ed.get_nodes()}")

ed.add_edge("A", "B", 10)
ed.add_edge("A", "C", 15)
ed.add_edge("B", "C", 18)
ed.add_edge("B", "D", 12)
ed.add_edge("C", "D", 13)
print(f"Dump of the edges: {ed.get_graph()}")


#print(f"Graph: {ed.get_graph()}")
#print(f"Nodes: {ed.get_nodes()}")
n = ed.find_shortest_route("A", "D")
print(f"Dump of intelligence learned: {n}")

for node in n:
    print(f"nodes: {node}")

print(f"End of program.")
