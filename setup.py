from setuptools import setup, find_packages

setup(
    name="hgi-common-python",

    version="0.1.0",

    author="Colin Nolan",
    author_email="hgi@sanger.ac.uk",

    packages=find_packages(exclude=["tests"]),

    url="https://github.com/wtsi-hgi/common-python",

    license="LICENSE",

    description="Common Python code used in HGI.",
    long_description=open("README.md").read(),

    test_suite="hgicommon.tests"
)
