import os
import uuid

from igraph import Graph
from igraph import InternalError
from igraph import plot


class GraphException(InternalError):
    pass


class GraphInterface:
    def __init__(self):
        self.graph_object = None

    def plot_graph(self) -> None:
        self.graph_object.vs["label"] = self.graph_object.vs.indices
        plot(self.graph_object, margin=(30, 30, 30, 30))

    def load_graph(self, filename: str) -> Graph:
        return self.graph_object.Read_GraphML(filename)

    def save_graph(self, filename: str) -> None:
        self.graph_object.write_graphml(filename)

    def get_graphml(self) -> str:
        temp_filename = str(uuid.uuid4())
        self.save_graph(temp_filename)
        with open(temp_filename) as f:
            graphml = f.read()
        os.remove(temp_filename)
        return graphml
