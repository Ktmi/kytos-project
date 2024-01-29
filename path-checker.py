#!/usr/bin/env python

import asyncio
import aiohttp
import hashlib
import itertools

KYTOS_URL = 'http://localhost:8181'

KYTOS_API = f"/api"

PATHFINDER_API = f"{KYTOS_API}/kytos/pathfinder/v3"



async def get_path(
    session: aiohttp.ClientSession,
    **kwargs
):
    async with session.post(
        PATHFINDER_API + "/",
        json=kwargs
    ) as response:
        if response.ok:
            data = await response.json()
            print(data)


            return True
        return False
    

async def main():
    async with aiohttp.ClientSession(KYTOS_URL) as session:
        await get_path(
            session,
            source="00:00:00:00:00:00:01:01:1",
            destination="00:00:00:00:00:00:01:03:1",
            mandatory_metrics={
                "not_ownership": "border"
            }
        )

asyncio.run(main())
