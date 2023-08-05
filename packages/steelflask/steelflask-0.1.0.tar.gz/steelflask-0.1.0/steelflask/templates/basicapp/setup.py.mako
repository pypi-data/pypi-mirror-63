from setuptools import setup, find_packages
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(BASE_DIR, "steelflaskapp", "version.py")

setup(
    name=${app_name},
    packages=find_packages(
        exclude=('tests', 'tests.*')
    ),
    include_package_data=True,
    zip_safe=False,
    use_scm_version={
        'write_to': VERSION_FILE,
        'write_to_template': '__version__ = "{version}"\n',
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'gunicorn==20.0.0',
        'flask==1.1.1',
        'flask-sqlalchemy==2.4.1',
        'psycopg2==2.8.4',
        'flask-migrate==2.5.2',
        'PyJWT==1.7.1',
        'kanpai==0.1.11'
    ],
)
