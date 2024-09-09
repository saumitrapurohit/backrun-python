import logging
import threading
from collections import deque
from datetime import datetime, timezone

import httpx
import orjson

from .constants import VERSION

logger = logging.getLogger("backrun")


class Client:
    def __init__(
        self,
        api_key=None,
        api_secret=None,
        api_url="https://api.backrun.io",
        always_eager=False,
        batch=False,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = api_url
        self.always_eager = always_eager
        self.batch = batch

        self._delay = 0.01
        self._reqs = deque()
        self._timer_thread = None
        self._transport = httpx.Client(
            http2=True,
            follow_redirects=False,
            timeout=30,
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "backrun/py-%s" % VERSION,
            },
        )

    def submit(self, func, args, kwargs):
        req = dict(
            func=func,
            sent_at=datetime.now(timezone.utc).isoformat(),
        )

        if args:
            req["args"] = args
        if kwargs:
            req["kwargs"] = kwargs

        if not self.batch:
            self._send(req)
        else:
            self._reqs.append(req)

            # Start the timer thread if it's not already running
            if not self._timer_thread or not self._timer_thread.is_alive():
                self._timer_thread = threading.Timer(self._delay, self.send_batched)
                self._timer_thread.start()

    def _send(self, data):
        try:
            content = orjson.dumps(data)
        except orjson.JSONDecodeError:
            logger.error(
                "enqueue.failed: invalid task args and kwargs",
            )
            return

        try:
            logging.disable(logging.FATAL)
            response = self._transport.post("/v1/enqueue", content=content)
            if response.status_code not in [200, 202]:
                raise Exception("did not accept")
            logging.disable(logging.NOTSET)
        except Exception as exc:
            logging.disable(logging.NOTSET)
            logger.error("enqueue.failed: %s", str(exc))

    def send_batched(self):
        tasklist = []
        while len(self._reqs) > 0:
            tasklist.append(self._reqs.popleft())

        self._send(tasklist)
