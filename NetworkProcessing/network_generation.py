import random
from typing import Tuple, List, Dict

import igraph
import pandas as pd
from igraph import plot


class GraphException(igraph.InternalError):
    pass


class Graph:
    def __init__(
        self,
        vertices: int = None,
        edges: int = None,
        initial_vertex_index: int = 0,
        final_vertex_index: int = -1,
        is_directed=True,
        is_simple=True,
        filename: str = None,
    ):
        self.initial_vertex_index = initial_vertex_index
        self.final_vertex_index = final_vertex_index
        self.graph_object = igraph.Graph()
        if filename:
            self.graph_object = self.load_graph(filename)
            self.vertices = self.graph_object.vcount()
            self.edges_number = self.graph_object.ecount()
        else:
            if not vertices or not edges:
                raise GraphException(
                    f"Vertices and edges numbers should be specified if graph is generated"
                )
            self.vertices = vertices
            self.edges_number = edges
            self.generate_graph()
        if (
            self.vertices < self.initial_vertex_index
            or self.vertices < self.final_vertex_index
        ):
            raise GraphException(
                f"Incorrect vertex indexes passed in argument list "
                f"for the graph loaded from file{filename} "
            )
        self.edge_weights = []
        self.set_edge_weights()
        self.__disabled_vertices = {}
        if is_directed:
            self.graph_object.to_directed(False)
        if is_simple:
            self.graph_object.simplify()

    def __str__(self):
        return self.adjacency_matrix

    @property
    def edges(self) -> List[Tuple[int, int]]:
        return self.graph_object.get_edgelist()

    @property
    def adjacency_matrix(self) -> pd.DataFrame:
        return pd.DataFrame(self.graph_object.get_adjacency().data)

    @property
    def shortest_path(self) -> List[int]:
        return self.graph_object.get_shortest_paths(
            v=self.initial_vertex_index, to=self.graph_object.vs.indices[-1]
        )

    @property
    def incidence_dict(self) -> Dict[int, List[Tuple[int, int]]]:
        incidence_list = self.graph_object.get_inclist()
        return {
            v: [self.edges[e] for e in incidence_list[v]]
            for v, inc in enumerate(incidence_list)
        }

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

    def __copy__(self):
        new_copy = type(self)(
            vertices=self.vertices,
            edges=self.edges_number,
            initial_vertex_index=self.initial_vertex_index,
            final_vertex_index=self.final_vertex_index,
        )
        new_copy.__dict__.update(self.__dict__)
        return new_copy

    def disable_vertex(self, vertex: int) -> None:
        self.__disabled_vertices[vertex] = self.incidence_dict[vertex]
        self.graph_object.delete_edges(self.__disabled_vertices[vertex])
        del self.incidence_dict[vertex]

    def enable_vertex(self, vertex: int) -> None:
        self.incidence_dict[vertex] = self.__disabled_vertices[vertex]
        self.graph_object.add_edges(self.__disabled_vertices[vertex])
        del self.__disabled_vertices[vertex]

    def is_vertex_enabled(self, vertex: int) -> None:
        return vertex not in self.__disabled_vertices

    def find_all_paths(
        self, start_vertex: int, end_vertex: int, cursor_path: List[int] = None
    ) -> List[List[int]]:
        cursor_path = cursor_path + [start_vertex] if cursor_path else [start_vertex]
        if start_vertex == end_vertex:
            return [cursor_path]
        all_paths = []
        for node in set(self.graph_object.neighbors(start_vertex)) - set(cursor_path):
            all_paths.extend(self.find_all_paths(node, end_vertex, cursor_path))
        return all_paths

    def load_graph(self, filename: str) -> igraph.Graph:
        return self.graph_object.Read_GraphML(filename)

    def save_graph(self, filename: str) -> None:
        self.graph_object.write_graphml(filename)


class ConnectedGraph(Graph):
    def generate_graph(self) -> None:
        if self.edges_number < self.vertices:
            raise GraphException(
                "Can't generate connected graph if number of edges is lesser than number of vertices"
            )
        self.graph_object = self.graph_object.Ring(n=self.vertices, circular=False)
        edges_to_add = self.edges_number - self.graph_object.ecount()
        self._generate_random_edges(edges_to_add)

    def get_all_shortest_paths(self) -> List[List[Tuple[int, int]]]:
        return self.graph_object.get_all_shortest_paths(
            v=self.initial_vertex_index, to=self.graph_object.vs.indices[-1]
        )
