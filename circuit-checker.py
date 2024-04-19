#!/usr/bin/env python

import asyncio
import httpx
import hashlib

KYTOS_URL = 'http://localhost:8181'

KYTOS_API = f"{KYTOS_URL}/api"

MEF_ELINE_API = f"{KYTOS_API}/kytos/mef_eline/v2"

class LinkID(str):
    """Link Identifier"""

    def __new__(cls, interface_a, interface_b):
        raw_str = ":".join(sorted((interface_a, interface_b)))
        digest = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
        return super().__new__(cls, digest)

    def __init__(self, interface_a, interface_b):
        self.interfaces = tuple(sorted((interface_a, interface_b)))
        super().__init__()

    def __getnewargs__(self):
        """To make sure it's pickleable"""
        return self.interfaces


forbidden_links = {
    LinkID(
        "00:00:00:00:00:00:01:01:4",
        "00:00:00:00:00:00:01:03:3"
    ),
    LinkID(
        "00:00:00:00:00:00:02:01:5",
        "00:00:00:00:00:00:02:03:4"
    ),
    LinkID(
        "00:00:00:00:00:00:03:01:5",
        "00:00:00:00:00:00:03:03:4"
    ),
    LinkID(
        "00:00:00:00:00:00:01:01:5",
        "00:00:00:00:00:00:03:01:4"
    ),
    LinkID(
        "00:00:00:00:00:00:01:02:5",
        "00:00:00:00:00:00:03:02:5"
    ),
    LinkID(
        "00:00:00:00:00:00:01:03:5",
        "00:00:00:00:00:00:03:03:5"
    ),
}

async def task(client: httpx.AsyncClient):
    response = await client.get(MEF_ELINE_API + f"/evc/",params={'checkConsistency':'True'})

    if not response.is_success:
        print(f"Failed to get EVCs")
    evc_dict: dict = response.json()
    print(f'Received {len(evc_dict)} EVCs')
    consistent_count = 0
    for circuit in evc_dict.values():
        path = circuit.get('current_path', [])
        if any(link['id'] in forbidden_links for link in path):
            print(f'EVC {circuit["id"]} {circuit["name"]} is not consistent')
        elif not circuit.get('active', False):
            print(f'EVC {circuit["id"]} {circuit["name"]} is not consistent')
        else:
            consistent_count +=1
    print(f'Received {consistent_count} consistent EVCs')
            
async def main():
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
    ) as client:
        await task(client)

asyncio.run(main())
