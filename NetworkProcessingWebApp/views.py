from aiohttp import web

from NetworkProcessing.network_generation import ConnectedGraph
from NetworkProcessing.structural_function import StructuralFunction
from NetworkProcessingDbLogic.db_controller import DbController


async def index(request):
    number_of_vertices = 15
    number_of_edges = number_of_vertices + 4
    g = ConnectedGraph(number_of_vertices, number_of_edges, is_directed=False)
    s = StructuralFunction(g)
    controller = DbController()
    controller.add_graph(g)
    controller.show_all_graphs()
    return web.Response(text=str(s))
