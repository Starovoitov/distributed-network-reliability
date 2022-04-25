from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from NetworkProcessing.graphs import Graph
from NetworkProcessingDbLogic.graph_model import DeclarativeBase, Graph as GraphModel


class DbController:
    USER = "postgres"
    PASSWORD = "test"
    HOST = "LOCALHOST"
    PORT = 5432
    DB = "networks"

    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
        )
        DeclarativeBase.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_graph(self, graph_object: Graph):
        graph = GraphModel(
            initial_vertex_index=graph_object.initial_vertex_index,
            final_vertex_index=graph_object.final_vertex_index,
            is_directed=graph_object.is_directed,
            is_simple=graph_object.is_simple,
            graph_ml=graph_object.get_graphml(),
        )
        self.session.add(graph)
        self.session.commit()

    def show_all_graphs(self):
        print(self.session.query(GraphModel).count())
        for graph in self.session.query(GraphModel):
            print(graph)
