# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obschart', 'obschart.api', 'obschart.api.nodes']

package_data = \
{'': ['*']}

install_requires = \
['gql>=0.3.0,<0.4.0', 'polling>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'obschart',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'ObsChart',
    'author_email': 'contact@obschart.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
