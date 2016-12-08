#!/bin/env python3
import sys
from setuptools import setup, find_packages

def readme():
    with open('README.rst', 'r') as f:
        return f.read()

pack_name = 'webbed'

with open(pack_name + '/version.py', 'r') as file:
    # getting __version__ variable
    exec(file.read())

print('Current version:', __version__)
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

__version__ = '.'.join(version)
print('New version:', __version__)
with open(pack_name + '/version.py', 'w') as f:
    f.write('__version__ = "' + __version__ + '"')

setup(
    name=pack_name,
    packages=find_packages(),
    version=__version__,
    include_package_data=True,
    license='MIT',
    description='Allows the execution of python code within any file',
    long_description=readme(),
    author='Christoffer Zakrisson',
    author_email='christoffer_zakrisson@hotmail.com',
    # url='https://github.com/Zaeb0s/ez-crypt',
    keywords=['webbed', 'script', 'file'],
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 3.5',
                 'Operating System :: POSIX :: Linux',
                    'Operating System :: POSIX :: Linux',
                 'License :: OSI Approved :: MIT License'],

    install_requires=[]
)


print('Installed version:', __version__)


