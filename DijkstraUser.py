from DijkstrasAlgorithm import Graph

def main():
    graph = Graph()
    boardX = 10
    boardY = 10
    countX = 1
    countY = 1

    while countX <= boardX:
        countY = 1
        while countY <= boardY:
            graph.add_node(f"{countX}_{countY}")
            countY += 1
        countX += 1

    print(f"Graph: {graph.get_nodes()}")

if __name__ == "__main__":
    try: 
        main()
    except Exception as ex:
        print(ex)
        input("Press any key...")