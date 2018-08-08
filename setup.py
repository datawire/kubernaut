import versioneer

from setuptools import setup, find_packages


setup(
    name="kubernaut",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[],
    entry_points="""
        [console_scripts]
        kubernaut=kubernaut.cli:cli
    """,
    author="datawire.io",
    author_email="dev@datawire.io",
    url="https://github.com/datawire/kubernaut",
    keywords=[
        "testing",
        "development",
        "kubernetes",
        "microservices"
    ],
    classifiers=[],
)
