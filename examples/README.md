# Joblet SDK Examples

This directory contains example scripts demonstrating how to use the Joblet SDK.

## Prerequisites

1. Joblet server running (default: `localhost:50051`)
2. Python 3.9+ with joblet-sdk-python installed
3. Configuration file at `~/.rnx/rnx-config.yml` (see Configuration section below)

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
Shows how to retrieve job logs and metrics (proto v2.3.0):
- Getting all logs for completed jobs
- Getting all metrics for completed jobs
- Client-side filtering and statistics
- Demonstrates simplified streaming API

```bash
python examples/04_historical_logs_metrics.py
```

**Note**: Proto v2.3.0 simplified the API - the server streams ALL logs/metrics for a job, and clients filter results as needed.

### 05_smart_log_streaming.py
Demonstrates intelligent log streaming that works like `rnx job log`:
- Automatic historical + live log handling
- Seamless access to logs from any job (running or completed)
- Reconnecting to running jobs with full history
- Live-only streaming option

```bash
python examples/05_smart_log_streaming.py
```

**Key Feature**: `client.jobs.get_job_logs()` automatically provides complete log history:
1. Server handles historical data internally via IPC
2. Streams both historical and live logs in unified response
3. Works transparently for both completed and running jobs

## Configuration

Create `~/.rnx/rnx-config.yml`:

```yaml
version: "3.0"
nodes:
  default:
    address: "localhost:50051"  # Required: Joblet service endpoint
    nodeId: "local-dev"  # Optional: node identifier
    cert: |
      -----BEGIN CERTIFICATE-----
      [Your client certificate]
      -----END CERTIFICATE-----
    key: |
      -----BEGIN PRIVATE KEY-----
      [Your client private key]
      -----END PRIVATE KEY-----
    ca: |
      -----BEGIN CERTIFICATE-----
      [Your CA certificate]
      -----END CERTIFICATE-----
```

Or connect with explicit parameters:
```python
with JobletClient(
    host="localhost",
    port=50051,
    ca_cert_path="/path/to/ca.pem",
    client_cert_path="/path/to/client.pem",
    client_key_path="/path/to/client-key.pem"
) as client:
    # Your code here
    pass
```

## Quick Start

1. Ensure Joblet service is running (Linux systemd service):
```bash
# Check Joblet service status (listens on port 50051)
sudo systemctl status joblet

# View service logs if needed
sudo journalctl -u joblet -f
```

2. Run an example:
```bash
# Install the SDK if not already installed
pip install -e ..

# Run basic example
python 01_basic_usage.py
```

**Note**: Joblet is a Linux-native service that runs as a systemd service with embedded persistence.
See the [Joblet Installation Guide](https://github.com/ehsaniara/joblet/blob/main/docs/INSTALLATION.md)
for server setup and [Quick Start](https://github.com/ehsaniara/joblet/blob/main/docs/QUICKSTART.md)
for getting started.

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
