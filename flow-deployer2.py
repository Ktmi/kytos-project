#!/usr/bin/env python


# ❯ jq -ncM '{method: "POST", url:"http://localhost:8181/api/kytos/flow_manager/v2/flows/00:00:00:00:00:00:00:01", body: { "force": false, "flows": [ { "priority": 10, "match": { "in_port": 1, "dl_vlan": 100 }, "actions": [ { "action_type": "output", "port": 1 } ] } ] } | @base64, header: {"Content-Type": ["application/json"]}}' | vegeta attack -format=json -rate 100/1s -duration=30s -timeout=60s | tee results.bin | vegeta report

import asyncio
import time

import httpx

KYTOS_URL = 'http://localhost:8181'

KYTOS_API = f"{KYTOS_URL}/api"

FLOW_MANAGER_API = f"{KYTOS_API}/kytos/flow_manager/v2"

async def deploy_flow(client: httpx.AsyncClient, flow):
    response = await client.post(
        FLOW_MANAGER_API + f'/flows/{flow["switch"]}',
        json=flow['flow_mod']
    )
    if not response.is_success:
        data = response.content
        print(f'Failed to deploy {flow}, reason {data}')
        return False
    #print(f"Response was: {response.content}")
    return True

async def worker(client: httpx.AsyncClient, queue: asyncio.Queue):
    while True:
        flow = await queue.get()

        await deploy_flow(client, flow)

        queue.task_done()


async def deploy_flows(client: httpx.AsyncClient, flows, worker_count):

    queue = asyncio.Queue()

    for flow in flows:
        queue.put_nowait(flow)

    worker_tasks = []

    for i in range(worker_count):
        task = asyncio.create_task(worker(client, queue))
        worker_tasks.append(task)

    await queue.join()

    for task in worker_tasks:
        task.cancel()

    await asyncio.gather(*worker_tasks, return_exceptions=True)

flow = {
    'switch': "00:00:00:00:00:00:01:01",
    'flow_mod': {
        "force": False,
        "flows": [
            {
                "owner": "Test",
                "priority": 10,
                "match": { "in_port": 1, "dl_vlan": 100 },
                "actions": [
                    {"action_type": "output", "port": 1}
                ]
            } for i in range(10000)
        ]
    }
}

async def main():
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(600.0),
    ) as client:
        start = time.time()
        await deploy_flow(client, flow)
        end = time.time()
        elapsed = end - start
        print(f"Process took: {elapsed} seconds to complete")


asyncio.run(main())
