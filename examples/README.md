# Joblet SDK Examples

This directory contains example scripts demonstrating how to use the Joblet SDK.

## Prerequisites

1. Joblet server running on `localhost:8080`
2. Python 3.9+ with joblet-sdk-python installed

## Examples

### 01_basic_usage.py
Demonstrates fundamental Joblet operations:
- Running simple jobs
- Checking job status
- Getting job logs
- Canceling jobs
- Cleaning up jobs

```bash
python examples/01_basic_usage.py
```

### 02_advanced_features.py
Shows advanced Joblet features:
- Resource limits (CPU, memory)
- Environment variables
- File uploads
- Scheduled jobs
- GPU resource allocation

```bash
python examples/02_advanced_features.py
```

### 03_streaming_logs.py
Demonstrates real-time log streaming:
- Streaming logs from running jobs
- Concurrent status monitoring
- Thread-based log handling

```bash
python examples/03_streaming_logs.py
```

### 04_historical_logs_metrics.py
Shows how to query historical logs and metrics using PersistService:
- Querying historical logs with filtering (stdout/stderr)
- Querying historical metrics for completed jobs
- Time-range queries for logs and metrics
- Pagination support
- Comprehensive job analysis using historical data

```bash
python examples/04_historical_logs_metrics.py
```

**Note**: This example queries the joblet-persist service (port 50052) which stores historical job data. Ensure joblet-persist is running.

### 05_smart_log_streaming.py
Demonstrates intelligent log streaming that works like `rnx job log`:
- Automatic historical + live log handling
- Seamless access to logs from any job (running or completed)
- Reconnecting to running jobs with full history
- Live-only streaming option
- Graceful fallback when persist service unavailable

```bash
python examples/05_smart_log_streaming.py
```

**Key Feature**: `client.jobs.get_job_logs()` automatically:
1. Fetches historical logs from persist service (if available)
2. Then streams live logs from job service
3. Works transparently for both completed and running jobs

## Quick Start

1. Start your Joblet server:
```bash
# Assuming you have joblet server installed
joblet serve --port 8080
```

2. Run an example:
```bash
# Install the SDK if not already installed
pip install -e ..

# Run basic example
python 01_basic_usage.py
```

## Common Patterns

### Error Handling
```python
from joblet import JobletClient, JobNotFoundError, ConnectionError

try:
    client = JobletClient(host="localhost", port=8080)
    job = client.run_job(name="test", command="echo", args=["hello"])
except ConnectionError as e:
    print(f"Failed to connect: {e}")
except JobNotFoundError as e:
    print(f"Job not found: {e}")
```

### Waiting for Job Completion
```python
# With timeout
status = client.wait_for_job(job_uuid, timeout=30)

# Manual polling
while True:
    status = client.get_job_status(job_uuid)
    if status.status in ["completed", "failed", "canceled"]:
        break
    time.sleep(1)
```

### Resource Management
```python
# Always clean up jobs when done
try:
    job = client.run_job(...)
    # Do work
finally:
    client.delete_job(job.uuid)
```

## Notes

- All examples use `localhost:8080` as the default server
- Modify the host and port in the examples to match your setup
- Some features (like GPU) require appropriate hardware and drivers
