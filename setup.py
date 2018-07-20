from setuptools import setup, find_packages


setup(
    name="kubernaut",
    version="v1alpha2",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "click==6.7",
        "requests==2.18.4",
        "scout.py==0.1.5",
        "pathlib2==2.3.0"
    ],
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
