from setuptools import find_namespace_packages, setup

# info about package management: https://setuptools.pypa.io/en/latest/userguide/package_discovery.html

setup(
    scripts=['bin/server', 'bin/client', 'bin/r'],
    name='computer',
    version='0.1.0',
    package_dir={"": "src"},
    packages=find_namespace_packages(where='src'),
)
