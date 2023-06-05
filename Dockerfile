FROM python:3.10.11

RUN python3 -m pip install --upgrade pip

RUN useradd -ms /bin/bash coinbase

COPY --chown=coinbase . /app/
WORKDIR /app
RUN pip install -r requirements.txt

USER coinbase