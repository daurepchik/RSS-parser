"""A setuptools based setup module"""
from setuptools import setup, find_packages

setup(
    name="rss-reader",
    version='0.2',
    description="RSS reader",
    author="Dauren Aidenov",
    author_email="daurenblin5@gmail.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "autopep8",
        "beautifulsoup4",
        "bs4",
        "build",
        "colorama",
        "inflect",
        "lxml",
        "packaging",
        "pep517",
        "pycodestyle",
        "pyparsing",
        "soupsieve",
        "toml",
        "tomli",
    ],
    entry_points={
        "console_scripts": ['rss_reader=src.rss_reader:main']
    }
)
