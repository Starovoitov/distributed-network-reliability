from sqlalchemy import Column, Integer, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Graph(DeclarativeBase):
    __tablename__ = "Graphs"

    id = Column("GraphId", Integer, primary_key=True)
    initial_vertex_index = Column("InitialVertexIndex", Integer)
    final_vertex_index = Column("FinalVertexIndex", Integer)
    is_directed = Column("IsDirected", Boolean)
    is_simple = Column("IsSimple", Boolean)
    graph_ml = Column("GraphML", Text)

    def __repr__(self):
        return f"Graph id: {self.id}"
