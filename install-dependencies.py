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
	'python-openflow',
	'kytos-utils',
	'kytos',
]

for name in kytos_components:
	os.chdir(name)
	result = os.system('python setup.py develop')
	if result:
		raise Exception('Failed to install {name}')
	os.chdir('..')

napps = {
	'kytos': [
		'of_core',
		'flow_manager',
		'topology',
		'of_lldp',
		'pathfinder',
		'maintenance',
		'mef_eline',
	],
	'amlight': [
		'coloring',
		'sdntrace',
		'flow_stats',
		'sdntrace_cp',
	],
}

try:
	os.chdir(NAPP_DEV_DIR)
except FileNotFoundError:
	os.makedirs(NAPP_DEV_DIR)
	os.chdir(NAPP_DEV_DIR)

for username, user_napps in napps.items():
	os.chdir(username)
	for napp_name in user_napps:
		os.chdir(napp_name)
		result = os.system('python setup.py develop')
		if result:
			raise Exception(f'Failed to install {napp_name}')
		os.chdir('..')
	os.chdir('..')