"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-orion-model',  
    version='0.92',
    description='A Django model to manage Fiware Orion Entities as local models ', 
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  
    install_requires=['django', 'pyfiware'],
    keywords='Fiware Orion development', 
    long_description=long_description, 
    long_description_content_type='text/markdown',  
    url='https://github.com/deusto-tech/django-orion-model/', 
    author='Josu Bermudez', 
    author_email='josu.bermudez@deusto.es',  
    project_urls={ 
        'Bug Reports': 'https://github.com/deusto-tech/django-orion-model/issues',
        'Source': 'https://github.com/deusto-tech/django-orion-model',
    },
    classifiers=[  
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 2.0',
    ],
    )
