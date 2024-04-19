#!/usr/bin/env python

import asyncio
import httpx
import itertools


KYTOS_URL = 'http://localhost:8181'

KYTOS_API = f"{KYTOS_URL}/api"

MEF_ELINE_API = f"{KYTOS_API}/kytos/mef_eline/v2"

VLAN_TAG_TYPE = 1

def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch



async def deploy_evc(client: httpx.AsyncClient, evc):
    response = await client.post(
        MEF_ELINE_API+'/evc/',
        json=evc
    )
    if not response.is_success:
        data = response.content()
        print(f'Failed to deploy {evc}, reason {data}')
        return False
    evc['id'] = response.json()['circuit_id']
    return True


async def deploy_evcs(client: httpx.AsyncClient, evcs):
    for batch in batched(
        [
            deploy_evc(client, evc)
            for evc in evcs
        ],
        5
    ):
        await asyncio.gather(
            *batch
        )

evc_cnt = 100

evcs1 = [
    {
        'name': f'Test Circuit 1-{i}',
        'uni_a': {
            'interface_id': '00:00:00:00:00:00:01:01:1',
            'tag': {
                'tag_type': VLAN_TAG_TYPE,
                'value': 100 + i
            }
        },
        'uni_z': {
            'interface_id': '00:00:00:00:00:00:01:03:1',
            'tag': {
                'tag_type': VLAN_TAG_TYPE,
                'value': 100 + i,
            }
        },
        'dynamic_backup_path': True,
        'primary_constraints': {
            'mandatory_metrics': {
                'not_ownership': ['border'],
            },
        },
        'primary_path': [
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:01:01:3'},
                'endpoint_b': {'id': '00:00:00:00:00:00:02:01:2'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:02:01:4'},
                'endpoint_b': {'id': '00:00:00:00:00:00:03:01:2'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:03:01:3'},
                'endpoint_b': {'id': '00:00:00:00:00:00:03:02:3'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:03:02:4'},
                'endpoint_b': {'id': '00:00:00:00:00:00:03:03:3'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:03:03:2'},
                'endpoint_b': {'id': '00:00:00:00:00:00:02:03:5'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:02:03:2'},
                'endpoint_b': {'id': '00:00:00:00:00:00:01:03:4'},
            },
        ],
    }
    for i in range(evc_cnt)
]

evcs2 = [
    {
        'name': f'Test Circuit 2-{i}',
        'uni_a': {
            'interface_id': '00:00:00:00:00:00:01:01:1',
            'tag': {
                'tag_type': VLAN_TAG_TYPE,
                'value': 200 + i,
            }
        },
        'uni_z': {
            'interface_id': '00:00:00:00:00:00:01:03:1',
            'tag': {
                'tag_type': VLAN_TAG_TYPE,
                'value': 200 + i,
            }
        },
        'dynamic_backup_path': True,
        'primary_constraints': {
            'mandatory_metrics': {
                'not_ownership': ['border'],
            },
        },
    }
    for i in range(evc_cnt)
]

evcs3 = [
    {
        'name': f'Test Circuit 3-{i}',
        'uni_a': {
            'interface_id': '00:00:00:00:00:00:03:01:1',
            'tag': {
                'tag_type': VLAN_TAG_TYPE,
                'value': 100 + i,
            }
        },
        'uni_z': {
            'interface_id': '00:00:00:00:00:00:03:03:1',
            'tag': {
                'tag_type': VLAN_TAG_TYPE,
                'value': 100 + i,
            }
        },
        'dynamic_backup_path': True,
        'primary_constraints': {
            'mandatory_metrics': {
                'not_ownership': ['border'],
            },
        },
        'primary_path': [
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:03:01:2'},
                'endpoint_b': {'id': '00:00:00:00:00:00:02:01:4'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:02:01:2'},
                'endpoint_b': {'id': '00:00:00:00:00:00:01:01:3'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:01:01:2'},
                'endpoint_b': {'id': '00:00:00:00:00:00:01:02:2'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:01:02:3'},
                'endpoint_b': {'id': '00:00:00:00:00:00:01:03:2'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:01:03:4'},
                'endpoint_b': {'id': '00:00:00:00:00:00:02:03:2'},
            },
            {
                'endpoint_a': {'id': '00:00:00:00:00:00:02:03:5'},
                'endpoint_b': {'id': '00:00:00:00:00:00:03:03:2'},
            },
        ]
    }
    for i in range(evc_cnt)
]

evcs4 = [
    {
        'name': f'Test Circuit 4-{i}',
        'uni_a': {
            'interface_id': '00:00:00:00:00:00:03:01:1',
            'tag': {
                'tag_type': VLAN_TAG_TYPE,
                'value': 200 + i,
            }
        },
        'uni_z': {
            'interface_id': '00:00:00:00:00:00:03:03:1',
            'tag': {
                'tag_type': VLAN_TAG_TYPE,
                'value': 200 + i,
            }
        },
        'dynamic_backup_path': True,
        'primary_constraints': {
            'mandatory_metrics': {
                'not_ownership': ['border'],
            },
        },
    }
    for i in range(evc_cnt)
]
async def main():
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
    ) as client:
        await asyncio.gather(
            deploy_evcs(client, evcs1),
            deploy_evcs(client, evcs2),
            deploy_evcs(client, evcs3),
            deploy_evcs(client, evcs4)
        )

asyncio.run(main())
