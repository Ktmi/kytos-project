#!/usr/bin/env python
'''
Installs kytos, several napps,
and there dependencies to the currently active environment.
'''

import os

NAPP_DEV_DIR = 'napps/'

dependencies = [
	'setuptools',
	'pip',
	'wheel',
]

for dependency in dependencies:
	os.system(f'pip install {dependency}')

kytos_components = [
	('python-openflow', 'master'),
	('kytos-utils', 'master'),
	('kytos', 'master'),
]

for name, branch in kytos_components:
	os.chdir(name)
	os.system('git fetch')
	os.system(f'git checkout {branch}')
	os.system('git pull')
	result = os.system('pip install -e .')
	if result:
		raise Exception(f'Failed to install {name}')
	os.chdir('..')

napps = {
	'kytos': [
		('of_core', 'master'),
		('flow_manager', 'master'),
		('topology', 'master'),
		('of_lldp', 'master'),
		('pathfinder', 'master'),
		('maintenance', 'master'),
		('mef_eline', 'master'),
	],
	'amlight': [
		('coloring', 'master'),
		('sdntrace', 'master'),
		('flow_stats', 'master'),
		('sdntrace_cp', 'master'),
	],
}

try:
	os.chdir(NAPP_DEV_DIR)
except FileNotFoundError:
	os.makedirs(NAPP_DEV_DIR)
	os.chdir(NAPP_DEV_DIR)

for username, user_napps in napps.items():
	os.chdir(username)
	for napp_name, branch in user_napps:
		os.chdir(napp_name)
		os.system('git fetch')
		os.system(f'git checkout {branch}')
		os.system('git pull')
		result = os.system('pip install -e .')
		if result:
			raise Exception(f'Failed to install {napp_name}')
		os.chdir('..')
	os.chdir('..')
