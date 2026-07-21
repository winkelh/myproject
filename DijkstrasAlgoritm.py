graph = {
    "A" : {"visited" : False},

}

class Graph:
    nodes = {}

    def __init__(self):
        pass

    def dijkstra(self, data: dict, start: str, goal: str) -> int:
        pass
    
    def add_node(self, name: str) -> None:
        self.nodes[name] = {"visited": False, "neighbours": {}}

    def add_edge(self, start_node: str, end_node: str, weigth: int) -> None:
        edge_id = start_node + "_" + end_node
        self.nodes[start_node]["neighbours"][end_node] = weigth
        self.nodes[end_node]["neighbours"][start_node] = weigth
        
    def add_node_set(self, data: Dict) -> None:
        self.nodes.update(data)

    def get_nodes(self) -> Dict:
        return self.nodes
        
    def navigate_route(self) -> Dict:
        for node in self.nodes.keys():
            is_visited = self.nodes[node]['visited']
            print(f"Is Node: {node} visited: {is_visited}")
        

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

print(ed.get_nodes())

# Test string from work laptop
# ASnother Test string from work laptop
