from __future__ import annotations
from typing import Optional
import redis
from time import sleep, time_ns
import json
import pkg_resources


class SingletonMeta(type):
    _instance: Optional[Singleton] = None

    def __call__(self, **kwargs) -> Singleton:
        if self._instance is None:
            self._instance = super().__call__(**kwargs)
        return self._instance


class RateLimitHandler(metaclass=SingletonMeta):
    def __init__(self, **kwargs):
        self.r = redis.Redis(**kwargs)
        # ping to be sure the connection is alive
        self.r.ping()

    def wait_slot(self, rate_limits: list, api_id: str = None):
        lua = pkg_resources.resource_filename('tartaruga', 'tartaruga.lua')
        with open(lua, 'r') as fp:
            self.r.luascript = self.r.register_script(fp.read())

        wait_time = self.r.luascript(args=[json.dumps(rate_limits),
                                     str(time_ns()),
                                     api_id])
        sleep(float(wait_time) / 1000)


def rate_limit(host: str = None, port: int = 6379, password: str = None,
               limits: list = None, api_id: str = None):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            RateLimitHandler(host=host,
                             port=port,
                             password=password).wait_slot(rate_limits=limits,
                                                          api_id=api_id)
            result = func(*args, **kwargs)
            return result
        return inner_wrapper
    return wrapper
