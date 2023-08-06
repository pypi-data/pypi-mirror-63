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
    'version': '0.1.1',
    'description': '',
    'long_description': '# int set\n\n# Abstract\n\nCounts the number of integers.\n整数を数えます。\n\n## What does this do?\n\nCounts the number of integers that can be any integer multiple within a given start and end.\n始まりと終了を指定すると、その中に含まれる任意の整数倍となる整数の数を数えます。\n\nVery Fast!!\n## usage\n```python\nfrom int_set import IntSet, step\n\n# IntSet makes range like object\n# IntSetはrangeのようのオブジェクトを作成します。\n\n_range = IntSet(100)       # start: 0 stop: 100\n_range = IntSet(100, 1000) # start: 100 stop: 1000\n\ns = step(2)   # a multiple of two（２の倍数）\ns = step(2,5) # a multiple of 2 or a multiple of 5（２の倍数または５の倍数）\n\n# Count multiples of 2 or 5 between 100 and 1000.\n# 100 ~ 1000に含まれる２の倍数または５の倍数の数を数えます。\n_range.count(s) # 541\n```\n\n## install\n\n```shell script\npip install int-set\n```',
    'author': 'YutaUra',
    'author_email': 'yuuta3594@outlook.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/YutaUra/IntSet',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
