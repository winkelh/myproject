from DijkstrasAlgorithm import Graph

def main():
    graph = Graph()
    boardX = 1000
    boardY = 1000
    countX = 1
    countY = 1

    while countX <= boardX:
        countY = 1
        while countY <= boardY:
            graph.add_node(f"{countX}_{countY}")
            countY += 1
        countX += 1

    # Connect each node to its right and lower neighbor in the grid.
    for x in range(1, boardX + 1):
        for y in range(1, boardY + 1):
            current_node = f"{x}_{y}"
            if x < boardX:
                graph.add_edge(current_node, f"{x + 1}_{y}", 1)
            if y < boardY:
                graph.add_edge(current_node, f"{x}_{y + 1}", 1)

    start_node = "3_4"
    end_node = "899_979"
    n = graph.process_route(start_node, end_node)
    print(f"The shortest distance from start node {start_node} to end node {end_node} is {graph.find_shortest_route(start_node, end_node)}")
    print(f"The route taken was: {graph.find_route(n, end_node)}")



if __name__ == "__main__":
    try: 
        main()
    except Exception as ex:
        print(ex)
        input("Press any key...")