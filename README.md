[![Build Status](https://travis-ci.org/wtsi-hgi/python-common.svg)](https://travis-ci.org/wtsi-hgi/python-common)
[![codecov.io](https://codecov.io/gh/wtsi-hgi/python-common/graph/badge.svg)](https://codecov.io/github/wtsi-hgi/python-common)

# Common Python used in HGI projects

## How to use
### Prerequisites
- Python >= 3.5

### Installation
This library can be installed directly from GitHub:
```bash
$ pip3 install git+https://github.com/wtsi-hgi/python-common.git@<commit_id_or_branch_or_tag>#egg=hgicommon
```

To declare this library as a dependency of your project, add it to your `requirement.txt` file.


## Development
### Setup
Install both library dependencies and the dependencies needed for testing:
```bash
$ pip3 install -q -r requirements.txt
$ pip3 install -q -r test_requirements.txt
```

### Testing
Using nosetests, in the project directory, run:
```bash
$ nosetests -v
```

To generate a test coverage report with nosetests:
```bash
$ nosetests -v --with-coverage --cover-package=hgicommon --cover-inclusive
```


## License
[LGPL](LICENSE.txt).

Copyright (c) 2015, 2016 Genome Research Limited