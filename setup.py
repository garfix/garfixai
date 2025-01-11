from setuptools import setup, find_packages

setup(
    scripts=['bin/server', 'bin/client', 'bin/r'],
    name='computer',
    version='0.1.0',
    package_dir='./computer',
    # packages=find_packages(),
)
