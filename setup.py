#!/usr/bin/env python
from setuptools import setup

requires = [
    'jinja2 >= 2.7',
    'python-slugify >= 1.1.4'
]

entry_points = {
    'console_scripts': [
        'readgull = readgull:main'
    ]
}

setup(
    name="readgull",
    version="0.0.1",
    author="Patrick Allen",
    author_email="prallen90@gmail.com",
    description="A tool to generate a static sige from Markdown",
    packages=['readgull'],
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        'Development Status :: 1 - Development/Not Stable',
         'Environment :: Console',
         'License :: OSI Approved :: GNU Affero General Public License v3',
         'Operating System :: OS Independent',
         'Programming Language :: Python :: 2',
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.3',
         'Programming Language :: Python :: 3.4',
         'Programming Language :: Python :: 3.5',
         'Topic :: Internet :: WWW/HTTP',
         'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
