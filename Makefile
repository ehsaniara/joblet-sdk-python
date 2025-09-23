# Joblet SDK Python - Development Makefile
#
# This Makefile provides convenient commands for development tasks.
# Run 'make help' to see available commands.

.PHONY: help setup install test clean lint format type-check proto-gen proto-clean dev-deps run-example

# Default target
help: ## Show this help message
	@echo "Joblet SDK Development Commands:"
	@echo "================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Quick start:"
	@echo "  make setup     # Complete development setup"
	@echo "  make test      # Run tests"
	@echo "  make example   # Run demo"

setup: ## Complete development environment setup
	@echo "🚀 Setting up development environment..."
	python setup_dev.py

install: ## Install package in development mode
	pip install -e .

dev-deps: ## Install development dependencies
	pip install -e .[dev]

proto-gen: ## Regenerate protocol buffer files
	@echo "🔄 Regenerating proto files..."
	python scripts/generate_proto.py --force

proto-clean: ## Clean generated proto files
	@echo "🧹 Cleaning proto files..."
	rm -f joblet/*_pb2.py joblet/*_pb2_grpc.py joblet/*_pb2.pyi
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

proto-list: ## List available proto versions
	python scripts/generate_proto.py --list-tags

test: ## Run tests
	@echo "🧪 Running tests..."
	pytest tests/ -v

test-cov: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	pytest tests/ --cov=joblet --cov-report=html --cov-report=term-missing

lint: ## Run code linting
	@echo "🔍 Running linters..."
	flake8 joblet examples tests
	bandit -r joblet

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	black joblet examples tests scripts
	isort joblet examples tests scripts

format-check: ## Check code formatting without applying changes
	@echo "🔍 Checking code format..."
	black --check joblet examples tests scripts
	isort --check-only joblet examples tests scripts

type-check: ## Run type checking with mypy
	@echo "🔍 Running type checks..."
	mypy joblet

security-check: ## Run security checks
	@echo "🔒 Running security checks..."
	safety check
	bandit -r joblet

example: ## Run the enhanced demo
	@echo "🚀 Running enhanced demo..."
	python examples/demo_with_guidance.py

example-basic: ## Run the basic example
	@echo "🚀 Running basic example..."
	python examples/basic_job.py

clean: ## Clean build artifacts and caches
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete

build: ## Build distribution packages
	@echo "📦 Building packages..."
	python -m build

build-check: ## Check build quality
	@echo "🔍 Checking build quality..."
	python -m twine check dist/*

install-local: ## Install from local build
	pip install dist/*.whl

pre-commit: format lint type-check test ## Run all pre-commit checks
	@echo "✅ All pre-commit checks passed!"

ci: format-check lint type-check test security-check ## Run all CI checks
	@echo "✅ All CI checks passed!"

dev-server-check: ## Check if development server is available
	@echo "🔍 Checking development server..."
	python -c "from joblet import JobletClient; client = JobletClient(); print('✅ Server available' if client.health_check() else '❌ Server not available')" 2>/dev/null || echo "❌ Server not available or connection failed"

docs-deps: ## Install documentation dependencies (if we add docs later)
	pip install sphinx sphinx-rtd-theme

# Development workflow shortcuts
quick-test: install test ## Quick install and test
dev: setup example ## Full setup and run example
rebuild: clean proto-clean proto-gen install ## Clean rebuild everything