import random
from typing import Tuple, List

import igraph
import pandas as pd
from igraph import plot


class GraphException(igraph.InternalError):
    pass


class Graph:
    def __init__(
        self,
        vertices: int,
        edges: int,
        initial_vertex_index: int = 0,
        final_vertex_index: int = -1,
    ):
        self.graph_object = igraph.Graph()
        self.initial_vertex_index = initial_vertex_index
        self.final_vertex_index = final_vertex_index
        self.vertices = vertices
        self.edges_number = edges
        self.edge_weights = []
        self.generate_graph()
        self.set_edge_weights()
        self.graph_object.to_directed(False)

    @property
    def edges(self) -> List[Tuple[int, int]]:
        return self.graph_object.get_edgelist()

    @property
    def adjacency_matrix(self) -> pd.DataFrame:
        return pd.DataFrame(self.graph_object.get_adjacency().data)

    @property
    def shortest_path(self) -> List:
        return self.graph_object.get_shortest_paths(
            v=self.initial_vertex_index, to=self.graph_object.vs.indices[-1]
        )

    def get_edge_weights(self, edge: Tuple[int, int]) -> List[float]:
        return [e[edge] for e in self.edge_weights if edge in e]

    def generate_graph(self) -> None:
        if self.graph_object.get_edgelist():
            raise GraphException("Graph already exists")
        self.graph_object.add_vertices(self.vertices)
        self._generate_random_edges(self.edges_number)

    def plot_graph(self) -> None:
        self.graph_object.vs["label"] = self.graph_object.vs.indices
        plot(self.graph_object, margin=(30, 30, 30, 30))

    def set_edge_weights(self) -> None:
        self.edge_weights = [{e: random.random()} for e in self.edges]

    def _get_random_vertex(self) -> Tuple[int, int]:
        return random.randint(0, self.vertices - 1)

    def _generate_random_edges(self, number_of_edges) -> None:
        v_paires = [
            (self._get_random_vertex(), self._get_random_vertex())
            for e in range(number_of_edges)
        ]
        self.graph_object.add_edges(v_paires)


class ConnectedGraph(Graph):
    def generate_graph(self) -> None:
        if self.edges_number < self.vertices:
            raise GraphException(
                "Can't generate connected graph if number of edges is lesser than number of vertices"
            )
        self.graph_object = self.graph_object.Ring(n=self.vertices, circular=False)
        edges_to_add = self.edges_number - self.graph_object.ecount()
        self._generate_random_edges(edges_to_add)
