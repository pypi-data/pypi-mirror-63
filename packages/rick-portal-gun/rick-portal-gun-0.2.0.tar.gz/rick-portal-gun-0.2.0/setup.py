# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rick_portal_gun']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.0.11,<0.0.12']

entry_points = \
{'console_scripts': ['rick-portal-gun = rick_portal_gun.main:app']}

setup_kwargs = {
    'name': 'rick-portal-gun',
    'version': '0.2.0',
    'description': '',
    'long_description': '# `callback`\n\nAwesome Portal Gun\n\n**Usage**:\n\n```console\n$ callback [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `load`: Load the portal gun\n* `shoot`: Shoot the portal gun\n\n## `callback load`\n\nLoad the portal gun\n\n**Usage**:\n\n```console\n$ callback load [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `callback shoot`\n\nShoot the portal gun\n\n**Usage**:\n\n```console\n$ callback shoot [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
    'author': 'Sebastián Ramírez',
    'author_email': 'tiangolo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
