# -*- coding: utf-8 -*-

import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = 'everon'
DESCRIPTION = 'It makes easier to build user command-line interface'
AUTHOR = 'Victor Dao'
EMAIL = 'daongocthang.vn@gmail.com'
URL = 'https://github.com/wayfar3/everon'

REQUIRED = ['colorama']

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(os.path.join(here, 'everon', '__version__.py')) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload"""
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds ...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel distribution ...')
        os.system('{} setup.py sdist bdist_wheel'.format(sys.executable))

        # Note: To use the 'upload' functionality of this file, you must:
        # pip install twine
        self.status('Uploading the package to PyPi via Twine ...')
        os.system('twine upload dist/*')


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
