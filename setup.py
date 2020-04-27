"""
Setup file for installation of the dataduct code
"""
from __future__ import absolute_import
from setuptools import find_packages
from setuptools import setup

from dataduct import __version__ as version

setup(
    name='dataduct',
    version=version,
    author='Coursera Inc.',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    namespace_packages=['dataduct'],
    include_package_data=True,
    url='https://github.com/coursera/dataduct',
    long_description=open('README.rst').read(),
    author_email='data-infra@coursera.org',
    license='Apache License 2.0',
    description='DataPipeline for Humans',
    install_requires=[
    'pytimeparse>=1.1.8',
    'requests>=2.21.0',
    'six>=1.12.0',
    'boto>=2.49.0',
    'python-dateutil>=2.7.5',
    'matplotlib>=3.0.2',
    'pandas>=0.23.4',
    'psycopg2>=2.7.6.1',
    'pyparsing>=2.3.0',
    'pytimeparse>=1.1.8',
    'PyYAML>=3.13',
    'testfixtures>=6.4.1',
    'pyprind>=2.11.2',
    'pandas>=0.23.4',
    'boto3>=1.9.113'
    ],
    scripts=['bin/dataduct'],
    classifiers=[
        'Development Status :: UnStable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS 9',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Unix Shell',
        'Topic :: Database',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities',
    ],
)
