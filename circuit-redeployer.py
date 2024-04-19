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

async def redeploy_evc(client: httpx.AsyncClient, evc):
    response = await client.patch(f"{MEF_ELINE_API}/evc/{evc}/redeploy")
    if not response.is_success:
        print(f"Failed to redeploy EVC: {evc}")

async def redeploy_evcs(client: httpx.AsyncClient):
    response = await client.get(f"{MEF_ELINE_API}/evc/")
    if not response.is_success:
        print('Failed to get EVCs')
        return
    evc_dict = response.json()
    for batch in batched(
        [
            redeploy_evc(client, evc)
            for evc in evc_dict
        ], 
        5
    ):
        await asyncio.gather(
            *batch
        )
            
async def main():
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
    ) as client:
        await redeploy_evcs(client)

asyncio.run(main())
