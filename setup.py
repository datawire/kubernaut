import os
import versioneer

from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)

with open(os.path.join(ROOT_DIR, "requirements.txt")) as fp:
    install_requirements = [i.strip() for i in list(fp)
                            if i.strip() and not i.strip().startswith("#")]

setup(
    name="kubernaut",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=install_requirements,
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
