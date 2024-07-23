#!/usr/bin/env python

import asyncio
import httpx
import itertools

KYTOS_URL = 'http://localhost:8181'

KYTOS_API = f"{KYTOS_URL}/api"

MEF_ELINE_API = f"{KYTOS_API}/kytos/mef_eline/v2"

def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch

async def delete_evc(client: httpx.AsyncClient, evc):
    response = await client.delete(f"{MEF_ELINE_API}/evc/{evc}")
    if not response.is_success:
        print(f"Failed to delete EVC: {evc}")

async def worker(client, queue):
    while True:
        evc = await queue.get()

        await delete_evc(client, evc)

        queue.task_done()

async def delete_evcs(client: httpx.AsyncClient):
    response = await client.get(MEF_ELINE_API+"/evc/")
    if not response.is_success:
        print('Failed to get EVCs')
        return
    evc_dict = response.json()

    queue = asyncio.Queue()

    for evc in evc_dict:
        queue.put_nowait(evc)

    worker_tasks = []
    
    for i in range(20):
        task = asyncio.create_task(worker(client, queue))
        worker_tasks.append(task)

    await queue.join()

    for task in worker_tasks:
        task.cancel()

    await asyncio.gather(*worker_tasks, return_exceptions=True)
        
async def main():
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0)
    ) as client:
        await delete_evcs(client)

asyncio.run(main())
