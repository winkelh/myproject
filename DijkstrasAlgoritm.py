graph = {
    "A" : {"visited" : False},

}

class Graph:
    graph = {} 

    def __init__(self, graph: Dict = {}) -> None:
        self.graph = graph

    def add_node(self, name: str) -> None:
        self.graph[name] = {"visited": False, "neighbours": {}}

    def add_edge(self, start_node: str, end_node: str, weigth: int) -> None:
        edge_id = start_node + "_" + end_node
        self.graph[start_node]["neighbours"][end_node] = weigth
        self.graph[end_node]["neighbours"][start_node] = weigth
        
    def add_node_set(self, data: Dict) -> None:
        self.graph.update(data)

    def get_nodes(self) -> Dict:
        return self.graph.keys()
        
    def get_graph(self) -> Dict:
        return self.graph
        
    def find_shortest_route(self, start_node: str, end_node: str) -> Dict:
        unvisited_nodes = set()
        unvisited_nodes.update(self.graph.keys())
        nodes = {}
        print(f"Nodes: {unvisited_nodes}")
        for node in unvisited_nodes:
            nodes[node][distance] = float('inf')
            nodes[node][visited] = False
        
        nodes[start_node][distance] = 0
        
        return {}
        

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

print(ed.get_graph())
print(ed.get_nodes())
ed.find_shortest_route("A", "D")

# Test string from work laptop
# ASnother Test string from work laptop
# And one from my private laptop

