# Joblet Python SDK - Development Makefile

.PHONY: help proto proto-list proto-clean install install-dev test lint format type-check clean all

# Default target
help:
	@echo "Joblet Python SDK - Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Proto Management:"
	@echo "  proto           Generate proto bindings from latest joblet-proto"
	@echo "  proto-list      List available joblet-proto versions"
	@echo "  proto-clean     Remove generated proto files"
	@echo ""
	@echo "Development:"
	@echo "  install         Install SDK in development mode"
	@echo "  install-dev     Install with development dependencies"
	@echo "  test            Run test suite"
	@echo "  lint            Run linting checks"
	@echo "  format          Format code with black and isort"
	@echo "  type-check      Run type checking with mypy"
	@echo "  clean           Clean up generated files and caches"
	@echo ""
	@echo "Examples:"
	@echo "  make proto PROTO_VERSION=v1.0.1   # Use specific proto version"
	@echo "  make install-dev                  # Setup development environment"
	@echo "  make test                         # Run tests"

# Proto file generation
proto:
	@echo "🔄 Generating proto bindings..."
ifdef PROTO_VERSION
	python scripts/generate_proto.py --version $(PROTO_VERSION)
else
	python scripts/generate_proto.py
endif
	@echo "✅ Proto generation complete!"

proto-list:
	@echo "📋 Available joblet-proto versions:"
	@python scripts/generate_proto.py --list-tags

proto-clean:
	@echo "🧹 Cleaning generated proto files..."
	@rm -f joblet/joblet_pb2.py
	@rm -f joblet/joblet_pb2_grpc.py
	@rm -f joblet/joblet_pb2.pyi
	@rm -f joblet/_proto_generation_info.py
	@echo "✅ Proto files cleaned!"

# Installation
install:
	@echo "📦 Installing Joblet SDK in development mode..."
	@pip install -e .
	@echo "✅ Installation complete!"

install-dev:
	@echo "📦 Installing Joblet SDK with development dependencies..."
	@pip install -e ".[dev]"
	@echo "✅ Development installation complete!"

# Development tools
test:
	@echo "🧪 Running test suite..."
	@python -m pytest tests/ -v --cov=joblet --cov-report=term-missing
	@echo "✅ Tests complete!"

lint:
	@echo "🔍 Running linting checks..."
	@python -m flake8 joblet/ examples/ scripts/ || echo "⚠️  Linting issues found"
	@python -m black --check joblet/ examples/ scripts/ || echo "⚠️  Code formatting issues found"
	@python -m isort --check-only joblet/ examples/ scripts/ || echo "⚠️  Import sorting issues found"
	@echo "✅ Linting complete!"

format:
	@echo "🎨 Formatting code..."
	@python -m black joblet/ examples/ scripts/
	@python -m isort joblet/ examples/ scripts/
	@echo "✅ Code formatting complete!"

type-check:
	@echo "🔍 Running type checks..."
	@python -m mypy joblet/ || echo "⚠️  Type checking issues found"
	@echo "✅ Type checking complete!"

# Cleanup
clean:
	@echo "🧹 Cleaning up generated files and caches..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete!"

# Comprehensive development workflow
all: proto-clean proto install-dev lint type-check test
	@echo "🎉 Full development workflow complete!"

# Development workflow without proto regeneration
dev: install-dev lint type-check test
	@echo "🎉 Development workflow complete!"

# Quick check (no installation)
check: lint type-check
	@echo "🎉 Code quality checks complete!"