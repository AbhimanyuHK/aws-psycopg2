@echo off

del psycopg2 y

pip install psycopg2 -t . --upgrade

python setup.py sdist bdist_wheel

python compile_and_build.py

twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
