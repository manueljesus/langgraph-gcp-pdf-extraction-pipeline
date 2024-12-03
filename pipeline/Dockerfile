FROM python:3.12.7-slim-bookworm AS builder

WORKDIR /workdir

# Install dependencies
COPY requirements.txt requirements-test.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt -r requirements-test.txt


FROM python:3.12.7-slim-bookworm

WORKDIR /workdir

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY requirements.txt requirements-test.txt ./
COPY src/ test/ ./

ENV PYTHONPATH = /workdir:$PYTHONPATH

RUN useradd -m pipeline
RUN chown -R pipeline:pipeline /workdir
RUN chown -R pipeline:pipeline /usr/local/lib/python3.12/site-packages
RUN chown -R pipeline:pipeline /usr/local/bin
USER pipeline

EXPOSE 8080

CMD [ "functions-framework", "--source=src/main.py", "--target=pipeline" ]
