from fastapi.testclient import TestClient
from itertools import combinations
from httpx import AsyncClient


def post_graph(test_client: TestClient, nodes: list[str], edges: list[tuple[str, str]]) -> int:

    response = test_client.post(
        "/api/graph/",
        json={
            "nodes": [{"name": node} for node in nodes],
            "edges": [{"source": source, "target": target} for source, target in edges]
        }
    )
    print({
        "nodes": [{"name": node} for node in nodes],
        "edges": [{"source": source, "target": target} for source, target in edges]
    })

    return response


def name_range(n: int):
    now = "a"

    for i in range(n):
        yield now

        j = len(now) - 1
        while j >= 0:
            if now[j] == "z":
                now = now[:j] + "a" + now[j + 1:]
                j -= 1
            else:
                now = now[:j] + chr(ord(now[j]) + 1) + now[j + 1:]
                break

        if j < 0:
            now = "a" + now


def test_simple_graph(test_client: TestClient):
    response = post_graph(test_client, ["a", "b", "c"], [("a", "b")])

    assert response.status_code == 200


def test_graph_with_cycle(test_client: TestClient):
    response = post_graph(test_client, ["a", "b", "c"], [
                          ("a", "b"), ("b", "c"), ("c", "a")])

    assert response.status_code == 422
    assert response.json() == {"detail": "Graph is not DAG"}


def test_graph_with_duplicate_edges(test_client: TestClient):
    response = post_graph(test_client, ["a", "b", "c"], [
                          ("a", "b"), ("b", "c"), ("a", "b")])

    assert response.status_code == 422
    assert response.json() == {
        "detail": "There are duplicate edges in the graph"}


def test_disconnected_graph(test_client: TestClient):
    response = post_graph(test_client, ["a", "b", "c", "d"], [])

    assert response.status_code == 200


def test_nonexistent_node(test_client: TestClient):
    response = post_graph(test_client, ["a", "b", "c"], [
                          ("a", "b"), ("b", "d")])

    assert response.status_code == 422
    assert response.json() == {"detail": "Node d not found in the graph"}


def test_graph_with_no_nodes(test_client: TestClient):
    response = post_graph(test_client, [], [])

    assert response.status_code == 422
    assert response.json() == {"detail": "Graph must have at least one node"}


def test_big_cycle_with_multiple_edges(test_client: TestClient):
    names = list(name_range(100))
    response = post_graph(test_client, names, [
        (str(names[i]), str(names[i + 1])) for i in range(len(names) - 1)] + [(str(names[-1]), str(names[0]))])

    assert response.status_code == 422
    assert response.json() == {"detail": "Graph is not DAG"}


def test_big_acyclic_graph_with_multiple_edges(test_client: TestClient):
    names = list(name_range(100))
    edges = [(name1, name2) for name1, name2 in combinations(names, 2)]
    response = post_graph(test_client, names, edges)

    assert response.status_code == 200
