# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renoir_haml']

package_data = \
{'': ['*']}

install_requires = \
['renoir>=1.1,<2.0']

setup_kwargs = {
    'name': 'renoir-haml',
    'version': '1.0.0',
    'description': 'HAML syntax for Renoir templates',
    'long_description': '# Renoir-HAML\n\nRenoir-HAML is an extension for the [Renoir engine](https://github.com/emmett-framework/renoir) providing an HAML like syntax for templates. This is not a template engine but a compiler which converts HAML files to HTML Renoir templates.\n\n[![pip version](https://img.shields.io/pypi/v/renoir-haml.svg?style=flat)](https://pypi.python.org/pypi/Renoir-HAML) \n\n## Installation\n\nYou can install Renoir-HAML using pip:\n\n    pip install renoir-haml\n\nAnd add it to your Renoir engine:\n\n```python\nfrom renoir_haml import Haml\n\nrenoir.use_extension(Haml)\n```\n\n## Configuration\n\n| param | default | description |\n| --- | --- | --- |\n| encoding | utf8 | encoding for IO |\n| reload | `False` | enable auto reload on file changes |\n\n## License\n\nRenoir-HAML is released under BSD license. Check the LICENSE file for more details.\n',
    'author': 'Giovanni Barillari',
    'author_email': 'gi0baro@d4net.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gi0baro/renoir-haml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
