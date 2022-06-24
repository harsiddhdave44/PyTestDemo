FROM python:alpine

COPY . /python-pytest

WORKDIR /python-pytest

ENV pytest_marker=

RUN pip install --no-cache-dir -r requirements.txt

RUN ["pytest", "-v", "--html=./reports/report.html"]

CMD tail -f /dev/null