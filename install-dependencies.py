#!/usr/env python
'''
Installs kytos, several napps,
and there dependencies to the currently active environment.
'''

import os

NAPP_DEV_DIR = 'napps/kytos/'

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

napps = [
	'of_core',
	'flow_manager',
	'topology',
	'of_lldp',
	'pathfinder',
	'maintenance',
	'coloring',
	'sdntrace',
	'flow_stats',
	'sdntrace_cp',
	'mef_eline',
]

try:
	os.chdir(NAPP_DEV_DIR)
except FileNotFoundError:
	os.makedirs(NAPP_DEV_DIR)
	os.chdir(NAPP_DEV_DIR)

for name in napps:
	os.chdir(name)
	result = os.system('python setup.py develop')
	if result:
		raise Exception('Failed to install {name}')
	os.chdir('..')