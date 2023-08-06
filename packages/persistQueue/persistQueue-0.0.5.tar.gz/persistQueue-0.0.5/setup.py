# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = "0.0.5"

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='persistQueue',
    version=VERSION,
    license=license,
    author='Logicalis',
    author_email='eugenio@eugenio.io',
    url='http://re91877z@10.55.200.102:7990/scm/edge/lib-persist-queue.git',
    download_url=''.format(VERSION),
    description='Persist Queue',
    long_description=readme,
    keywords=['queue', 'persistence', 'iot', 'embedded'],
    packages=['persistQueue'],
    install_requires=['persist-queue']
)

