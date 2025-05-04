from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    graph_id = Column(Integer, ForeignKey('graphs.id'))

    __table_args__ = (
        UniqueConstraint('name', 'graph_id')
    )

    edges_in = relationship(
        "Edge", foreign_keys="edges.source_id", back_populates="source_node", cascade="all, delete-orphan")
    edges_out = relationship(
        "Edge", foreign_keys="edges.target_id", back_populates="target_node", cascade="all, delete-orphan")

    graph = relationship("Graph", back_populates="graps.id")


class Edge(Base):
    __tablename__ = 'edges'
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey('nodes.id'))
    target_id = Column(Integer, ForeignKey('nodes.id'))

    graph_id = Column(Integer, ForeignKey('graphs.id'))

    source_node = relationship("Node", foreign_keys=[
                               source_id], back_populates="edges_in")
    target_node = relationship("Node", foreign_keys=[
                               target_id], back_populates="edges_out")

    graph = relationship("Graph", back_populates="graps.id")


class Graph(Base):
    __tablename__ = 'graphs'
    id = Column(Integer, primary_key=True, index=True)

    nodes = relationship("Node", back_populates="graph",
                         cascade="all, delete-orphan")
    edges = relationship("Edge", back_populates="graph",
                         cascade="all, delete-orphan")
