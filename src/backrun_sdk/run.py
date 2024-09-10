import importlib
import time


def run_task(data):
    start_at = time.perf_counter()

    module_name, func_name = data["func"].rsplit(".", 1)
    args = data.get("args") or []
    kwargs = data.get("kwargs") or {}

    result = None
    error = None
    try:
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        result = func(*args, **kwargs)
    except Exception as e:
        print("coming here")
        error = str(e)
    finally:
        end_at = time.perf_counter()
        duration = int((end_at - start_at) * 1000) + 1

    return dict(
        duration=duration,
        result=result,
        error=error,
    )
