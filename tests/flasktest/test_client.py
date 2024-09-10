from datetime import datetime, timezone

import orjson
from mock import patch

from .app import author_count


def test_sync_call():
    assert author_count() == 1


@patch("httpx.Client.post")
@patch("backrun_sdk.client.datetime")
def test_delay_simple(mock_now, mock_post):
    now = datetime.now(timezone.utc)
    mock_now.now.return_value = now

    author_count.delay()
    mock_post.assert_called_once_with(
        "/v1/enqueue",
        content=orjson.dumps(
            {
                "func": "tests.flasktest.app.author_count",
                "sent_at": now.isoformat(),
            }
        ),
    )


@patch("httpx.Client.post")
@patch("backrun_sdk.client.datetime")
def test_delay_with_args(mock_now, mock_post):
    now = datetime.now(timezone.utc)
    mock_now.now.return_value = now
    author_count.delay(1, 2, is_published=True)
    mock_post.assert_called_once_with(
        "/v1/enqueue",
        content=orjson.dumps(
            {
                "func": "tests.flasktest.app.author_count",
                "sent_at": now.isoformat(),
                "args": [1, 2],
                "kwargs": {"is_published": True},
            }
        ),
    )


@patch("httpx.Client.post")
@patch("backrun_sdk.client.datetime")
def test_apply_async_simple(mock_now, mock_post):
    now = datetime.now(timezone.utc)
    mock_now.now.return_value = now

    author_count.apply_async()
    mock_post.assert_called_once_with(
        "/v1/enqueue",
        content=orjson.dumps(
            {
                "func": "tests.flasktest.app.author_count",
                "sent_at": now.isoformat(),
            }
        ),
    )


@patch("httpx.Client.post")
@patch("backrun_sdk.client.datetime")
def test_apply_async_with_args(mock_now, mock_post):
    now = datetime.now(timezone.utc)
    mock_now.now.return_value = now

    author_count.apply_async(args=(1, 2), kwargs={"is_published": True})
    mock_post.assert_called_once_with(
        "/v1/enqueue",
        content=orjson.dumps(
            {
                "func": "tests.flasktest.app.author_count",
                "sent_at": now.isoformat(),
                "args": [1, 2],
                "kwargs": {"is_published": True},
            }
        ),
    )
