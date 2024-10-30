#!/usr/bin/env python
'''
Installs kytos, several napps,
and there dependencies to the currently active environment.
'''

import os
import shutil

NAPP_DEV_DIR = 'napps/'

dependencies = [
	'setuptools',
	'pip',
	'wheel',
	'tox',
	'pip-tools',
	'isort',
	'black',
]

for dependency in dependencies:
	os.system(f'pip install {dependency}')

kytos_components = [
	('python-openflow', '2023.2.0'),
	('kytos-utils', '2023.2.0'),
	('kytos', '2023.2.0'),
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

ui = [('ui', '2023.2.3')]

for name, branch in ui:
	os.chdir(name)
	os.system('git fetch')
	os.system(f'git checkout {branch}')
	os.system('git pull')
	os.system('npm install')
	os.system('npm run build')
	try:
		os.mkdir('../kytos/kytos/web-ui/')
	except FileExistsError as exc:
		shutil.rmtree('../kytos/kytos/web-ui/')
		os.mkdir('../kytos/kytos/web-ui/')
	os.system('unzip latest.zip -d ../kytos/kytos/web-ui/')
	os.chdir('..')

napps = {
	'kytos': [
		('of_core','2023.2.0'),
		('flow_manager', '2023.2.0'),
		('topology', '2023.2.4'),
		('of_lldp', '2023.2.1'),
		('pathfinder', '2023.2.0'),
		('maintenance', '2023.2.0'),
		('mef_eline', '2023.2.4'),
		('of_multi_table', '2023.2.0'),
		('telemetry_int', '2023.2.0'),
	],
	'amlight': [
		('coloring', '2023.2.0'),
		('sdntrace', '2023.2.0'),
		('flow_stats', '2023.1.0'),
		('sdntrace_cp', '2023.2.0'),
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
