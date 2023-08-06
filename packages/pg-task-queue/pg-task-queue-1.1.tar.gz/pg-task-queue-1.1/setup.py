import codecs
import os
import sys


from distutils.util import convert_path
from fnmatch import fnmatchcase
from setuptools import setup, find_packages


PACKAGE = "pg_tasks_queue"
NAME = "pg-task-queue"
DESCRIPTION = "Python asinc task system with postgres database"
AUTHOR = "Alex V. Smith"
AUTHOR_EMAIL = "smith.it.interface@gmail.com"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    packages=find_packages(exclude=["tests.*", "tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        'psycopg2',
        'pandas',
    ],
    include_package_data=True,
    zip_safe=False,
)