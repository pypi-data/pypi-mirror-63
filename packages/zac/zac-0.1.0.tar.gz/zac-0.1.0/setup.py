# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zac']

package_data = \
{'': ['*']}

install_requires = \
['gdal>=3.0.4,<4.0.0',
 'numba>=0.48.0,<0.49.0',
 'numpy>=1.18.1,<2.0.0',
 'psutil>=5.7.0,<6.0.0',
 'pyproj>=2.5.0,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'zac',
    'version': '0.1.0',
    'description': 'ZAC Atmospheric Correction',
    'long_description': None,
    'author': 'Tang Ziya',
    'author_email': 'tcztzy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
