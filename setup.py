import versioneer

from setuptools import setup, find_packages

setup(
    name='kubernaut',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        kubernaut=kubernaut.cli:cli
    ''',
)
