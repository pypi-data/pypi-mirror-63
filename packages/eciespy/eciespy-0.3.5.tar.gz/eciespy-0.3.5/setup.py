"""
 _______  _______ _________ _______  _______  _______
(  ____ \(  ____ \\__   __/(  ____ \(  ____ \(  ____ )|\     /|
| (    \/| (    \/   ) (   | (    \/| (    \/| (    )|( \   / )
| (__    | |         | |   | (__    | (_____ | (____)| \ (_) /
|  __)   | |         | |   |  __)   (_____  )|  _____)  \   /
| (      | |         | |   | (            ) || (         ) (
| (____/\| (____/\___) (___| (____/\/\____) || )         | |
(_______/(_______/\_______/(_______/\_______)|/          \_/

"""
from setuptools import setup, find_packages
from setuptools.command.install import install

import os

here = os.path.abspath(os.path.dirname(__file__))
about = {}  # type: dict

with open(os.path.join(here, "ecies", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    long_description = f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG", "").lstrip("v")

        if tag != about["__version__"]:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, about["__version__"]
            )
            os.sys.exit(info)


setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    packages=find_packages(),
    install_requires=[
        "coincurve>=13.0,<14.0",
        "eth-keys>=0.3.1,<0.4.0",
        "pycryptodome>=3.9,<4.0",
    ],
    python_requires=">=3.5.3",
    entry_points={"console_scripts": ["eciespy = ecies.__main__:main"]},
    keywords=[
        "secp256k1",
        "crypto",
        "elliptic curves",
        "ecies",
        "bitcoin",
        "ethereum",
        "cryptocurrency",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Security :: Cryptography",
    ],
    cmdclass={"verify": VerifyVersionCommand},
)
