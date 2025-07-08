import json
import asyncio
import random
import string
import urllib.error
import urllib.parse
import urllib.request
from contextlib import closing
from itertools import cycle

import aiohttp
import numpy as np
import pylab as py


py.rcParams.update({"font.size": 16})
markers = cycle("h*o>Dxsp8")
linestyles = cycle(["-", ":", "--", "-."])


def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


async def process(session, url):
    try:
        response = await session.get(url)
        return len(await response.text())
    except TimeoutError:
        print("Timeout Error with request:", url)
        return 0


async def run_experiment(base_url, num_iter, chunk_size=100):
    connector = aiohttp.TCPConnector(limit=chunk_size)
    tasks = []
    timeout = aiohttp.ClientTimeout(total=600000)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        async with asyncio.TaskGroup() as tg:
            for url in generate_urls(base_url, num_iter):
                task = tg.create_task(process(session, url))
                tasks.append(task)
    response_size = sum(task.result() for task in tasks)
    return response_size


if __name__ == "__main__":
    try:
        data = json.load(open("parallel_requests.json"))
    except IOError:
        import time

        num_iter = 500
        data = {}
        for delay in range(50, 1000, 250):
            base_url = f"http://127.0.0.1:8080/add?name=concurrency_test&delay={delay}&"
            data[delay] = []
            for parallel_requests in range(1, num_iter, 25):
                start = time.time()
                result = asyncio.run(
                    run_experiment(base_url, num_iter, parallel_requests)
                )
                t = time.time() - start
                print(f"{delay},{parallel_requests},{t}")
                data[delay].append((parallel_requests, t))

        json.dump(data, open("parallel_requests.json", "w+"))
    print("plotting")
    py.figure()
    for delay, values in data.items():
        values = np.asarray(values)
        py.plot(
            values[:, 0],
            values[:, 1],
            label=f"{delay}ms request time",
            linestyle=next(linestyles),
            marker=next(markers),
            markersize=12,
            linewidth=4,
        )

    py.axvline(x=100, alpha=0.5, c="r")
    ax = py.gca()
    ax.set_yscale("log")

    py.xlabel("Number of concurrent requests")
    py.ylabel("Time to process 500 http requests (s)")
    py.title("Finding the right number of concurrent requests")
    py.legend()

    py.savefig("images/parallel_requests.png")
