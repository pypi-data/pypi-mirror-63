# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['empyrionbuildassistant', 'empyrionbuildassistant.lib']

package_data = \
{'': ['*']}

install_requires = \
['pathtools>=0.1.2,<0.2.0',
 'psutil>=5.7.0,<6.0.0',
 'vdf>=3.2,<4.0',
 'watchdog>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['APPLICATION-NAME = entry:main']}

setup_kwargs = {
    'name': 'empyrionbuildassistant',
    'version': '0.1.5',
    'description': 'A simple set of scripts to make developing mods for Empyrion easier',
    'long_description': '# Empyrion Build Assistant\n ## What is this?\n This is a python package that I created to automate a lot of the tasks that go into building mods for Empyrion. \n ## How do I use it?\n assuming you have python 3.8 installed,the package is loaded using:\n ```shell script\npip install empyrionbuildassistant\n``` \n\nOnce installed, you an view the help using:\n```\npython -m EmpyrionBuildAssistant -h\n```\n\nwhich should show:\n\n```text\nusage: __main__.py [-h] [--copyDllsToFolder COPYDLLSTOFOLDER] [--modName MODNAME] [--bundleAndDeployMod BUNDLEANDDEPLOYMOD] [-clearLogs] [-watchLogs] [-launchServer]\n\nscripts to help build and deploy empyrion mods\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --copyDllsToFolder COPYDLLSTOFOLDER\n                        the folder to copied the required dlls to\n  --modName MODNAME     the name of the mod being deployed\n  --bundleAndDeployMod BUNDLEANDDEPLOYMOD\n                        the folder containing the mod that will be deployed\n  -clearLogs            clears the logs on the dedi server\n  -watchLogs            watches the dedi server logs, press enter to exit\n  -launchServer         launches the dedi server, press enter to kill\n\nNote: modname must be specified when using the bundleAndDeployMod option\n```\n\n## Can the commands be chained?\n\nYup, the most useful command that I use for debugging is\n\n```shell script\npython -m EmpyrionBuildAssistant -clearLogs -watchLogs -launchServer\n```\n\nWhich clears the logs launches the server and creates a window that watches all of the changes to the server\'s log files.  When you press enter, it will terminate the server process (and its children)\n\n## How does it work?\n\nIt starts by scanning your windows registry (sorry at the moment this works on windows only :( ) to locate your steam installation path.  From there it traverses the steamapps manifests to locate the install location of the dedicated server (Steam AppID 530870) and it uses that path as the root for all of the commands.\n\n## Is this like, "done"?\n\nHAHAHAHAHAHAHAHAAHAHAHAHAHA\n\nNo, it is not, as evidence I present the complete absence of tests.  this is really just a collection of scripts that I threw together to make another problem that I\'m working on easier to solve.\n\nIf you\'d like to help please leave issues or PRs\n\n## What about the obvious question you haven\'t addressed here?\n\nIf you have a question I didn\'t think of, feel free to leave it as an issue.  If it gets asked a lot (or it seems like a really good question) I\'ll add it here.\n',
    'author': 'Chris Wheeler',
    'author_email': 'cmwhee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lostinplace/EmpyrionBuildAssistant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
