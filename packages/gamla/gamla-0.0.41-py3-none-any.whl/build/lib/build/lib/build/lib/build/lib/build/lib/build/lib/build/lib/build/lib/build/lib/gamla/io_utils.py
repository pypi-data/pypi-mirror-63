import asyncio
import datetime
import functools
import logging
import time
from typing import Text

import requests
import requests.adapters
import toolz
from requests.packages.urllib3.util import retry

from gamla import functional


def _time_to_readable(time_s: float):
    return datetime.datetime.fromtimestamp(time_s)


def _request_id(name, args, kwargs) -> Text:
    return f"{name}, args: {args}, kwargs: {kwargs}"


def _async_timeit(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        req_id = _request_id(f.__name__, args, kwargs)
        start = time.time()
        logging.info(f"{req_id} started at {_time_to_readable(start)}")
        result = await f(*args, **kwargs)
        finish = time.time()
        elapsed = finish - start
        logging.info(
            f"{req_id} finished at {_time_to_readable(finish)}, took {elapsed}"
        )
        return result

    return wrapper


def timeit(f):
    if asyncio.iscoroutinefunction(f):
        return _async_timeit(f)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        req_id = _request_id(f.__name__, args, kwargs)
        start = time.time()
        logging.info(f"{req_id} started at {_time_to_readable(start)}")
        result = f(*args, **kwargs)
        finish = time.time()
        elapsed = finish - start
        logging.info(
            f"{req_id} finished at {_time_to_readable(finish)}, took {elapsed:.2f}"
        )
        return result

    return wrapper


def requests_with_retry(retries: int = 3) -> requests.Session:
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        max_retries=retry.Retry(
            total=retries, backoff_factor=0.1, status_forcelist=(500, 502, 504)
        )
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def batch_calls(f, timeout=20):
    """Batches single call into one request.

    Turns `f`, a function that gets a `tuple` of independent requests, into a function
    that gets a single request.
    """
    queue = {}

    async def make_call():
        await asyncio.sleep(0.1)
        if not queue:
            return
        promises = tuple(queue.values())
        requests = tuple(queue.keys())
        queue.clear()
        try:
            for promise, result in zip(promises, await f(requests)):
                # We check for possible mid-exception or timeouts.
                if promise.done() or promise.cancelled():
                    continue
                promise.set_result(result)
        except Exception as exception:
            for promise in promises:
                # We check for possible mid-exception or timeouts.
                if promise.done() or promise.cancelled():
                    continue
                promise.set_exception(exception)

    async def wrapped(hashable_input):
        if hashable_input in queue:
            return await asyncio.wait_for(queue[hashable_input], timeout=timeout)
        async_result = asyncio.Future()
        # Check again because of context switch due to the creation of `asyncio.Future`.
        # TODO(uri): Make sure this is needed.
        if hashable_input in queue:
            return await asyncio.wait_for(queue[hashable_input], timeout=timeout)
        queue[hashable_input] = async_result
        asyncio.create_task(make_call())
        return await asyncio.wait_for(async_result, timeout=timeout)

    return wrapped


def queue_identical_calls(f):
    # Note that pending grows infinitely large, this assumes we cache the results
    # anyway after this decorator, so we at most double the memory consumption.
    pending = {}

    @functools.wraps(f)
    async def wrapped(*args, **kwargs):
        key = functional.make_call_key(args, kwargs)
        if key not in pending:
            pending[key] = asyncio.Future()
            pending[key].set_result(await f(*args, **kwargs))
        return await asyncio.wait_for(pending[key], timeout=20)

    return wrapped


@toolz.curry
def athrottle(limit, f):
    semaphore = asyncio.Semaphore(limit)

    @functools.wraps(f)
    async def wrapped(*args, **kwargs):
        async with semaphore:
            return await f(*args, **kwargs)

    return wrapped


@toolz.curry
async def throttled_amap(f, it, limit):
    return await functional.amap(athrottle(limit, f), it)
