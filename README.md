# Tickets API

API responsible for management of support tickets. 

## Funcionalities
 - CRUD of Tickets
 - CRUD of Categories
 - Categories can have nested subcategories
 - Tickets are associated a category and a subcategory
 - Tickets have a severity (1 = ISSUE HIGH, 2 = HIGH, 3 = MEDIUM, 4 = LOW)
 - When a ticket is created, a attendant is randomly selected from a external service

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
 - `docker compose up --build -d && docker compose logs app -f` or `just dev-docker`

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

## Folder Structure

|
+-- migrations - used by alembic to manage migrations
+-- tests - test files
+-- tickets_api - main project codebase
|   +-- clients - external services clients
|   +-- database - database models
|   +-- routers - API routers
|   +-- schemas - data schemas models to data transfer between layers
|   +-- service - services by context with business logic
|   +-- utils - utility tools
|   app_factory.py - build app and dependencies
|   config.py - manage configuration from env variables
|   main.py - entrypoint

## Environment variables
Project is configured by environment vars. Default values was setted to facilitate development, but if a .env is present, will be loaded.

.env example:
```
IS_LOCAL=
LOG_LEVEL=
VERSION=
DATABASE__USER=
DATABASE__PASSWORD=
DATABASE__HOST=
DATABASE__PORT=
DATABASE__DB_NAME=
ACCOUNT_SERVICE_URL=
```

## Migrations
Migrations are managed by alembic. With correct database variables, the following commands can be used:

 - `just gen-migration`: Generate a new migration based on changes on the database model
 - `just migrate`: apply all pending migrations