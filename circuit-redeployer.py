#!/usr/bin/env python

import asyncio
import aiohttp
import itertools

KYTOS_URL = 'http://localhost:8181'

KYTOS_API = f"/api"

MEF_ELINE_API = f"{KYTOS_API}/kytos/mef_eline/v2"

def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch

async def redeploy_evc(session, evc):
    async with session.patch(MEF_ELINE_API + f"/evc/{evc}/redeploy") as response:
        if not response.ok:
            print(f"Failed to redeploy EVC: {evc}")

async def redeploy_evcs(session):
    async with session.get(MEF_ELINE_API+"/evc/") as response:
        if not response.ok:
            print('Failed to get EVCs')
            return
        evc_dict = await response.json()
        for batch in batched(
            [
                redeploy_evc(session, evc)
                for evc in evc_dict
            ], 
            5
        ):
            await asyncio.gather(
                *batch
            )
            
async def main():
    async with aiohttp.ClientSession(KYTOS_URL) as session:
        await redeploy_evcs(session)

asyncio.run(main())