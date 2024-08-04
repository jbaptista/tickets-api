FROM python:3.12-alpine3.20

WORKDIR /usr/src/app

ENV PORT=8000
RUN apk update && \
    apk add --no-cache libffi-dev build-base python3-dev rust cargo openssl-dev && \
    apk del curl

RUN pip install "poetry~=1.7.1"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false 
COPY tickets_api ./tickets_api
RUN poetry install --no-dev

CMD uvicorn tickets_api.main:app --host '0.0.0.0' --port $PORT --log-level info