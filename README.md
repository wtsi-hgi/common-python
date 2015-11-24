# Common Python used in HGI projects


## How to use in your project
### Include the `hgicommon` library
Link to use in ``/requirements.txt`` or in your ``/setup.py`` script:
```
git+https://github.com/wtsi-hgi/common-python.git@master#egg=hgicommon
```
*See more information about how to use packages not on PyPI in [this documentation about specifying dependencies]
(http://python-packaging.readthedocs.org/en/latest/dependencies.html#packages-not-on-pypi).*


## How to develop
### Testing
#### Locally
To run the tests, use ``./scripts/run-tests.sh`` from the project's root directory. This script will use ``pip`` to 
install all requirements for running the tests (use `virtualenv` if necessary).

#### Using Docker
From the project's root directory:
```
$ docker build -t wtsi-hgi/common-python/test -f docker/tests/Dockerfile .
$ docker run wtsi-hgi/common-python/test
```