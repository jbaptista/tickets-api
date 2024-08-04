prun := "poetry run"
module := "tickets_api"

# Install dependencies
install:
	poetry install

# Run app in development mode
dev:
  {{ prun }} uvicorn  {{ module }}.main:app --reload

# Run tests
test *args:
  {{ prun }} pytest {{ args }}

# build docker image
build:
  docker build -t {{ module }} .

# run docker container
run-docker: build
  docker run -p 8000:8000 {{ module }}
