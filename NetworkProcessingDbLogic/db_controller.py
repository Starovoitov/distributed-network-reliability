from typing import List

from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker

from NetworkProcessing.graphs import Graph
from NetworkProcessingDbLogic.graph_model import DeclarativeBase
from NetworkProcessingDbLogic.graph_model import Graph as GraphModelObject


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
        self.session = sessionmaker(bind=self.engine)

    def add_graph(self, graph_object: Graph) -> None:
        with self.session.begin() as session:
            graph = GraphModelObject(
                initial_vertex_index=graph_object.initial_vertex_index,
                final_vertex_index=graph_object.final_vertex_index,
                is_directed=graph_object.is_directed,
                is_simple=graph_object.is_simple,
                graph_ml=graph_object.get_graphml(),
            )
            session.add(graph)
            session.commit()

    def get_all_graphs(self) -> List[GraphModelObject]:
        with self.session.begin() as session:
            graphs = session.query(GraphModelObject).all()
        return graphs

    def get_graph_by_id(self, graph_id: int) -> GraphModelObject:
        with self.session.begin() as session:
            graph = (
                session.execute(select(GraphModelObject).filter_by(id=graph_id))
                .scalars()
                .first()
            )
        return graph

    def count_stored_graphs(self) -> int:
        with self.session.begin() as session:
            graph_count = session.query(GraphModelObject).count()
        return graph_count

    def delete_all_graphs(self) -> None:
        with self.session.begin() as session:
            session.query(GraphModelObject).delete()
            session.commit()

    def delete_graph_by_id(self, graph_id: int) -> None:
        with self.session.begin() as session:
            session.execute(
                delete(GraphModelObject).where(GraphModelObject.id == graph_id)
            )
            session.commit()

    def is_graph_exists(self, graph_id: int) -> bool:
        with self.session.begin() as session:
            is_exists = session.query(
                session.query(GraphModelObject).filter_by(id=graph_id).exists()
            ).scalar()
        return is_exists
