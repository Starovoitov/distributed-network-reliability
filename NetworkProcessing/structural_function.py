import collections
from typing import List, Tuple

from NetworkProcessing.graphs import Graph
from utils import multiple_values_in_list, get_random_struct_values


class StructuralFunctionError(ValueError):
    pass


class StructuralFunction:
    def __init__(self, g: Graph, vertices_values: List[bool] = None):
        self.graph = g
        self.min_non_workable_cuts = self.get_all_min_non_workable_cuts()
        self.min_workable_paths = self.get_all_min_workable_paths()

        if vertices_values is not None:
            self.vertices_values = vertices_values
        else:
            self.vertices_values = get_random_struct_values(self.graph.vertices)

        self.min_paths_structural_function_value = (
            self.calculate_structural_function_min_paths()
        )
        self.min_cuts_structural_function_value = (
            self.calculate_structural_function_min_cuts()
        )

    def __str__(self):
        return (
            f"Min paths collected: {self.min_workable_paths}\n"
            f"Min cuts collected: {self.min_non_workable_cuts}"
        )

    def get_all_min_workable_paths(self) -> List[List[int]]:
        return self.graph.find_all_paths(0, self.graph.vertices - 1)

    def get_all_min_non_workable_cuts(self) -> List[List[Tuple[int, int]]]:
        trees_built = [[0]]
        self.__find_new_trees(trees_built)

        sections = sorted(
            [self.graph.incidence_dict[tree[-1]] for tree in trees_built]
        )

        not_min_sections = []

        for section in sorted(sections, key=len):
            if not section:
                continue

            rest_sections = sections.copy()
            rest_sections.remove(section)

            including_sections = [r for r in rest_sections if section in r]
            not_min_sections.extend(including_sections)

        return [s for s in sections if s and s not in not_min_sections]

    def set_new_vertices_values(self, vertices_values: List[bool]) -> None:
        if len(vertices_values) != len(self.vertices_values):
            raise StructuralFunctionError(
                "Mismatch of vertices between argument and graph of structural function"
            )

        self.vertices_values = vertices_values

        self.min_paths_structural_function_value = (
            self.calculate_structural_function_min_paths()
        )

        self.min_cuts_structural_function_value = (
            self.calculate_structural_function_min_cuts()
        )

    def calculate_structural_function_value_for_serial(
        self, structural_elements: List[int]
    ) -> bool:
        """
        Serial block:
        X1 * X2 * ... * Xn
        """
        return bool(
            multiple_values_in_list(
                [self.vertices_values[v] for v in structural_elements]
            )
        )

    def calculate_structural_function_min_paths(self) -> bool:
        """
        OR over all minimal paths:
        φ(X) = P1 OR P2 OR ...
        """
        structural_block_values = [
            self.calculate_structural_function_value_for_serial(p)
            for p in self.min_workable_paths
        ]

        return any(structural_block_values)

    def calculate_structural_function_min_cuts(self) -> bool:
        """
        AND over all cuts:
        φ(X) = C1 AND C2 AND ...
        where each cut is OR over its elements
        """
        cut_values = []

        for cut in self.min_non_workable_cuts:
            if len(cut) == 1:
                destination_vertices = [max(cut[0])]
            else:
                vertices_in_cut = [vertex for edge in cut for vertex in edge]

                common_source = [
                    vertex
                    for vertex, count in collections.Counter(
                        vertices_in_cut
                    ).items()
                    if count > 1
                ][0]

                destination_vertices = list(
                    {
                        vertex
                        for edge in cut
                        for vertex in edge
                        if vertex != common_source
                    }
                )

            # OR inside each cut
            cut_value = any(
                self.vertices_values[v] for v in destination_vertices
            )

            cut_values.append(cut_value)

        # AND between cuts
        return all(cut_values)

    def __find_new_trees(self, constructed_trees: List[List[int]]) -> None:
        cursor_tree = constructed_trees[-1]
        cursor_vertex = cursor_tree[-1]

        if cursor_vertex == self.graph.vertices - 1:
            return

        neighbours = [
            sorted(e)[1]
            for e in self.graph.edges
            if cursor_vertex in e
        ]

        for n in neighbours:
            if n == cursor_vertex:
                continue

            # защита от циклов
            if n in cursor_tree:
                continue

            current_tree = cursor_tree + [n]
            constructed_trees.append(current_tree)

        if len(constructed_trees) > 1:
            self.__find_new_trees(constructed_trees)
