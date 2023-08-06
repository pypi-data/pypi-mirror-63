# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_solar']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.770,<0.771', 'numpy>=1.18.1,<2.0.0', 'pygame>=1.9.6,<2.0.0']

setup_kwargs = {
    'name': 'py-solar',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Danil',
    'author_email': 'danilunrandom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
