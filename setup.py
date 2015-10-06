
from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
long_descrioption=[]
# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages=['tacklebox','tacklebox.tools','tacklebox.components']


setup(
    name="tacklebox",
    version="0.0.1",
    description="Toolkit for bringing your hardware with you into Docker containers",
    long_description = long_description,
    author="Jonathan Weisz",
    author_email='jweisz@cs.columbia.edu',
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Dev Ops',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
    ],
    keywords='docker, gpu support',
    packages=packages,
    py_modules=['helper'],
    zip_safe=False
    )


