from pydantic import BaseModel, Field

MAX_NODE_NAME_LENGTH = 255
node_name_pattern = r'^[a-zA-Z]+$'


class Node(BaseModel):
    name: str = Field(max_length=MAX_NODE_NAME_LENGTH,
                      pattern=node_name_pattern,)


class Edge(BaseModel):
    source: str = Field(max_length=MAX_NODE_NAME_LENGTH,
                        pattern=node_name_pattern,)

    target: str = Field(max_length=MAX_NODE_NAME_LENGTH,
                        pattern=node_name_pattern,)


class GraphCreate(BaseModel):
    nodes: list[Node]
    edges: list[Edge]


class GraphCreateResponse(BaseModel):
    id: int


class GraphReadResponse(BaseModel):
    id: int
    nodes: list[Node]
    edges: list[Edge]


class AdjacencyListResponse(BaseModel):
    adjacency_list: dict[str, list[str]]


class ErrorResponse(BaseModel):
    message: str


class ValidationError(BaseModel):
    loc: list[str]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    detail: list[ValidationError] = None
