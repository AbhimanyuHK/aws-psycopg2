import setuptools
from distutils.core import Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-psycopg2",
    version="1.1.0",
    author="Abhimanyu HK",
    author_email="manyu1994@hotmail.com",
    description="A aws psycopg2 package from psycopg2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbhimanyuHK/aws-psycopg2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
