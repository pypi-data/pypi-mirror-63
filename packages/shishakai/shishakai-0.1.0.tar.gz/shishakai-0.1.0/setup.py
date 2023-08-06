# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shishakai']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8,<5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0']}

setup_kwargs = {
    'name': 'shishakai',
    'version': '0.1.0',
    'description': 'Gather schedules for movie preview events',
    'long_description': '# shishakai\n\nshishakai is a Python library that gathers schedules for movie preview events. The "shishakai" (試写会) is a movie preview in Japanese.\n\n[![PyPI](https://img.shields.io/pypi/v/shishakai.svg)](https://pypi.org/project/shishakai/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shishakai.svg)](https://pypi.org/project/shishakai/)\n[![Python Tests](https://github.com/speg03/shishakai/workflows/Python%20Tests/badge.svg)](https://github.com/speg03/shishakai/actions?query=workflow%3A%22Python+Tests%22)\n[![codecov](https://codecov.io/gh/speg03/shishakai/branch/master/graph/badge.svg)](https://codecov.io/gh/speg03/shishakai)\n',
    'author': 'Takahiro Yano',
    'author_email': 'speg03@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/speg03/shishakai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
