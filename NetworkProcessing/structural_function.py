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
        if vertices_values:
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
        #  As per definition of min path as "min path is a min set of workable elements ensuring system functioning"
        return self.graph.find_all_paths(0, self.graph.vertices - 1)

    def get_all_min_non_workable_cuts(self) -> List[List[Tuple[int, int]]]:
        # As per definition of min cut as "min cut is a min set of non-workable elements ensuring system failure while
        # restoring of any of them leads to restoring of system functioning"
        trees_built = [[0]]
        self.__find_new_trees(trees_built)
        sections = sorted([self.graph.incidence_dict[tree[-1]] for tree in trees_built])
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
        """Structural block is a construction of type (1 - X1X2...Xn)"""
        elements_value = multiple_values_in_list(
            [self.vertices_values[v] for v in structural_elements]
        )
        return bool(1 - elements_value)

    def calculate_structural_function_min_paths(self) -> bool:
        """Structural function for min paths has a following template: 1 - (1 - X1..Xn)*(1 - X1..Xn)....
            where (1 - X1...Xn) is a structural function for series of elements in path
        """
        structural_block_values = [
            self.calculate_structural_function_value_for_serial(p)
            for p in self.min_workable_paths
        ]
        return bool(1 - multiple_values_in_list(structural_block_values))

    def calculate_structural_function_min_cuts(self) -> bool:
        """Structural function for min cuts has a following template:
        [1 - (1 - x1)(1 - X2)..][1 - (1 - x1)..(1 - Xn)]... where [1 - (1 - x1)(1 - X2)..]
        is a structural function for every single cut
        """
        for cut in self.min_non_workable_cuts:
            if len(cut) == 1:
                destination_vertices = [max(cut[0])]
            else:
                vertices_in_cut = [vertex for edge in cut for vertex in edge]
                common_source = [
                    vertex
                    for vertex, count in collections.Counter(vertices_in_cut).items()
                    if count > 1
                ][0]
                destination_vertices = list(
                    set(
                        [
                            vertex
                            for edge in cut
                            for vertex in edge
                            if vertex != common_source
                        ]
                    )
                )
            structural_block_values = [
                1 - self.calculate_structural_function_value_for_serial([v])
                for v in destination_vertices
            ]
            return bool(multiple_values_in_list(structural_block_values))

    def __find_new_trees(self, constructed_trees: List[List[int]]) -> None:
        cursor_tree = constructed_trees[-1]
        cursor_vertex = cursor_tree[-1]
        if cursor_vertex == self.graph.vertices - 1:
            return
        neighbours = [sorted(e)[1] for e in self.graph.edges if cursor_vertex in e]
        for n in neighbours:
            if n == cursor_vertex:
                continue
            current_tree = cursor_tree + [n]
            constructed_trees.append(current_tree)
        self.__find_new_trees(constructed_trees)
