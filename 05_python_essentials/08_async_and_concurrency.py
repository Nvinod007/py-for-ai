# Async: do many waiting jobs (API calls) at the same time.
# FastAPI and most modern LLM clients use this.

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

# %% Waiting one by one is slow
def fetch_slow(n):
    time.sleep(0.5)                       # pretend this is a network call
    return n * 10


start = time.perf_counter()
print([fetch_slow(i) for i in range(4)])
print(f"sequential: {time.perf_counter() - start:.1f}s")

# %% Threads: simple speed-up for waiting work
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(fetch_slow, range(4))))
print(f"threads: {time.perf_counter() - start:.1f}s")

# %% async / await
async def fetch(n):
    await asyncio.sleep(0.5)              # gives control back while waiting
    return n * 10


async def main():
    start = time.perf_counter()
    results = await asyncio.gather(*(fetch(i) for i in range(4)))
    print(results, f"async: {time.perf_counter() - start:.1f}s")



def run(coro):
    # Interactive windows already have a running event loop, so asyncio.run()
    # would fail there. Running it in a helper thread works everywhere.
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


run(main())
# In a normal script you would simply write: asyncio.run(main())

# %% Limiting how many run at once (be kind to APIs)
async def limited(semaphore, n):
    async with semaphore:
        await asyncio.sleep(0.2)
        return n


async def run_limited():
    semaphore = asyncio.Semaphore(2)
    results = await asyncio.gather(*(limited(semaphore, i) for i in range(6)))
    print(results)


run(run_limited())

# %% Timeouts and errors
async def maybe_slow():
    await asyncio.sleep(2)


async def with_timeout():
    try:
        await asyncio.wait_for(maybe_slow(), timeout=0.3)
    except asyncio.TimeoutError:
        print("took too long")


run(with_timeout())


async def risky(n):
    if n == 2:
        raise ValueError("bad item")
    return n


async def collect_errors():
    results = await asyncio.gather(*(risky(i) for i in range(4)), return_exceptions=True)
    print(results)


run(collect_errors())

# %% Producer / consumer with a queue
async def producer(queue):
    for i in range(3):
        await queue.put(i)
    await queue.put(None)


async def consumer(queue):
    while (item := await queue.get()) is not None:
        print("got", item)


async def pipeline():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))


run(pipeline())

# %% Rule of thumb
# Waiting on network/disk (API calls)   -> async or threads
# Heavy maths on the CPU                -> multiprocessing or NumPy
