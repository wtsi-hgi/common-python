from setuptools import setup, find_packages

setup(
    name="hgi-python-common",

    version="0.1.0",

    author="Colin Nolan",
    author_email="hgi@sanger.ac.uk",

    packages=find_packages(exclude=["tests"]),

    url="https://github.com/wtsi-hgi/python-common",

    license="LICENSE",

    description="Common Python code used in HGI.",
    long_description=open("README.md").read(),

    install_requires=[x for x in open("requirements.txt").read().splitlines() if "://" not in x],
    dependency_links=[x for x in open("requirements.txt").read().splitlines() if "://" in x],

    test_suite="hgicommon.tests"
)
