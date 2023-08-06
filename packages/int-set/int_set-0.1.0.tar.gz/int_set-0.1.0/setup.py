# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['int_set']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'int-set',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'YutaUra',
    'author_email': 'yuuta3594@outlook.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
