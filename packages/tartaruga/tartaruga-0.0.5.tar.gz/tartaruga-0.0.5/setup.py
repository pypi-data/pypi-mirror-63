import setuptools
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='tartaruga',
    version='0.0.5',
    author='Devmons s.r.o.',
    description='tartaruga ratelimiter',
    license='GPL3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['tartaruga'],
    package_data={'tartaruga': ['tartaruga.lua']},
    install_requires=[
        'redis>=3.3.11'
    ],
)

