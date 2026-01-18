# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.5.1] - 2025-01-18

### Added

- **Environment variable support for certificates**: Set `JOBLET_CA_CERT`, `JOBLET_CLIENT_CERT`, `JOBLET_CLIENT_KEY` environment variables with certificate content (PEM format)
- **AWS Secrets Manager support**: Load certificates from AWS Secrets Manager using `aws_secret_name` (single JSON secret) or `aws_secret_prefix` (separate secrets)
- **AWS Parameter Store (SSM) support**: Load certificates from AWS Parameter Store using `aws_ssm_prefix`
- New optional dependency group `[aws]` for AWS integration: `pip install joblet-sdk-python[aws]`
- `EnvironmentCertProvider`, `AWSSecretsManagerProvider`, `AWSParameterStoreProvider` classes for advanced use cases
- Environment variable constants: `ENV_CA_CERT`, `ENV_CLIENT_CERT`, `ENV_CLIENT_KEY`, `ENV_HOST`, `ENV_PORT`
- `COMPATIBILITY.md` documenting version compatibility between SDK, joblet-proto, and Joblet server

### Changed

- Certificate loading now checks multiple sources in order: explicit paths → AWS Secrets Manager → AWS Parameter Store → environment variables → config file
- Moved `grpcio-tools` from runtime to dev dependencies (reduces install size for end users)
- Improved error messages to list all available certificate sources
- Synced dependency versions between `pyproject.toml` and `requirements.txt`

### Fixed

- grpcio minimum version now correctly set to `>=1.75.1` to match generated proto files

## [2.5.0] - 2025-01-09

### Added

- New `JobOperationError` exception for job operation failures (run, stop, cancel, delete, list)
- New `JobletConnectionError` exception (replaces shadowed `ConnectionError`)
- New `JobletTimeoutError` exception (replaces shadowed `TimeoutError`)
- Input validation for `command` parameter in `run_job()`
- Input validation for `job_uuid` parameter in `get_job_status()`, `stop_job()`, `cancel_job()`, `delete_job()`,
  `get_job_logs()`
- Deprecation warning when using `include_historical=False` in `get_job_logs()`
- Added `__all__` export list to `helpers.py`

### Changed

- `run_job()` now raises `JobOperationError` instead of `JobNotFoundError` on failure
- `stop_job()` now raises `JobOperationError` instead of `JobNotFoundError` on failure
- `cancel_job()` now raises `JobOperationError` instead of `JobNotFoundError` on failure
- `delete_job()` now raises `JobOperationError` instead of `JobNotFoundError` on failure
- `delete_all_jobs()` now raises `JobOperationError` instead of `JobNotFoundError` on failure
- `list_jobs()` now raises `JobOperationError` instead of `JobNotFoundError` on failure

### Deprecated

- `ConnectionError` alias (use `JobletConnectionError` instead)
- `TimeoutError` alias (use `JobletTimeoutError` instead)
- `include_historical` parameter in `get_job_logs()` (server always includes historical logs)

## [2.4.1] - 2025-12-26

### Changed
- Unified `upload()` function that auto-detects files vs directories
- `upload()` now always returns `List[Dict]` for consistent usage with spread operator

### Removed
- `upload_file()` - use `upload()` instead
- `upload_directory()` - use `upload()` instead

### Migration Guide
```python
# Before (v2.4.0)
from joblet import upload_file, upload_directory
uploads=[
    upload_file("./script.py"),
    upload_directory("./data", exclude=["*.pyc"])
]

# After (v2.4.1)
from joblet import upload
uploads=[
    *upload("./script.py"),
    *upload("./data", exclude=["*.pyc"])
]
```

## [2.4.0] - 2025-12-21

### Added
- Updated proto files to joblet-proto v2.5.5
- New runtime build API with OverlayFS-based isolation:
  - `build_runtime()` - Build a runtime from YAML specification with streaming progress
  - `validate_runtime_yaml()` - Validate a runtime YAML specification without building
- Runtime build uses OverlayFS-based chroot isolation ensuring host system is never modified
- Support for 14-phase build pipeline with real-time progress streaming

### Changed
- Runtime builds now use OverlayFS isolation instead of direct host installation
- Build process streams progress events (phase, log, result) for real-time feedback

## [2.3.0] - 2025-12-05

### Added
- Updated proto files to joblet-proto v2.5.0
- New telemetry API support (proto only, implementation pending):
  - `StreamJobTelemetry` - Stream live telemetry (metrics + eBPF activity)
  - `GetJobTelemetry` - Query historical telemetry
  - `TelemetryEvent`, `TelemetryMetricsData`, `TelemetryExecData`, `TelemetryConnectData`, `TelemetryFileData` messages

## [2.2.0] - 2025-12-04

### Breaking Changes
- Removed workflow functionality (run_workflow, get_workflow_status, list_workflows, get_workflow_jobs)
- Removed WorkflowNotFoundError exception
- Updated proto files to joblet-proto v2.4.0

### Changed
- Updated documentation to remove workflow references
- Cleaned up docstrings in services.py and client.py

## [2.1.0] - 2025-10-13

### Added
- Smart log streaming in `get_job_logs()` - automatically fetches historical + live logs (like `rnx job log`)
- Example 05: Smart log streaming demonstration
- `stream_live_logs()` method for live-only log streaming
- PersistService for querying historical logs and metrics (port 50052)
- Example 04: Historical logs and metrics querying with PersistService
- Support for time-range queries, filtering, and pagination in persist queries
- Comprehensive API reference documentation in `docs/API_REFERENCE.md`
- `include_historical` parameter in `get_job_logs()` to control historical log fetching

### Changed
- JobService now accepts persist_service_getter for lazy access to persist functionality
- Improved error handling with graceful fallback when persist service unavailable

### Improved
- Enhanced documentation for all service methods
- Better inline examples showing real-world usage patterns
- Updated examples README with smart log streaming usage

## [2.0.0] - Previous Release

### Added
- Initial Python SDK for Joblet
- Job management (run, stop, cancel, delete, status, logs)
- Workflow support with dependencies
- GPU support (allocation and memory requirements)
- Resource management (volumes, networks, runtimes)
- System monitoring and metrics streaming
- Streaming log support via gRPC
- Configuration via YAML files
- mTLS authentication support
- Comprehensive test suite
- Examples and documentation
