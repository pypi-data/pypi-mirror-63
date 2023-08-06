# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convertempPy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'convertemppy',
    'version': '4.0.0',
    'description': 'Easily convert between temperatures!',
    'long_description': '## convertempPy \n\n![](https://github.com/ttimbers/convertempPy/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/ttimbers/convertempPy/branch/master/graph/badge.svg)](https://codecov.io/gh/ttimbers/convertempPy) ![Release](https://github.com/ttimbers/convertempPy/workflows/Release/badge.svg)\n\n[![Documentation Status](https://readthedocs.org/projects/convertemppy/badge/?version=latest)](https://convertemppy.readthedocs.io/en/latest/?badge=latest)\n\nEasily convert between temperatures: Celsius, Kelvin & Fahrenheit! This is a toy package developed for the [UBC MDS DSCI 524 (Collaborative Software Development) course](https://github.com/UBC-MDS/DSCI_524_collab-sw-dev). \n\n### Installation:\n\n```\npip install -i https://test.pypi.org/simple/ convertempPy\n```\n\n### Features\nContains functions for all permutations of conversions between Celsius, Kelvin and Fahrenheit. This package is an example for the UBC MDS DSCI 524 (Collaborative Software Development) course. Yup, that one!\n\n### Dependencies\n\n- Python 3 or greater\n\n### Usage\n\nExample usage:\n```\n>>> from convertempPy import convertempPy as tmp\n>>> tmp.fahr_to_celsius(32)\n```\n\n```\n0\n```\n\n### Documentation\nThe official documentation is hosted on Read the Docs: <https://convertempPy.readthedocs.io/en/latest/>\n\n### Credits\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'ttimbers',
    'author_email': 'tiffany.timbers@stat.ubc.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ttimbers/convertempPy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
