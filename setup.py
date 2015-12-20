# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='acsclient',
    version='0.1',
    description="Access Cisco ACS 5.6 API",
    classifiers=[],
    keywords='cisco acs access control',
    author='Nathan Gotz',
    author_email='nathan@gotz.co',
    url='https://github.com/nlgotz/acsclient',
    license='Apache 2.0',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        ],
    setup_requires=[],
    namespace_packages=[],
    )
