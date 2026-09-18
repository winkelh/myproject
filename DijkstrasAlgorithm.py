"""A small undirected graph implementation using Dijkstra's algorithm."""

from heapq import heappop, heappush
from numbers import Real
from typing import Any, Callable


class Graph:
    """An undirected weighted graph with non-negative edge weights.

    Dijkstra's algorithm is only correct when every edge weight is
    non-negative, so this class validates that requirement when edges are
    created.  Nodes are represented by names and stored in an adjacency list.
    """

    def __init__(self, graph: dict[str, dict[str, dict[str, Real]]] | None = None):
        # The old constructor used a mutable dictionary default.  Although
        # that default was not mutated between instances in normal use, using
        # None and creating a fresh dictionary avoids accidental state sharing.
        self.graph = graph if graph is not None else {}

        # An input graph is accepted for compatibility, but validating it here
        # makes malformed data fail at construction time rather than much later
        # inside the shortest-path algorithm.
        for node, data in self.graph.items():
            if not isinstance(data, dict) or not isinstance(data.get("neighbors"), dict):
                raise ValueError(
                    f"Node {node!r} must contain a 'neighbors' dictionary."
                )

    def add_node(self, name: str) -> None:
        # Silently replacing an existing node used to erase all of its edges.
        # Raising an explicit error protects the graph and tells the caller
        # that the requested operation would destroy existing data.
        if name in self.graph:
            raise ValueError(f"Node {name!r} already exists.")
        self.graph[name] = {"neighbors": {}}

    def add_edge(self, start_node: str, end_node: str, weight: Real) -> None:
        # The previous implementation assumed both nodes existed and would
        # fail with an opaque KeyError.  Explicit checks make the public API
        # easier to use and prevent edges pointing at unknown nodes.
        if start_node not in self.graph:
            raise KeyError(f"Unknown start node: {start_node!r}")
        if end_node not in self.graph:
            raise KeyError(f"Unknown end node: {end_node!r}")

        # Negative weights invalidate Dijkstra's algorithm, while non-numeric
        # and non-finite values make distance comparisons unreliable.  Reject
        # them at the boundary instead of producing an incorrect path.
        if isinstance(weight, bool) or not isinstance(weight, Real):
            raise TypeError("Edge weight must be a finite non-negative number.")
        if weight < 0 or weight != weight or weight in (float("inf"), float("-inf")):
            raise ValueError("Edge weight must be a finite non-negative number.")

        # add_edge has always created a connection in both directions.  The
        # behavior is retained and documented explicitly so existing grid
        # callers remain correct; use a separate directed-graph abstraction
        # if one-way edges are required.
        self.graph[start_node]["neighbors"][end_node] = weight
        self.graph[end_node]["neighbors"][start_node] = weight

    def add_node_set(self, data: dict[str, dict[str, dict[str, Real]]]) -> None:
        # Bulk insertion now goes through the same validation path as normal
        # insertion.  This prevents callers from bypassing the node invariant
        # by placing arbitrary dictionaries directly into self.graph.
        if not isinstance(data, dict):
            raise TypeError("Node set must be a dictionary.")
        for node, node_data in data.items():
            if node in self.graph:
                raise ValueError(f"Node {node!r} already exists.")
            if (
                not isinstance(node_data, dict)
                or not isinstance(node_data.get("neighbors"), dict)
            ):
                raise ValueError(
                    f"Node {node!r} must contain a 'neighbors' dictionary."
                )
            self.graph[node] = {"neighbors": {}}

        # Validate and copy edges after all nodes have been installed, so
        # references between nodes in the same batch are supported.
        for node, node_data in data.items():
            for neighbor, weight in node_data["neighbors"].items():
                self.add_edge(node, neighbor, weight)

    def get_nodes(self):
        # Returning the existing keys view preserves the original lightweight
        # API while keeping the graph itself available for existing callers.
        return self.graph.keys()

    def get_graph(self):
        # This method remains for compatibility.  Callers should treat the
        # returned structure as read-only because mutating it can bypass the
        # validation performed by add_node and add_edge.
        return self.graph

    def find_nearest_node(self, nodes: dict[str, dict[str, Any]]) -> str | None:
        # This compatibility helper still performs a linear scan, but the
        # actual shortest-path implementation below uses a heap and therefore
        # does not suffer from this O(V) selection cost on every iteration.
        candidates = (
            node
            for node, state in nodes.items()
            if not state["visited"] and state["distance_to_start"] != float("inf")
        )
        return min(
            candidates,
            key=lambda node: nodes[node]["distance_to_start"],
            default=None,
        )

    def process_route(
        self,
        start_node: str,
        end_node: str,
        progress_callback: Callable[[str], None] | None = None,
    ) -> dict[str, dict[str, Any]]:
        # Validate both endpoints before indexing the adjacency list.  This
        # replaces accidental KeyErrors with errors that identify the invalid
        # API argument directly.
        if start_node not in self.graph:
            raise KeyError(f"Unknown start node: {start_node!r}")
        if end_node not in self.graph:
            raise KeyError(f"Unknown end node: {end_node!r}")

        # Keep the original result shape so find_route and existing callers
        # continue to work, while recording the predecessor needed to rebuild
        # the actual path.
        nodes = {
            node: {
                "distance_to_start": float("inf"),
                "visited": False,
                "previous_node": None,
            }
            for node in self.graph
        }
        nodes[start_node]["distance_to_start"] = 0

        # A heap gives O((V + E) log V) behavior instead of repeatedly scanning
        # every node.  Duplicate heap entries are expected: when a shorter
        # route is found, the new distance is pushed and the stale entry is
        # discarded when it is popped.
        queue: list[tuple[Real, str]] = [(0, start_node)]
        while queue:
            current_distance, current_node = heappop(queue)
            known_distance = nodes[current_node]["distance_to_start"]

            # Ignore stale queue entries and already-finalized nodes.  With
            # non-negative weights, the first valid pop finalizes this node.
            if current_distance != known_distance or nodes[current_node]["visited"]:
                continue

            nodes[current_node]["visited"] = True

            # The optional callback exposes only the newly finalized node.
            # Sending the complete nodes dictionary here used to copy every
            # node for every step, turning an otherwise efficient algorithm
            # into an avoidable O(V^2) progress-reporting operation.
            if progress_callback is not None:
                progress_callback(current_node)

            # Once the destination is finalized, its shortest distance and
            # predecessor are complete; processing the rest of the graph is
            # unnecessary work.
            if current_node == end_node:
                break

            for neighbor, edge_weight in self.graph[current_node]["neighbors"].items():
                tentative_distance = current_distance + edge_weight
                if tentative_distance < nodes[neighbor]["distance_to_start"]:
                    nodes[neighbor]["distance_to_start"] = tentative_distance
                    nodes[neighbor]["previous_node"] = current_node
                    heappush(queue, (tentative_distance, neighbor))

        return nodes

    def find_shortest_route(
        self, start_node: str, end_node: str
    ) -> Real | None:
        # Returning None for an unreachable destination is clearer than
        # exposing infinity as though it were a usable route length.
        nodes = self.process_route(start_node, end_node)
        distance = nodes[end_node]["distance_to_start"]
        return None if distance == float("inf") else distance

    def find_route(
        self, nodes: dict[str, dict[str, Any]], end_node: str
    ) -> list[str]:
        # Validate the supplied route state and return an empty path for an
        # unreachable destination instead of returning [end_node], which used
        # to look like a successful one-node route.
        if end_node not in nodes:
            raise KeyError(f"Unknown end node: {end_node!r}")
        if nodes[end_node]["distance_to_start"] == float("inf"):
            return []

        route: list[str] = []
        current_node: str | None = end_node
        while current_node is not None:
            route.append(current_node)
            current_node = nodes[current_node]["previous_node"]

        # Backtracking discovers the target-to-source order; reverse it for
        # the conventional source-to-target route returned to the caller.
        route.reverse()
        return route
