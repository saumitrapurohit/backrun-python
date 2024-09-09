import importlib
import inspect

import orjson
from django.apps import apps
from django.http import HttpResponse

from ..run import run_task


def _sync():
    tasklist = set()
    for app in apps.get_app_configs():
        try:
            tasks_module = importlib.import_module(f"{app.module.__name__}.tasks")
        except ModuleNotFoundError:
            continue

        tasklist.update(
            [
                func
                for name, func in inspect.getmembers(tasks_module)
                if inspect.isfunction(func) and getattr(func, "is_backrun_task", None)
            ]
        )

    return (
        sorted(
            [dict(name=task.name, cron=task.cron) for task in tasklist],
            key=lambda x: x["name"],
        )
        if tasklist
        else []
    )


def serve(request, *a, **kw):
    if request.method != "POST":
        return HttpResponse("ok", content_type="text/plain", status=200)

    if not request.body:
        return HttpResponse("bad request", content_type="text/plain", status=400)

    data = orjson.loads(request.body)
    request_type = data.pop("type", "task")
    if request_type == "sync":
        result = _sync()
    else:
        result = run_task(data)

    return HttpResponse(
        content=orjson.dumps(result),
        content_type="application/json",
        status=200,
    )


__all__ = ["serve"]
