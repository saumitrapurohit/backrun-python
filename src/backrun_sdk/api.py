from .client import Client

_active_client = None


def init(*args, **kwargs):
    client = Client(*args, **kwargs)

    global _active_client
    _active_client = client


def get_active_client():
    return _active_client


__all__ = ["init", "get_active_client"]
