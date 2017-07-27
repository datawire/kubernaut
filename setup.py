from setuptools import setup, find_packages

setup(
    name='kubernaut',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requirements'
    ],
    entry_points='''
        [console_scripts]
        kubernaut=kubernaut.cli:cli
    ''',
)
