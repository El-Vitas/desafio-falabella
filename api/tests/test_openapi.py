from fastapi.testclient import TestClient


def responses_of(client: TestClient, path: str) -> set[str]:
    return set(client.get("/openapi.json").json()["paths"][path]["get"]["responses"])


def test_the_docs_list_the_errors_the_detail_really_returns(client: TestClient) -> None:
    assert responses_of(client, "/items/{pokemon_id}") == {"200", "400", "404", "500", "503"}


def test_the_docs_list_the_errors_of_the_queries(client: TestClient) -> None:
    assert responses_of(client, "/queries/top-trainers") == {"200", "500", "503"}


def test_the_docs_do_not_announce_a_422_the_api_never_returns(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()

    statuses = {
        status
        for path_item in schema["paths"].values()
        for operation in path_item.values()
        for status in operation["responses"]
    }

    assert "422" not in statuses
    assert "HTTPValidationError" not in schema["components"]["schemas"]
