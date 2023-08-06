# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_iam_tester']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.12.22',
 'click>=7.1.1,<8.0.0',
 'pyyaml>=5.3,<6.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['aws_iam_tester = aws_iam_tester.cli:main']}

setup_kwargs = {
    'name': 'aws-iam-tester',
    'version': '0.0.3',
    'description': 'AWS IAM tester - simple command-line tool to check permissions handed out to IAM users and roles.',
    'long_description': None,
    'author': 'Gerco Grandia',
    'author_email': 'gerco.grandia@4synergy.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
