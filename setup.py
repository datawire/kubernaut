import versioneer

from setuptools import setup, find_packages

setup(
    name="kubernaut",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "click",
        "requests"
    ],
    entry_points="""
        [console_scripts]
        kubernaut=kubernaut.cli:cli
    """,
    author="datawire.io",
    author_email="dev@datawire.io",
    url="https://github.com/datawire/kubernaut",
    download_url="https://github.com/datawire/kubernaut/tarball/{}".format(versioneer.get_version()),
    keywords=[
        "testing",
        "development",
        "kubernetes",
        "microservices"
    ],
    classifiers=[],
)
