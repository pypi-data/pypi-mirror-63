#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

description = "Tomato Clock is a simple command line pomodoro app"
version = "0.0.4"

setup(
    name="tomato-clock",
    version=version,
    author="Bruce Lee",
    author_email="bruce.meerkat@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    keywords="pomodoro tomato tomato-timer terminal terminal-app pomodoro-timer",
    url="https://github.com/coolcode/tomato-clock",
    python_requires=">=3.5",
    classifiers=['Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: Unix',
                 'Operating System :: MacOS'],
    platforms='any',
    scripts=['tomato.py'],
    include_package_data=True,
    package_data={"": ["*.md"]},
    packages=find_packages(),
    entry_points={"console_scripts": ["tomato = tomato:main"]}
)
