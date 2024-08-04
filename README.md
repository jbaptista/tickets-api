# Tickets API

API responsible for managing support tickets

## Requirements

- [Python 3.12](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) - project/package manager
- [Just](https://github.com/casey/just)- task runner

## Setup and Run Locally

After install requirements, run
 - `just install`
 - `just dev`

 or, if you want to use docker
 - `just run-docker`

 ## Tests and Quality Checkers
 - `just test` Run unit tests with pytest
 - `just lint` Run lint with Ruff
 - `just fmt` Format code with Ruff
 - `just typecheck` Check static types with mypy
 - `just check` Run all quality checkers above