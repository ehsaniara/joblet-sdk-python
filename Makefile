.PHONY: help install dev clean test lint format proto check ci

# Default target
help:
	@echo "Available targets:"
	@echo "  install     - Install package in production mode"
	@echo "  dev         - Install package in development mode with all dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run pre-commit hooks (formatting + linting)"
	@echo "  format      - Auto-fix formatting issues"
	@echo "  proto       - Regenerate protobuf files"
	@echo "  check       - Run all checks (lint + test)"
	@echo "  clean       - Remove build artifacts and cache"

# Installation
install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=joblet --cov-report=term-missing

# Code quality - simplified to just use pre-commit
lint:
	pre-commit run --all-files

format:
	# Auto-fix what we can
	black .
	isort .
	# Then check what's left
	pre-commit run --all-files

# Proto generation
proto:
	python scripts/generate_proto.py
	# Format generated files
	black joblet/joblet_pb2*.py joblet/proto/ joblet/local_joblet_pb2.pyi || true

# Combined check for CI
check: lint test

# CI simulation - run exactly what CI runs
ci:
	pre-commit run --all-files
	pytest tests/ -v --tb=short

# Cleanup
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete
