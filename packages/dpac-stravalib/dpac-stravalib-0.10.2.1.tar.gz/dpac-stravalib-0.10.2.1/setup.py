# -*- coding: utf-8 -*-
import os.path
import re
import warnings

from setuptools import setup, find_packages

version = '0.10.2.1'

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


news = os.path.join(os.path.dirname(__file__), 'docs', 'news.rst')
news = open(news).read()
parts = re.split(r'([0-9\.]+)\s*\n\r?-+\n\r?', news)
found_news = ''
for i in range(len(parts) - 1):
    if parts[i] == version:
        found_news = parts[i + i]
        break
if not found_news:
    warnings.warn('No news for this version found.')

long_description = """
stravalib is a Python 2.7 and 3.x library that provides a simple API for interacting
with the Strava activity tracking website.
"""

if found_news:
    title = 'Changes in %s' % version
    long_description += '\n%s\n%s\n' % (title, '-' * len(title))
    long_description += found_news

reqs = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))

setup(
    name='dpac-stravalib',
    version=version,
    author='David Pacheco',
    author_email='davidpch@gmail.com',
    url='http://github.com/davidpch/stravalib',
    license='Apache',
    description='Python library for interacting with Strava v3 REST API',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data={'stravalib': ['tests/resources/*']},
    install_requires=reqs,
    tests_require=['nose>=1.0.3'],
    test_suite='stravalib.tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=True
)
