.PHONY: help install dev test lint proto clean test-package build

# Default target
help:
	@echo "Available commands:"
	@echo "  dev          - Set up development environment"
	@echo "  test         - Run tests with coverage"
	@echo "  lint         - Run all code quality checks"
	@echo "  test-package - Test package installation (CI-like, recommended before release)"
	@echo "  build        - Build distribution packages"
	@echo "  proto        - Regenerate protobuf files"
	@echo "  clean        - Remove build artifacts"

# Development setup
dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing (with coverage by default)
test:
	pytest tests/ -v --cov=joblet --cov-report=term-missing

# Code quality (exactly what CI runs)
lint:
	pre-commit run --all-files

# Proto generation (simplified)
proto:
	python scripts/generate_proto.py
	@echo "Running lint to format generated files..."
	pre-commit run --files joblet/*_pb2* || true

# Test package installation (replicates CI environment)
test-package:
	@echo "Testing package installation (CI-like)..."
	bash scripts/test-package.sh

# Build distribution packages
build:
	python3 -m build

# Cleanup
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage __pycache__
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
