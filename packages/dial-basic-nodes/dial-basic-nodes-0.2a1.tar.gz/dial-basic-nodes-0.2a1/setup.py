# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dial_basic_nodes',
 'dial_basic_nodes.dataset_editor',
 'dial_basic_nodes.dataset_editor.dataset_table',
 'dial_basic_nodes.dataset_editor.datasets_list',
 'dial_basic_nodes.layers_editor',
 'dial_basic_nodes.layers_editor.layers_tree',
 'dial_basic_nodes.layers_editor.layers_tree.abstract_tree_model',
 'dial_basic_nodes.layers_editor.model_table',
 'dial_basic_nodes.model_compiler',
 'dial_basic_nodes.model_compiler.parameters_form']

package_data = \
{'': ['*']}

install_requires = \
['dial-core>=0.9a0,<0.10', 'dial-gui>=0.5a0,<0.6']

setup_kwargs = {
    'name': 'dial-basic-nodes',
    'version': '0.2a1',
    'description': 'Basic nodes for the Dial app.',
    'long_description': "# dial-basic-nodes\nBasic nodes for DL tasks, used by the Dial app.\n\n## Documentation\n\nThis project's documentation lives at [readthedocs.io](https://dial-basic-nodes.readthedocs.io)\n\n## License\n\nAll code is provided under the __GPL-3.0__ license. See [LICENSE](LICENSE) for more details.\n\n## Authors\n\n* **David Afonso (davafons)**: [Github](https://github.com/davafons) [Twitter](https://twitter.com/davafons)\n",
    'author': 'David Afonso',
    'author_email': 'davafons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dial-app/dial-basic-nodes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)
