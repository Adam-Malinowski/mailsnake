#!/usr/bin/env python
from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'mailchimp api wrapper 1.4'

setup(
    name = 'mailsnake',
    version = '1.4.2.0',
    description = """MailChimp API v1.4 wrapper for Python.""",
    author = 'John-Kim Murphy',
    url = "https://github.com/leftium/mailsnake",
    packages = find_packages(),
    download_url = "http://pypi.python.org/pypi/mailsnake/",
    classifiers = CLASSIFIERS,
    keywords = KEYWORDS,
    zip_safe = True,
    install_requires = ['requests'],
)
