import orjson
from flask import request
from flask import Response

from ..run import run_task


def _sync():
    return []


def serve(*a, **kw):
    if request.method != "POST":
        return Response("ok", content_type="text/plain", status=200)

    if not request.data:
        return Response("bad request", content_type="text/plain", status=400)

    data = orjson.loads(request.data)
    request_type = data.pop("type", "task")
    if request_type == "sync":
        result = _sync()
    else:
        result = run_task(data)

    return Response(
        response=orjson.dumps(result),
        content_type="application/json",
        status=200,
    )


serve.provide_automatic_options = False
serve.methods = ("POST",)
