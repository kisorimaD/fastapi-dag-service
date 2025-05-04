import queue
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import GraphCreate, GraphReadResponse, GraphCreateResponse, AdjacencyListResponse
from fastapi import HTTPException
from models import Graph, Node, Edge


async def create_graph(db: AsyncSession, graph: GraphCreate) -> GraphCreateResponse:
    adj_list = dict()

    for node in graph.nodes:
        adj_list[node.name] = []

    for edge in graph.edges:
        adj_list[edge.source].append(edge.target)

    visited_nodes = set()

    for node in graph.nodes:
        node_name = node.name

        if not node_name in visited_nodes:
            q = queue.Queue()

            q.put(node_name)

            while (not q.empty()):
                v = q.get()

                for v_neighbour in adj_list[v]:
                    if v_neighbour in visited_nodes:
                        raise HTTPException(422, "Validation Error")

                    visited_nodes.add(v_neighbour)
                    q.put(v_neighbour)

    graph_db = Graph()
    db.add(graph_db)

    await db.flush()

    nodes_entity = dict()

    for node in graph.nodes:
        node_db = Node(
            name=node.name,
            graph_id=graph_db.id
        )
        db.add(node_db)
        nodes_entity[node.name] = node_db

    await db.flush()

    for edge in graph.edges:
        edge_db = Edge(
            source_id=nodes_entity[edge.source].id,
            target_id=nodes_entity[edge.target].id,
            graph_id=graph_db.id
        )

    await db.commit()

    return GraphCreateResponse(graph_db.id)


async def get_graph(db: AsyncSession, graph_id: int) -> GraphReadResponse:
    query = select(Graph).where(Graph.id == graph_id).scalar()

    graph_db = await db.execute(query)

    if graph_db is None:
        raise HTTPException(404, "Graph entity not found")

    return GraphReadResponse(
        {
        "nodes": graph_db.nodes,
        "edegs": graph_db.edges,
        }
    )


async def get_adj_list(db: AsyncSession, graph_id: int, transpose: bool = False) -> AdjacencyListResponse:
    regular_graph = await get_graph(db, graph_id)

    name_by_id = dict()
    adj_list = dict()

    for node in regular_graph["nodes"]:
        adj_list[node.id] = node.name
        adj_list[node.id] = []

    for edge in regular_graph["edges"]:
        if not transpose:
            adj_list[name_by_id[edge.source_id]].append(
                name_by_id[edge.target_id])
        else:
            adj_list[name_by_id[edge.target_id]].append(
                name_by_id[edge.source_id])

    return AdjacencyListResponse(
        {
            "id": graph_id,
            "nodes": regular_graph["nodes"],
            "edges": adj_list
        }
    )


async def delete_node(db: AsyncSession, graph_id: int, node_name: str):
    query = select(Node).where(Node.graph_id == graph_id,
                               Node.name == node_name).scalar()

    node_db = await db.execute(query)

    if node_db is None:
        raise HTTPException(404, "Graph entity not found")

    await db.delete(node_db)

    await db.commit()

    return None
