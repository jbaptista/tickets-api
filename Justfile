prun := "poetry run"
module := "tickets_api"
code_folders := module + " tests"

# Install dependencies
install:
	poetry install

docker-db:
  docker-compose up -d postgres

# Run app in development mode
dev: docker-db migrate
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
run-docker:
  docker-compose up --build -d
  docker-compose exec app alembic upgrade head
  docker-compose logs -f app

# Generates migration script from difference between models and database
gen-migration:
	{{ prun }} alembic revision --autogenerate

# Apply pending migrations to database
migrate:
	{{ prun }} alembic upgrade head
