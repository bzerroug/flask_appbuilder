import os
import re

from setuptools import setup, find_packages


MODULE_NAME = 'meteo'

DEPENDENCIES = [
    'flask-appbuilder',
    'psycopg2',
    'pandas',
    'urllib3',
    'google-api-python-client',
    'pyasn1>=0.1.8',
    'splunk-sdk',
]

TEST_DEPENDENCIES = [
]


def get_version():
    """ Read package version number from package's __init__.py. """
    with open(os.path.join(
        os.path.dirname(__file__), MODULE_NAME, '__init__.py'
    )) as init:
        for line in init.readlines():
            res = re.match(r'^__version__ = [\'"](.*)[\'"]$', line)
            if res:
                return res.group(1)


def get_long_description():
    """ Read description from README. """
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as stream:
        return stream.read()


setup(
    name=MODULE_NAME,
    version=get_version(),
    description='Graphs for dataware',
    long_description=get_long_description(),
    author='Bachir Zerroug',
    author_email='bzerroug@auchandirect.net',
    url='http://www.auchandirect.fr',
    packages=find_packages(),
    install_requires=DEPENDENCIES,
    tests_require=DEPENDENCIES + TEST_DEPENDENCIES,
    test_suite=MODULE_NAME + '.tests',
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    license='Proprietary',
    entry_points={
        'console_scripts': [
            'dataware-meteo = meteo.run:debug',
        ],
    },
)