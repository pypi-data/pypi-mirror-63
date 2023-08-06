from datetime import timedelta
from redis import Redis

from .template import RateLimiterBackend


ONE_SECOND = timedelta(seconds=1)
INCREMENT_SCRIPT = b"""
    local current
    current = tonumber(redis.call("incrby", KEYS[1], ARGV[2]))
    if current == tonumber(ARGV[2]) then
        redis.call("expire", KEYS[1], ARGV[1])
    end
    return current
"""


class RedisRateLimiterBackend(RateLimiterBackend):
    def __init__(self, client, default_expiry: timedelta = ONE_SECOND):
        self._client: Redis = client
        self._expiry = int(default_expiry.total_seconds())

    def increment_usage(
        self, key: str, expiry: timedelta = None, increment_by: int = 1
    ):
        expiry = int((expiry or self._expiry).total_seconds())
        current_usage = self._client.eval(
            INCREMENT_SCRIPT, 1, key, expiry, increment_by
        )

        return current_usage
