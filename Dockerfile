FROM python:alpine

COPY . /python-pytest

WORKDIR /python-pytest

RUN pip install --no-cache-dir -r requirements.txt

# RUN ["pytest", "-v", "-m account" ]

# CMD tail -f /dev/null

CMD ["pytest", "-v", "-m account" ]