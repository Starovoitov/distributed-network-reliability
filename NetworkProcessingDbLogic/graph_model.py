from typing import List

from sqlalchemy import Column, Integer, Boolean, Text, select, delete
from sqlalchemy.orm import declarative_base

from NetworkProcessing.graphs import Graph

DeclarativeBase = declarative_base()


class GraphModel(DeclarativeBase):
    __tablename__ = "Graphs"

    id = Column("GraphId", Integer, primary_key=True)
    initial_vertex_index = Column("InitialVertexIndex", Integer)
    final_vertex_index = Column("FinalVertexIndex", Integer)
    is_directed = Column("IsDirected", Boolean)
    is_simple = Column("IsSimple", Boolean)
    graph_ml = Column("GraphML", Text)

    def __repr__(self):
        return f"Graph id: {self.id}"

    @classmethod
    async def add_graph(cls, graph_object: Graph) -> None:
        with cls.session.begin() as session:
            graph = GraphModel(
                initial_vertex_index=graph_object.initial_vertex_index,
                final_vertex_index=graph_object.final_vertex_index,
                is_directed=graph_object.is_directed,
                is_simple=graph_object.is_simple,
                graph_ml=graph_object.get_graphml(),
            )
            await session.add(graph)
            await session.commit()

    @classmethod
    async def get_all_graphs(cls) -> List[Graph]:
        with cls.session.begin() as session:
            graphs = await session.query(GraphModel).all()
        return graphs

    @classmethod
    async def get_graph_by_id(cls, graph_id: int):
        with cls.session.begin() as session:
            graph = await (
                session.execute(select(GraphModel).filter_by(id=graph_id))
                .scalars()
                .first()
            )
        return graph

    @classmethod
    async def count_stored_graphs(cls) -> int:
        with cls.session.begin() as session:
            graph_count = await session.query(GraphModel).count()
        return graph_count

    @classmethod
    async def delete_all_graphs(cls) -> None:
        with cls.session.begin() as session:
            await session.query(GraphModel).delete()
            await session.commit()

    @classmethod
    async def delete_graph_by_id(cls, graph_id: int) -> None:
        with cls.session.begin() as session:
            await session.execute(delete(GraphModel).where(GraphModel.id == graph_id))
            await session.commit()

    @classmethod
    async def is_graph_exists(cls, graph_id: int) -> bool:
        with cls.session.begin() as session:
            is_exists = await session.query(
                session.query(GraphModel).filter_by(id=graph_id).exists()
            ).scalar()
        return is_exists
