# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = "0.0.7"

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='persistQueue',
    version=VERSION,
    license=license,
    author='logicalis',
    Maintainer='waraujo',
    author_email='eugenio@eugenio.io',
    url='http://re91877z@10.55.200.102:7990/scm/edge/lib-persist-queue.git',
    download_url=''.format(VERSION),
    description='A implementation of Class for Persist Queue',
    long_description=readme,
    keywords=['queue', 'persistence', 'iot', 'embedded'],
    packages=['persistQueue'],
    install_requires=['persist-queue'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ]
)

