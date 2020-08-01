# coding=utf-8

from setuptools import find_packages
from setuptools import setup


setup(
    name='5ch-crawler',
    packages=find_packages(),
    install_requires=[
        'Scrapy',
        'pytz',
    ],
)
