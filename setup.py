from setuptools import find_namespace_packages, setup

# info about package management: https://setuptools.pypa.io/en/latest/userguide/package_discovery.html

setup(
    name='garfixai',
    version='0.1.0',
    package_dir={"": "src"},
    packages=find_namespace_packages(where='src'),
     entry_points={
        'console_scripts': [
            'r=client.cli:main',
            'server=server.server:main'
        ]
    },
)
