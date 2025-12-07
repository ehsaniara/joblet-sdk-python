# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2025-12-05

### Added
- Updated proto files to joblet-proto v2.5.0
- New telemetry API support (proto only, implementation pending):
  - `StreamJobTelemetry` - Stream live telemetry (metrics + eBPF activity)
  - `GetJobTelemetry` - Query historical telemetry
  - `TelemetryEvent`, `TelemetryMetricsData`, `TelemetryExecData`, `TelemetryConnectData`, `TelemetryFileData` messages

## [3.0.0] - 2025-12-04

### Breaking Changes
- Removed workflow functionality (run_workflow, get_workflow_status, list_workflows, get_workflow_jobs)
- Removed WorkflowNotFoundError exception
- Updated proto files to joblet-proto v2.4.0

### Changed
- Updated documentation to remove workflow references
- Cleaned up docstrings in services.py and client.py

## [2.0.0] - 2025-10-13

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

## [1.1.5] - Previous Release

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
