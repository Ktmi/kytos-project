#!/usr/bin/env python

import asyncio
import httpx
import hashlib
import itertools

KYTOS_URL = 'http://localhost:8181'

KYTOS_API = f"{KYTOS_URL}/api"

PATHFINDER_API = f"{KYTOS_API}/kytos/pathfinder/v3"



async def get_path(
    client: httpx.AsyncClient,
    **kwargs
):
    response = await client.post(
        PATHFINDER_API + "/",
        json=kwargs
    )
    if response.is_success:
        data = response.json()
        print(data)


        return True
    return False
    

async def main():
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
    ) as client:
        await get_path(
            client,
            source="00:00:00:00:00:00:01:01:1",
            destination="00:00:00:00:00:00:01:03:1",
            mandatory_metrics={
                "not_ownership": "border"
            }
        )

asyncio.run(main())
