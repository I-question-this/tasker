#!/usr/bin/env python
"""The setup file for installing Chesster as a module"""
import os
from setuptools import setup, find_packages

version_path = os.path.join(os.path.dirname(__file__), 'src/tasker/version.py')
# Get current version
with open(version_path, 'r') as fin:
    exec(fin.read())

setup(
    version=str(__version__),
    setup_requires=[],
    test_require=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'check_off_tasks = tasker.cli.check_off_tasks:cli_interface',
            'reminder_tasks = tasker.cli.reminder_tasks:cli_interface',
            'todays_schedule = tasker.cli.todays_schedule:cli_interface'
        ]
    }
)
