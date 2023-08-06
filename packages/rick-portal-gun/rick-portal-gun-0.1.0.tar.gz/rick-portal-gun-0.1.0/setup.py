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
    'version': '0.1.0',
    'description': '',
    'long_description': '# Portal Gun\n\nThe awesome Portal Gun\n',
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
