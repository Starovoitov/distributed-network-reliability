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
        vertices: int,
        edges: int,
        initial_vertex_index: int = 0,
        final_vertex_index: int = -1,
        is_directed=True,
        is_simple=True,
    ):
        self.graph_object = igraph.Graph()
        self.initial_vertex_index = initial_vertex_index
        self.final_vertex_index = final_vertex_index
        self.vertices = vertices
        self.edges_number = edges
        self.edge_weights = []
        self.generate_graph()
        self.set_edge_weights()
        self.__disabled_vertices = {}
        if is_directed:
            self.graph_object.to_directed(False)
        if is_simple:
            self.graph_object.simplify()

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

    def disable_vertice(self, vertice: int) -> None:
        self.__disabled_vertices[vertice] = self.incidence_dict[vertice]
        self.graph_object.delete_edges(self.__disabled_vertices[vertice])
        del self.incidence_dict[vertice]

    def enable_vertice(self, vertice: int) -> None:
        self.incidence_dict[vertice] = self.__disabled_vertices[vertice]
        self.graph_object.add_edges(self.__disabled_vertices[vertice])
        del self.__disabled_vertices[vertice]

    def is_vertice_enabled(self, vertice: int) -> None:
        return vertice not in self.__disabled_vertices


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

    def get_all_min_sections(self) -> List[List[Tuple[int, int]]]:
        trees_built = [[0]]
        self.__find_new_trees(trees_built)
        sections = sorted([self.incidence_dict[tree[-1]] for tree in trees_built])
        not_min_sections = []
        for section in sorted(sections, key=len):
            if not section:
                continue
            rest_sections = sections.copy()
            rest_sections.remove(section)
            including_sections = [r for r in rest_sections if section in r]
            not_min_sections.extend(including_sections)
        return [s for s in sections if s and s not in not_min_sections]

    def __find_new_trees(self, constructed_trees: List[List[int]]) -> None:
        cursor_tree = constructed_trees[-1]
        cursor_vertice = cursor_tree[-1]
        if cursor_vertice == self.vertices - 1:
            return
        neighbours = [sorted(e)[1] for e in self.edges if cursor_vertice in e]
        for n in neighbours:
            if n == cursor_vertice:
                continue
            current_tree = cursor_tree + [n]
            constructed_trees.append(current_tree)
        self.__find_new_trees(constructed_trees)
