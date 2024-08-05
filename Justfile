prun := "poetry run"
module := "tickets_api"
code_folders := module + " tests"

# Install dependencies
install:
	poetry install

# Run app in development mode
dev:
  {{ prun }} uvicorn  {{ module }}.main:app --reload

# Format code
fmt *args:
  {{prun}} ruff format {{ args }} {{ code_folders }}

# Check if code is in the standard format
fmt-ci: (fmt "--diff")

lint *args:
  {{ prun }} ruff check {{ args }} {{ code_folders }}

# Run tests
test *args:
  {{ prun }} pytest {{ args }}

# Run static type checker
typecheck *args:
	{{ prun }} mypy {{ args }} {{ code_folders }}

# Run all static checks
check: fmt lint typecheck test

# build docker image
build:
  docker build -t {{ module }} .

# run docker container
run-docker: build
  docker run -p 8000:8000 {{ module }}
