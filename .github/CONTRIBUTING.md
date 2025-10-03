# Contributing to Joblet Python SDK

Thanks for your interest in contributing!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/ehsaniara/joblet-sdk-python.git
cd joblet-sdk-python

# Install dev dependencies and pre-commit hooks
make dev
```

## Making Changes

1. **Create a branch** for your feature or fix
2. **Write tests** for your changes
3. **Run tests and linting** before committing:
   ```bash
   make lint    # Run all code quality checks
   make test    # Run tests with coverage
   ```
4. **Commit your changes** - pre-commit hooks will automatically format your code
5. **Submit a pull request**

## Code Standards

- Follow PEP 8 style guide (enforced by black/flake8)
- Add type hints where appropriate
- Write docstrings for public APIs
- Maintain test coverage above 70%

## Pull Request Process

1. Ensure all tests pass and code is properly formatted
2. Update documentation if adding new features
3. Add entries to CHANGELOG.md under `[Unreleased]`
4. PRs require passing CI checks before merging

## Questions?

Open an issue or discussion on GitHub.
