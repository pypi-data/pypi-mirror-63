#! /usr/bin/env python
import os
from setuptools import setup

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules']

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='django-prices-openexchangerates',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description='openexchangerates.org support for django-prices',
    license='BSD',
    version='1.1.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mirumee/django-prices-openexchangerates',
    packages=[
        'django_prices_openexchangerates',
        'django_prices_openexchangerates.management',
        'django_prices_openexchangerates.management.commands',
        'django_prices_openexchangerates.migrations',
        'django_prices_openexchangerates.templatetags'],
    include_package_data=True,
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.11', 'django-prices>=1.0.0', 'prices>=1.0.0'],
    platforms=['any'],
    tests_require=['mock==1.0.1', 'pytest'],
    zip_safe=False)
