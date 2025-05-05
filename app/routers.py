from fastapi import APIRouter, status
from .schemas import GraphReadResponse, GraphCreateResponse, AdjacencyListResponse, GraphCreate
from .crud import db_create_graph, db_get_graph, db_get_adj_list, db_delete_node
from .deps import Session
router = APIRouter(prefix="/api/graph")


@router.post("/")
async def create_graph(db: Session, new_graph: GraphCreate) -> GraphCreateResponse:
    result_graph_id = await db_create_graph(db, new_graph)

    return result_graph_id


@router.get("/{graph_id}")
async def read_graph(db: Session, graph_id: int) -> GraphReadResponse:
    result_graph = await db_get_graph(db, graph_id)

    return result_graph


@router.get("/{graph_id}/adjacency_list")
async def get_adjacency_list(db: Session, graph_id: int) -> AdjacencyListResponse:
    result_adj_list = await db_get_adj_list(db, graph_id, transpose=False)

    return result_adj_list


@router.get("/{graph_id}/reverse_adjacency_list")
async def get_reverse_adjacency_list(db: Session, graph_id: int) -> AdjacencyListResponse:
    result_adj_list = await db_get_adj_list(db, graph_id, transpose=True)

    return result_adj_list


@router.delete("/{graph_id}/node/{node_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(db: Session, graph_id: int, node_name: str):
    await db_delete_node(db, graph_id, node_name)
    return None
