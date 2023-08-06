# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iostat_context']

package_data = \
{'': ['*']}

install_requires = \
['serde>=0.8.0,<0.9.0']

extras_require = \
{':python_version >= "2.7" and python_version < "3.0"': ['backports.shutil_which>=3.5.2,<4.0.0']}

setup_kwargs = {
    'name': 'iostat-context',
    'version': '0.1.0',
    'description': 'A context manager for iostat.',
    'long_description': None,
    'author': 'Gregory C. Oakes',
    'author_email': 'gregoryoakes@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
