# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typer_cli']

package_data = \
{'': ['*']}

install_requires = \
['click-completion>=0.5.2,<0.6.0',
 'colorama>=0.4.3,<0.5.0',
 'importlib_metadata>=1.5,<2.0',
 'typer>=0.0.9,<0.0.10']

entry_points = \
{'console_scripts': ['typer = typer_cli.main:main']}

setup_kwargs = {
    'name': 'typer-cli',
    'version': '0.0.4',
    'description': 'Run Typer scripts with completion, without having to create a package, using Typer CLI.',
    'long_description': '# Typer CLI\n\n<p align="center">\n    <em>Run <strong>Typer</strong> scripts with completion, without having to create a package, using <strong>Typer CLI</strong>.</em>\n</p>\n<p align="center">\n<a href="https://travis-ci.com/tiangolo/typer-cli" target="_blank">\n    <img src="https://travis-ci.com/tiangolo/typer-cli.svg?branch=master" alt="Build Status">\n</a>\n<a href="https://codecov.io/gh/tiangolo/typer-cli" target="_blank">\n    <img src="https://codecov.io/gh/tiangolo/typer-cli/branch/master/graph/badge.svg" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/typer-cli" target="_blank">\n    <img src="https://badge.fury.io/py/typer-cli.svg" alt="Package version">\n</a>\n</p>\n\n---\n\n⚠️ **WARNING** ⚠️ If you are building a CLI package you probably need [**Typer**](https://typer.tiangolo.com/), the library itself. This, **Typer CLI**, is a CLI application that simplifies running simple **Typer** scripts, it is not the library itself.\n\n## Description\n\n**Typer** is a library for building CLIs (Command Line Interface applications).\n\n**Typer CLI** (this package) is a CLI application that simplifies running simple programs created with **Typer** with completion. 🚀\n\n**Typer CLI**\'s main feature is to provide ✨ completion ✨ in the Terminal for your own small programs built with **Typer**, without you having to create a complete installable Python package with them.\n\nIt\'s probably most useful if you have a small custom Python script using **Typer** (maybe as part of some project), for some small tasks, and it\'s not complex/important enough to create a whole installable Python package for it (something to be installed with `pip`).\n\nIn that case, you can install **Typer CLI**, and run your program with the `typer` command in your Terminal, and it will provide completion for your script.\n\n## Usage\n\n### Install\n\nInstall **Typer CLI**:\n\n```console\n$ python -m pip install typer-cli\n```\n\nThat creates a `typer` command.\n\nYou can then install completion for it:\n\n```console\n$ typer --install-completion\n```\n\n### Sample script\n\nLet\'s say you have a script that uses **Typer** in `my_custom_script.py`:\n\n```Python\nimport typer\n\napp = typer.Typer()\n\n\n@app.command()\ndef hello(name: str = None):\n    if name:\n        typer.echo(f"Hello {name}")\n    else:\n        typer.echo("Hello World!")\n\n\n@app.command()\ndef bye(name: str = None):\n    if name:\n        typer.echo(f"Bye {name}")\n    else:\n        typer.echo("Goodbye!")\n\n\nif __name__ == "__main__":\n    app()\n```\n\n### Run with Python\n\nThen you could run your script with normal Python:\n\n```console\n$ python my_custom_script.py hello\n\nHello World!\n\n$ python my_custom_script.py hello --name Camila\n\nHello Camila!\n\n$ python my_custom_script.py bye --name Camila\n\nBye Camila\n```\n\nThere\'s nothing wrong with running with Python directly. And, in fact, if some other code or program uses your script, that would be the best way to do it.\n\n⛔️ But in your terminal, you won\'t get completion when hitting <kbd>TAB</kbd> for any of the subcommands or options, like `hello`, `bye`, and `--name`.\n\n### Run with **Typer CLI**\n\nHere\'s where **Typer CLI** is useful.\n\nYou can also run the same script with the `typer` command you get after installing `typer-cli`:\n\n```console\n$ typer my_custom_script.py run hello\n\nHello World!\n\n$ typer my_custom_script.py run hello --name Camila\n\nHello Camila!\n\n$ typer my_custom_script.py run bye --name Camila\n\nBye Camila\n```\n\n* Instead of using `python` directly you type `typer`.\n* After the name of the file you add the subcommand `run`.\n\n✔️ If you installed completion for **Typer CLI** (for the `typer` command) as described above, when you hit <kbd>TAB</kbd> you will have completion for everything, including the `run` and all the subcommands and options of your script, like `hello`, `bye`, and `--name`. 🚀\n\n## If main\n\nBecause **Typer CLI** won\'t use the block with:\n\n```Python\nif __name__ == "__main__":\n    app()\n```\n\nYou can also remove it if you are calling that script only with **Typer CLI** (using the `typer` command).\n\n## What can it run\n\n**Typer CLI** will run any script made with **Typer**.\n\nIt could even run a file with a function that could be used with `typer.run()`, even if it doesn\'t really use **Typer**.\n\nFor example, a file `main.py` like this will still work:\n\n```Python\ndef main(name: str = "World"):\n    print(f"Hello {name}")\n```\n\nThen you can call it with:\n\n```console\n$ typer main.py run --help\nUsage: typer run [OPTIONS]\n\nOptions:\n  --name TEXT\n  --help       Show this message and exit.\n\n$ typer main.py run --name Camila\n\nHello Camila\n```\n\nAnd it will also have completion for things like the `--name` **CLI Option**.\n\n## Options\n\nYou can specify the following **CLI Options**:\n\n* `--app`: the name of the variable with a `Typer()` object to run as the main app.\n* `--func`: the name of the variable with a function that would be used with `typer.run()`.\n\n### Defaults\n\nWhen your run a script with the **Typer CLI** (the `typer` command) it will use the app from the following priority:\n\n* App object from `--app` *CLI Option*.\n* Function to convert to a **Typer** app from `--func` *CLI Option*.\n* **Typer** app in a variable with a name of `app`, `cli`, or `main`.\n* The first **Typer** app available in the file, with any name.\n* A function in a variable with a name of `main`, `cli`, or `app`.\n* The first function in the file, with any name.\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Sebastián Ramírez',
    'author_email': 'tiangolo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tiangolo/typer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
