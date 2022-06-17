
## Setup

It is recommended to create a virtual environment:

```shell
python3 -m venv ./venv
source ./venv/bin/activate
```

## Installing requirements

This library uses poetry for managing dependencies, virtual environment and package publication. For full documentation, see https://python-poetry.org/docs/. In short, Poetry works by:

* Locking dependencies in place and committing this to source control: you always use the same package versions, no matter what OS
* Installing packages from the lockfile, if needed deleting redundant ones

Before you start, add `export POETRY_VIRTUALENVS_IN_PROJECT=1` to your `.bash_profile`, `.bashrc`, etc to make sure poetry creates the venv in this project folder and your IDE can auto-discover it. It will be kept out of source control.

Install poetry in your global environment and point it to your local Python version of choice:
```shell
pip install poetry==1.2.0a2 poetry-dynamic-versioning
poetry env use [location/of/python/version/bin/python]
```
You can also use e.g. pyenv or virtualenv to manage Python versions (might have to upgrade the latter) and point poetry to that. Refer to the docs on how to set the right Python env: https://python-poetry.org/docs/managing-environments/.

## Updating / installing dependencies

In order to lock dependencies (e.g. after you've made manual edits to the `pyproject.toml`), run
```shell
poetry lock --no-update
```
The `no-update` argument greatly speeds up and is to only update changed dependencies (and not update existing open-ended ones), which is fine because we generally fix package versions.

To (then) install from the lockfile, run
```shell
poetry install --sync
```
It will warn you if the lockfile is out of date and needs to be re-locked. `--sync` argument is to also remove any packages that you manually removed from `pyproject.toml`. Editing `pyproject.toml` is probably the quickest way to update your environment. Always remember to lock after you've edited it.

You can also add / remove packages individually by using
```shell
poetry add --group test pytest==6.1.0
poetry remove pytest
```
The `--group test` argument adds the package to a dependency group `test`, meaning it is kept out of production dependencies and used only for local dev / CICD. Without this, it's added to the default env.

