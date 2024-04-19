#!/usr/bin/env python

import asyncio
import hashlib
import httpx
import itertools


KYTOS_URL = 'http://localhost:8181'

KYTOS_API = f"{KYTOS_URL}/api"

TOPOLOGY_API = f"{KYTOS_API}/kytos/topology/v3"

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



def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch



async def add_metadata(client: httpx.AsyncClient, item_id, metadata):
    response = await client.post(
        f'{TOPOLOGY_API}/{item_id}/metadata',
        json=metadata
    )
    if not response.is_success:
        data = response.json()
        print(f'Failed to add metadata to item {item_id}, reason {data}')
        return False
    return True


async def deploy_metadata(client: httpx.AsyncClient, meta_info):
    for batch in batched(
        [
            add_metadata(client, *command)
            for command in meta_info
        ],
        5
    ):
        await asyncio.gather(
            *batch
        )

switch_positions = [
    (
        f"switches/00:00:00:00:00:00:{x:02d}:{y:02d}",
        {
            'lat': -(10*x),
            'lng': 10*y,
        }
    )
    for x, y in itertools.product(
        range(1,4),
        range(1,4)
    )
]

border_links = [
    (
        f'links/{link_id}',
        {
            "ownership": [
                "border"
            ]
        }
    )
    for link_id in [
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
    ]
]

async def main():
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
    ) as client:
        await asyncio.gather(
            deploy_metadata(client, switch_positions),
            deploy_metadata(client, border_links),
        )

asyncio.run(main())
