## Steelflask
Opinionated flask app scaffolding tool. It will create a flask app structure targeted for rapid development and seamless deployment.

## Setup and Installation
- Create a folder where you want your application to reside.
- Create a virtual environment in that folder.
- activate the virtual environment.
- run `pip install steelflask` to install `steelflask` to your project.
- run `steelflask init` to generate flask app structure.
- `steelflask` uses `setuptools_scm` for automatic versioning of the project, which require the project to be maintained as a git repo.
- run `git init`
- run `pip install -r requirements_dev.txt` to install dev dependencies.
- run `pip install -e .` - it will install the project in with all required dependencies.
- You may need to deactivate the `venv` and activate again.
- run `pytest -vvs` to run test cases.