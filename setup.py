#! coding: utf-8

from setuptools import find_packages
from setuptools import setup


setup(
    name='bombril',
    version='0.2.0',
    author='Eduardo Tenório',
    author_email='embatbr@gmail.com',
    license='WTFPL',
    packages=[
        'bombril',
        'bombril.aws',
        'bombril.cryptography'
    ],
    include_package_data=True,
    install_requires=[
        'boto3==1.9.80',
        'cryptography==2.4.2'
    ]
)
