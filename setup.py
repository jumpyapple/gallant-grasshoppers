"""
Setup file.

Base on https://python-packaging.readthedocs.io/en/latest/index.html
"""
from setuptools import setup


def readme() -> str:
    """Read in text in README.md file."""
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="gallant-grasshoppers",
    version="0.0.1",
    description="Python Discord Summer 2021 Code Jam",
    long_description=readme(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://github.com/StackedQueries/gallant-grasshoppers",
    author="Burned, Breno Cabral, jumpyapple, KnoxZingVille, zachkaupp, Zix",
    author_email="",
    license="MIT",
    packages=["gallant_grasshoppers"],
    install_requires=["blessed",],
    entry_points={
        "console_scripts": ["gallant-grasshoppers=gallant_grasshoppers.__main__:main"]
    },
    zip_safe=False,
)
