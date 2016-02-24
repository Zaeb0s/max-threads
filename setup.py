#!/bin/env python3
# from distutils.core import setup
from setuptools import setup
from maxthreads import __version__
import sys


def readme():
    with open('README.rst') as f:
        return f.read()

print('Current version: ', __version__)
version = __version__.split('.')


if sys.argv[-1] == 'minor':
    version[2] = str(int(version[2]) + 1)
    del sys.argv[-1]
elif sys.argv[-1] == 'major':
    version[1] = str(int(version[1]) + 1)
    version[2] = '0'
    del sys.argv[-1]
elif sys.argv[-1] == 'huge':
    version[0] = str(int(version[0]) + 1)
    version[1] = '0'
    version[2] = '0'
    del sys.argv[-1]


version = '.'.join(version)
with open('maxthreads/version', 'w') as f:
    f.write(version)


setup(
    name='maxthreads',
    packages=['maxthreads'],  # this must be the same as the name above
    version=version,
    include_package_data=True,
    license='MIT',
    description='Python module for queuing threads',
    long_description=readme(),
    author='Christoffer Zakrisson',
    author_email='christoffer_zakrisson@hotmail.com',
    url='https://github.com/Zaeb0s/max-threads', # use the URL to the github repo
    keywords=['max', 'threads', 'thread'], # arbitrary keywords
    classifiers=['Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 3.5',
                 'Operating System :: POSIX :: Linux',
                 'License :: OSI Approved :: MIT License'],
    install_requires=[]
)


print('Installed version: ' + version)
