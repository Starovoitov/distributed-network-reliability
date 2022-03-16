import random
from typing import Tuple, List

import igraph
import pandas as pd
from igraph import plot


class GraphException(igraph.InternalError):
    pass


class Graph:

    def __init__(self, vertices: int, edges: int, initial_vertex_index: int = 0, final_vertex_index: int = -1):
        self.graph_object = igraph.Graph()
        self.initial_vertex_index = initial_vertex_index
        self.final_vertex_index = final_vertex_index
        self.vertices = vertices
        self.edges_number = edges
        self.edge_weights = []
        self.generate_graph()
        self.set_edge_weights()

    @property
    def edges(self) -> List[Tuple[int, int]]:
        return self.graph_object.get_edgelist()

    @property
    def adjacency_matrix(self) -> pd.DataFrame:
        return pd.DataFrame(self.graph_object.get_adjacency().data)

    @property
    def shortest_path(self) -> List:
        return self.graph_object.get_shortest_paths(v=self.initial_vertex_index, to=self.graph_object.vs.indices[-1])

    def get_edge_weights(self, edge: Tuple[int, int]) -> List[float]:
        return [e[edge] for e in self.edge_weights if edge in e]

    def generate_graph(self) -> None:
        if self.graph_object.get_edgelist():
            raise GraphException("Graph already exists")
        self.graph_object.add_vertices(self.vertices)
        v_paires = [(self.__get_random_vertex(), self.__get_random_vertex()) for e in range(self.edges_number)]
        self.graph_object.add_edges(v_paires)

    def plot_graph(self) -> None:
        layout = self.graph_object.layout_kamada_kawai()
        plot(self.graph_object, layout=layout)

    def set_edge_weights(self) -> None:
        self.edge_weights = [{e: random.random()} for e in self.edges]

    def __get_random_vertex(self) -> Tuple[int, int]:
        return random.randint(0, self.vertices - 1)
