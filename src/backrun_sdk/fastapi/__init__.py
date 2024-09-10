import orjson
from fastapi import Request, Response
from ..run import run_task


def _sync():
    return []


async def serve(request: Request):
    if request.method != "POST":
        return Response("ok", status_code=200)

    body = await request.body()
    if not body:
        return Response("bad request", status_code=400)

    data = orjson.loads(body)
    request_type = data.pop("type", "task")
    if request_type == "sync":
        result = _sync()
    else:
        result = run_task(data)

    return Response(
        content=orjson.dumps(result),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
