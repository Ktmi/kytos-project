#!/usr/bin/env python
'''
Installs kytos, several napps,
and there dependencies to the currently active environment.
'''

import os

NAPP_DEV_DIR = 'napps/'

dependencies = [
	'setuptools==60.2.0',
	'pip==21.3.1',
	'wheel==0.37.1',
]

for dependency in dependencies:
	os.system(f'pip install {dependency}')

kytos_components = [
	('python-openflow', '2023.1.0'),
	('kytos-utils', '2023.1.0'),
	('kytos', '2023.1.1'),
]

for name, branch in kytos_components:
	os.chdir(name)
	os.system('git fetch')
	os.system(f'git checkout {branch}')
	os.system('git pull')
	result = os.system('python setup.py develop')
	if result:
		raise Exception(f'Failed to install {name}')
	os.chdir('..')

napps = {
	'kytos': [
		('of_core', '2023.1.0'),
		('flow_manager', '2023.1.1'),
		('topology', '2023.1.1'),
		('of_lldp', '2023.1.0'),
		('pathfinder', '2023.1.0'),
		('maintenance', '2023.1.0'),
		('mef_eline', '2023.1.3'),
	],
	'amlight': [
		('coloring', '2023.1.0'),
		('sdntrace', '2023.1.0'),
		('flow_stats', '2023.1.0'),
		('sdntrace_cp', '2023.1.0'),
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
		result = os.system('python setup.py develop')
		if result:
			raise Exception(f'Failed to install {napp_name}')
		os.chdir('..')
	os.chdir('..')