#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import httpx

async def deactivate_interface(intf):
    proc = await asyncio.create_subprocess_exec(
        'sudo', 'ip', 'link', 'set', 'dev', intf, 'down',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await proc.wait()

async def activate_interface(intf):
    proc = await asyncio.create_subprocess_exec(
        'sudo', 'ip', 'link', 'set', 'dev', intf, 'up',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await proc.wait()

async def flap_interface(intf):
    await deactivate_interface(intf)
    await activate_interface(intf)

async def do_link_flap(interfaces: list[str]) -> None:
    """perform link flap."""
    await asyncio.gather(*[
        flap_interface(intf)
        for intf in interfaces
    ])

async def flap_forever(interfaces: list[str], info: dict):
    flap_count = 0
    try:
        while True:
            flap_count += 1
            await asyncio.shield(do_link_flap(interfaces))
    except asyncio.CancelledError:
        pass
    finally:
        info['flap_count'] = flap_count

def assert_topology_link_up(link_id: str) -> None:
    """assert link up."""
    client = httpx.Client(base_url="http://localhost:8181/api/kytos/topology/v3/links")
    resp = client.get("/")
    resp.raise_for_status()
    data = resp.json()
    link = data["links"][link_id]
    assert link["status"] == "UP", link
    assert link["endpoint_a"]["status"] == "UP", link
    assert link["endpoint_b"]["status"] == "UP", data


async def main() -> None:
    """Main function."""
    link_flap_time = 5
    interfaces = ["s1x1-eth1", "s3x3-eth1","s1x3-eth1", "s3x1-eth1"]
    wait_for = 0.1
    test_iters = 2

    for test_iter in range(test_iters):
        print(f"link_flap test iteration {test_iter}")
        # assert_topology_link_up(link_id)
        current_time = time.time()
        start = current_time
        info = {'flap_cnt': 0}
        try:
            await asyncio.wait_for(flap_forever(interfaces, info), link_flap_time)
        except TimeoutError:
            pass
        end = time.time()
        print(f"\t Flapped links {info['flap_count']} times in {end-start} seconds")
        print(f"\t waiting for {wait_for} secs before next iteration")
        time.sleep(wait_for)
        # assert_topology_link_up(link_id)


if __name__ == "__main__":
    asyncio.run(main())