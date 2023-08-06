#!/usr/bin/env python3
# flake8: noqa
import re
import setuptools


# main setup kw args
setup_kwargs = {
    'name': 'coax',
    'version': '0.0.0',
    'description':
        "(this is a placeholder for the forthcoming coax package)",
    'long_description':
        "(this is a placeholder for the forthcoming coax package)",
    'author': 'Kristian Holsheimer',
    'author_email': 'kristian.holsheimer@gmail.com',
    'url': '',
    'license': 'MIT',
    'install_requires': [],
    'classifiers': [
        'Development Status :: 1 - Planning',
        'Environment :: Other Environment',
        'Framework :: Jupyter',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    'zip_safe': True,
    'packages': [],
}


if __name__ == '__main__':
    setuptools.setup(**setup_kwargs)
