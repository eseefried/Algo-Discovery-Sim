FROM python:3.12-slim-bookworm@sha256:6a0e06f5ba0b373d051aabd3fffb9b873f27f9a2a3a14bcbe37dee6f0e3bbc70
COPY requirements.txt /tmp/requirements.txt
RUN pip install --disable-pip-version-check --no-cache-dir --require-hashes -r /tmp/requirements.txt
USER 65534:65534
WORKDIR /tmp
