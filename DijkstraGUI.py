"""Tkinter visualizer for navigating a rectangular grid with Graph."""

from __future__ import annotations

from dataclasses import dataclass
from queue import Empty, Queue
from threading import Thread
import tkinter as tk
from tkinter import messagebox, ttk

from DijkstrasAlgorithm import Graph


@dataclass(frozen=True)
class Progress:
    """A thread-safe message containing one algorithm animation step."""

    current_node: str


@dataclass(frozen=True)
class Finished:
    """A thread-safe message containing the completed route state."""

    nodes: dict[str, dict]
    end_node: str


@dataclass(frozen=True)
class Failed:
    """A thread-safe message containing a worker error."""

    error: Exception


class DijkstraGUI:
    """Build and animate a grid graph through a small Tkinter interface."""

    MAX_DIMENSION = 100
    CANVAS_WIDTH = 900
    CANVAS_HEIGHT = 650

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Dijkstra Grid Navigator")
        self.root.resizable(False, False)

        # The queue is the deliberate boundary between the worker thread and
        # Tkinter.  Tkinter widgets must only be touched by the main thread,
        # so the background algorithm sends data here and the UI polls it.
        self.messages: Queue[Progress | Finished | Failed] = Queue()
        self.worker: Thread | None = None
        self.node_positions: dict[str, tuple[float, float]] = {}
        self.route: list[str] = []
        self.route_index = 0
        self.visited_nodes: set[str] = set()
        self.current_node: str | None = None
        self.running = False

        self.x_size = tk.StringVar(value="30")
        self.y_size = tk.StringVar(value="20")
        self.start_x = tk.StringVar(value="1")
        self.start_y = tk.StringVar(value="1")
        self.end_x = tk.StringVar(value="30")
        self.end_y = tk.StringVar(value="20")
        self.status = tk.StringVar(value="Enter grid and endpoint coordinates.")

        self._build_controls()
        self.canvas = tk.Canvas(
            root,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            background="white",
            highlightthickness=1,
            highlightbackground="#999999",
        )
        self.canvas.pack(padx=10, pady=(0, 10))

        # Polling is scheduled rather than blocking in wait/join, which keeps
        # the window repainting and responsive throughout the animation.
        self.root.after(30, self._poll_messages)

    def _build_controls(self) -> None:
        # Each field is explicit about its coordinate meaning: x is the
        # horizontal column and y is the vertical row, both starting at 1.
        controls = ttk.Frame(self.root, padding=10)
        controls.pack(fill="x")
        fields = (
            ("X size", self.x_size),
            ("Y size", self.y_size),
            ("Begin X", self.start_x),
            ("Begin Y", self.start_y),
            ("End X", self.end_x),
            ("End Y", self.end_y),
        )
        for column, (label, variable) in enumerate(fields):
            ttk.Label(controls, text=label).grid(row=0, column=column, padx=3)
            ttk.Entry(controls, textvariable=variable, width=7).grid(
                row=1, column=column, padx=3
            )

        self.start_button = ttk.Button(
            controls, text="Start navigation", command=self.start_navigation
        )
        self.start_button.grid(row=1, column=len(fields), padx=(10, 3))
        ttk.Label(controls, textvariable=self.status).grid(
            row=2, column=0, columnspan=len(fields) + 1, pady=(8, 0)
        )

    @staticmethod
    def _node(x: int, y: int) -> str:
        # A single conversion method guarantees that GUI coordinates and Graph
        # node names use exactly the same representation.
        return f"{x}_{y}"

    def _read_input(self) -> tuple[int, int, str, str]:
        # Validation happens before any graph allocation, so malformed input
        # cannot leave a half-built visualization behind.
        try:
            width = int(self.x_size.get())
            height = int(self.y_size.get())
            start_x = int(self.start_x.get())
            start_y = int(self.start_y.get())
            end_x = int(self.end_x.get())
            end_y = int(self.end_y.get())
        except ValueError as error:
            raise ValueError("All size and coordinate fields must be integers.") from error

        if not (1 <= width <= self.MAX_DIMENSION and 1 <= height <= self.MAX_DIMENSION):
            raise ValueError(
                f"Grid dimensions must be between 1 and {self.MAX_DIMENSION}."
            )
        for label, x, y in (
            ("begin", start_x, start_y),
            ("end", end_x, end_y),
        ):
            if not (1 <= x <= width and 1 <= y <= height):
                raise ValueError(
                    f"{label.title()} point ({x}, {y}) must be inside the grid."
                )
        return width, height, self._node(start_x, start_y), self._node(end_x, end_y)

    def _build_graph(self, width: int, height: int) -> Graph:
        # The GUI constructs the same four-neighbor rectangular graph as the
        # existing command-line example, with unit weights in every direction.
        graph = Graph()
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                graph.add_node(self._node(x, y))
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                current = self._node(x, y)
                if x < width:
                    graph.add_edge(current, self._node(x + 1, y), 1)
                if y < height:
                    graph.add_edge(current, self._node(x, y + 1), 1)
        return graph

    def _draw_grid(self, width: int, height: int) -> None:
        # Cell coordinates are calculated once and reused by every animation
        # frame, avoiding repeated geometry work while colors change.
        self.canvas.delete("all")
        cell_width = self.CANVAS_WIDTH / width
        cell_height = self.CANVAS_HEIGHT / height
        self.node_positions.clear()
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                node = self._node(x, y)
                left = (x - 1) * cell_width
                top = (y - 1) * cell_height
                self.node_positions[node] = (
                    left + cell_width / 2,
                    top + cell_height / 2,
                )
                self.canvas.create_rectangle(
                    left,
                    top,
                    left + cell_width,
                    top + cell_height,
                    fill="#f4f4f4",
                    outline="#d0d0d0",
                    tags=(node,),
                )

    def _paint_node(self, node: str, color: str) -> None:
        # Canvas tags let one node be recolored without retaining thousands of
        # individual rectangle IDs.
        self.canvas.itemconfigure(node, fill=color)

    def start_navigation(self) -> None:
        if self.running:
            return
        try:
            width, height, start_node, end_node = self._read_input()
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        graph = self._build_graph(width, height)
        self._draw_grid(width, height)
        self._paint_node(start_node, "#55a868")
        self._paint_node(end_node, "#c44e52")
        self.visited_nodes.clear()
        self.current_node = None
        self.route = []
        self.route_index = 0
        self.running = True
        self.start_button.configure(state="disabled")
        self.status.set(f"Navigating from {start_node} to {end_node}...")

        # The algorithm runs off the Tkinter thread.  Its callback only places
        # one node name on the queue, so it never touches widgets or copies
        # the complete graph state.
        self.worker = Thread(
            target=self._run_graph,
            args=(graph, start_node, end_node),
            daemon=True,
        )
        self.worker.start()

    def _run_graph(self, graph: Graph, start_node: str, end_node: str) -> None:
        # The callback is intentionally incremental.  The UI already owns its
        # visited set, so rebuilding it from every full algorithm snapshot is
        # unnecessary O(V) work for every finalized node.
        def report(current_node: str) -> None:
            self.messages.put(Progress(current_node))

        try:
            nodes = graph.process_route(
                start_node, end_node, progress_callback=report
            )
            # Include the requested destination because Dijkstra deliberately
            # stops as soon as it is finalized; it is not safe to infer the
            # destination by looking for a node that visited every grid cell.
            self.messages.put(Finished(nodes, end_node))
        except Exception as error:
            self.messages.put(Failed(error))

    def _poll_messages(self) -> None:
        # Drain stale progress messages and keep only the newest one.  The
        # worker can finish many algorithm steps before Tkinter gets a chance
        # to repaint; animating every queued historical step makes the window
        # lag far behind the actual result.
        try:
            message = self.messages.get_nowait()
        except Empty:
            self.root.after(30, self._poll_messages)
            return

        if isinstance(message, Progress):
            newest_progress = message
            try:
                while True:
                    next_message = self.messages.get_nowait()
                    if isinstance(next_message, Progress):
                        newest_progress = next_message
                    else:
                        # Preserve terminal messages so they are handled by
                        # the next polling cycle after this visual update.
                        self.messages.put(next_message)
                        break
            except Empty:
                pass

            message = newest_progress
            if self.current_node is not None:
                self.visited_nodes.add(self.current_node)
                self._paint_node(self.current_node, "#9ecae1")
            self.visited_nodes.add(message.current_node)
            self.current_node = message.current_node
            self._paint_node(message.current_node, "#fdae6b")
            self.status.set(f"Exploring {message.current_node}...")
        elif isinstance(message, Finished):
            self.route = self._route_from_nodes(message.nodes, message.end_node)
            self.route_index = 0
            self._animate_route()
        else:
            self.running = False
            self.start_button.configure(state="normal")
            messagebox.showerror("Navigation failed", str(message.error))
            self.status.set("Navigation failed.")

        self.root.after(30, self._poll_messages)

    @staticmethod
    def _route_from_nodes(nodes: dict[str, dict], destination: str) -> list[str]:
        # The destination is supplied by the Finished message because
        # process_route intentionally stops early rather than visiting every
        # node in the grid.  An infinite distance means that no route exists.
        if (
            destination not in nodes
            or nodes[destination]["distance_to_start"] == float("inf")
        ):
            return []
        route: list[str] = []
        current: str | None = destination
        while current is not None:
            route.append(current)
            current = nodes[current]["previous_node"]
        route.reverse()
        return route

    def _animate_route(self) -> None:
        # A second animation phase highlights the final predecessor chain,
        # making the distinction between explored nodes and the chosen route
        # visible to the user.
        if self.route_index >= len(self.route):
            self.running = False
            self.start_button.configure(state="normal")
            self.status.set(
                f"Navigation complete: {max(0, len(self.route) - 1)} steps."
                if self.route
                else "No route exists."
            )
            return
        node = self.route[self.route_index]
        self._paint_node(node, "#4c78a8")
        self.route_index += 1
        self.root.after(70, self._animate_route)


def main() -> None:
    # Keeping startup behind main prevents a window from opening merely by
    # importing this module, which also makes the GUI easier to test.
    root = tk.Tk()
    DijkstraGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
