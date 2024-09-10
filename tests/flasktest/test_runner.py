from mock import patch
from .app import app


@patch("tests.flasktest.app.author_count")
def test_run_task(mock_author_count):
    mock_author_count.return_value = 1

    client = app.test_client()
    resp = client.post(
        path="/backrun/",
        json={
            "func": "tests.flasktest.app.author_count",
            "args": [1, 2],
            "kwargs": {"is_published": True},
        },
    )
    mock_author_count.assert_called_once()
    mock_author_count.assert_called_with(1, 2, is_published=True)
    assert resp.status_code == 200
    response = resp.json
    assert response["result"] == 1
    assert response["duration"] > 0
    assert response["error"] is None


def test_run_non_existing_task():
    client = app.test_client()
    resp = client.post(
        path="/backrun/",
        json={
            "func": "tests.flasktest.app._random_non_existing_task_",
            "args": [1, 2],
            "kwargs": {"is_published": True},
        },
    )
    assert resp.status_code == 200
    response = resp.json
    assert response["result"] is None
    assert response["duration"] > 0
    assert "has no attribute '_random_non_existing_task_'" in response["error"]


def test_run_exception_raiser():
    client = app.test_client()
    resp = client.post(
        "/backrun/",
        json={"func": "tests.flasktest.app.exception_raiser"},
    )
    assert resp.status_code == 200
    response = resp.json
    assert response["result"] is None
    assert response["duration"] > 0
    assert "This is an exception from exception_raiser" in response["error"]
