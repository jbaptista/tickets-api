# Tickets API

API responsible for managing support tickets

## Requirements

- [Python 3.12](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) - project/package manager
- [Just](https://github.com/casey/just)- task runner

## Stack

This Python project was built using the following technologies
 - [FastAPI](https://fastapi.tiangolo.com/) as web framework
 - [SqlAlchemy](https://www.sqlalchemy.org/) as ORM
 - [Alembic] as database migration tool
 - [Pydantic](https://docs.pydantic.dev/latest/) as data validator
 - [Pytest](https://pytest.org) as tests framework
 - [Ruff](https://github.com/astral-sh/ruff) as code formatter and linter
 - [MyPy](https://mypy-lang.org/) as static type checker

## Setup and Run Locally

After install requirements, run
 - `just install`
 - `just dev`

 or, if you want to use docker
 - `docker compose up --build -d && docker compose logs app -f`

A container with postgres will be started and the app will run on http://localhost:8000

 ## Docs and Examples
 The OpenAPI Docs (Swagger) are in http://localhost:8000/docs

 [This postman collection](https://www.postman.com/navigation-geologist-23746087/workspace/tickets-api/request/15351339-7dbfca81-184a-4a12-bda0-b2ccb07159a9?action=share&creator=15351339&ctx=documentation) contains examples of this api calls

 ## Tests and Quality Checkers
 - `just test` Run unit tests with pytest
 - `just lint` Run lint with Ruff
 - `just fmt` Format code with Ruff
 - `just typecheck` Check static types with mypy
 - `just check` Run all quality checkers above