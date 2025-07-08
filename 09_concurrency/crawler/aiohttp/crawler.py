import asyncio
import random
import string

import aiohttp


def generate_urls(base_url, num_urls):
    """
    We add random characters to the end of the URL to break any caching
    mechanisms in the requests library or the server
    """
    for _ in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


async def process(session, url):
    async with session.get(url) as response:
        return len(await response.text())


async def run_experiment(base_url, num_iter=1000):
    tasks = []
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:  # <1>
            for url in generate_urls(base_url, num_iter):
                coro = process(session, url)
                task = tg.create_task(coro)
                tasks.append(task)
    response_size = sum(task.result() for task in tasks)  # <2>
    return response_size


if __name__ == "__main__":
    import time

    delay = 100
    num_iter = 1000
    base_url = f"http://127.0.0.1:8080/add?name=aiohttp&delay={delay}&"
    experiment = run_experiment(base_url, num_iter)

    start = time.time()
    result = asyncio.run(experiment)
    end = time.time()
    print(f"Result: limit: {result}, Time: {end - start}")
