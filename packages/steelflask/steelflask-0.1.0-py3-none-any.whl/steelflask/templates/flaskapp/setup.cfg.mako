[flake8]
max-line-length = 160
exclude=${app_name}/migrations/**/* ${venv_folder}/**/ build/**/* dist/**/* htmlcov/**/* .git/**/* __pycache__ .eggs/**/*
max-complexity = 10

[options]
setup_requires = setuptools_scm
