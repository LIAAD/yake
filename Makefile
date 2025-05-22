install:
	uv pip install --upgrade pip
	uv pip install -e .

install-dev:
	uv pip install --upgrade pip
	uv pip install -e ".[dev]"

test:
	uv run pytest -vv --cov=yake test_*.py

format:
	uv run black .

lint:
	uv run ruff check --fix .
	uv run ruff check .
	uv run flake8 yake/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:
	uv build

deploy:
	uv build
	uv publish

all: install-dev lint test format

.PHONY: install install-dev test format lint clean build deploy all