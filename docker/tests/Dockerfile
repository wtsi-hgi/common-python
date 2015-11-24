FROM python:3.5
MAINTAINER Colin Nolan <hgi@sanger.ac.uk>

COPY . /common-python
WORKDIR common-python

RUN pip install -r requirements.txt
RUN pip install -r test_requirements.txt

CMD ["./scripts/run-tests.sh"]