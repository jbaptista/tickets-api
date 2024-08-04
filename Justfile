module := "tickets_api"

# Install dependencies
install:
	poetry install

# Run app in development mode
dev:
  poetry run uvicorn  {{ module }}.main:app --reload