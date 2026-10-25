# Async: do many waiting jobs (API calls) at the same time.
# FastAPI and most modern LLM clients use this.
# Each line has a short comment saying WHAT it is.

import asyncio  # asyncio: Python's tool for running waiting jobs together
import time  # time: clock and sleep tools
from concurrent.futures import ThreadPoolExecutor  # ThreadPoolExecutor: runs functions in several threads (parallel workers)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Waiting one by one is slow
def fetch_slow(n):  # def: makes a function
    time.sleep(0.5)                       # sleep(s): pauses s seconds; pretend this is a network call
    return n * 10  # return: sends a value back


start = time.perf_counter()  # perf_counter(): precise clock in seconds
print([fetch_slow(i) for i in range(4)])  # [.. for ..]: list comprehension; range(4) = 0..3; print: shows it
print(f"sequential: {time.perf_counter() - start:.1f}s")  # f-string puts values in text; :.1f = 1 decimal

# %% Threads: simple speed-up for waiting work
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:  # with: auto-cleans up at the end; max_workers=4: up to 4 jobs at once
    print(list(pool.map(fetch_slow, range(4))))  # pool.map(f, items): runs f on each item in parallel; list(): collects results
print(f"threads: {time.perf_counter() - start:.1f}s")

# %% async / await
async def fetch(n):  # async def: a function that can pause while waiting
    await asyncio.sleep(0.5)              # await: pause here until done; asyncio.sleep: wait without blocking others
    return n * 10


async def main():
    start = time.perf_counter()
    results = await asyncio.gather(*(fetch(i) for i in range(4)))  # gather(...): runs all jobs together, returns results in order; *(...) spreads them as arguments
    print(results, f"async: {time.perf_counter() - start:.1f}s")



def run(coro):  # coro = an async function call waiting to be run
    # Interactive windows already have a running event loop, so asyncio.run()
    # would fail there. Running it in a helper thread works everywhere.
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()  # submit(f, x): runs f(x) in a thread; asyncio.run: runs an async function to the end; result(): waits for the answer


run(main())
# In a normal script you would simply write: asyncio.run(main())

# %% Rule of thumb
# Waiting on network/disk (API calls)   -> async or threads
# Heavy maths on the CPU                -> multiprocessing or NumPy

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Limiting how many run at once (be kind to APIs)
async def limited(semaphore, n):
    async with semaphore:  # async with: like with, but for async things; semaphore lets only a few in at once
        await asyncio.sleep(0.2)
        return n


async def run_limited():
    semaphore = asyncio.Semaphore(2)  # Semaphore(2): allows at most 2 jobs at the same time
    results = await asyncio.gather(*(limited(semaphore, i) for i in range(6)))
    print(results)


run(run_limited())

# %% Timeouts and errors
async def maybe_slow():
    await asyncio.sleep(2)


async def with_timeout():
    try:  # try: run code that might fail
        await asyncio.wait_for(maybe_slow(), timeout=0.3)  # wait_for(job, timeout=s): gives up after s seconds
    except asyncio.TimeoutError:  # except: runs if that error happened
        print("took too long")


run(with_timeout())


async def risky(n):
    if n == 2:  # if: runs block when the test is True
        raise ValueError("bad item")  # raise: throws an error on purpose
    return n


async def collect_errors():
    results = await asyncio.gather(*(risky(i) for i in range(4)), return_exceptions=True)  # return_exceptions=True: errors become results instead of crashing
    print(results)


run(collect_errors())

# %% Producer / consumer with a queue
async def producer(queue):
    for i in range(3):  # for: repeats for each number
        await queue.put(i)  # put(x): adds x to the queue
    await queue.put(None)  # None = "nothing"; used here as a "finished" signal


async def consumer(queue):
    while (item := await queue.get()) is not None:  # while: repeats while True; := saves a value and tests it at once; get(): takes the next item
        print("got", item)


async def pipeline():
    queue = asyncio.Queue()  # Queue(): a line of items passed between jobs
    await asyncio.gather(producer(queue), consumer(queue))  # run both jobs together


run(pipeline())
