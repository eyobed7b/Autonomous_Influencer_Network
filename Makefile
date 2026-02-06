.PHONY: setup update format test clean docker-build docker-run

# Project variables
IMAGE_NAME = project-chimera

# Environment Setup
setup:
	@echo "Syncing dependencies with uv..."
	uv sync

update:
	@echo "Updating dependencies..."
	uv lock --upgrade
	uv sync

# Development Tools
format:
	@echo "Formatting code with Black..."
	uv run black .

test:
	@echo "Running tests..."
	uv run pytest

# Docker Operations
spec-check:
	@echo "Checking specs..."
	python tools/check_specs.py

docker-test:
	@echo "Running tests in Docker..."
	docker run --rm $(IMAGE_NAME) uv run pytest

docker-build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) .

docker-run:
	@echo "Running Docker container..."
	docker run --rm $(IMAGE_NAME)

# Cleanup
clean:
	@echo "Cleaning up..."
	@if exist .venv rmdir /s /q .venv
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist __pycache__ rmdir /s /q __pycache__
