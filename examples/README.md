# Joblet SDK Examples

Hands-on examples demonstrating the Joblet Python SDK.

## Prerequisites

1. Joblet server running (default: `localhost:50051`)
2. Python 3.9+ with joblet-sdk-python installed
3. Configuration file at `~/.rnx/rnx-config.yml`

## Examples

| Example | Description |
|---------|-------------|
| [01_basic_usage](01_basic_usage/) | Running jobs, checking status, getting logs |
| [02_advanced_features](02_advanced_features/) | Resource limits, GPUs, networks, volumes |
| [03_streaming_logs](03_streaming_logs/) | Real-time log streaming |
| [04_historical_logs_metrics](04_historical_logs_metrics/) | Logs and metrics from completed jobs |
| [05_smart_log_streaming](05_smart_log_streaming/) | Automatic historical + live log handling |
| [06_long_running_job](06_long_running_job/) | Managing long-duration jobs |
| [07_file_uploads_and_dependencies](07_file_uploads_and_dependencies/) | File uploads and Python dependencies |

## Quick Start

```bash
# Install SDK
pip install -e ..

# Run an example
cd 01_basic_usage
python main.py
```

## Configuration

Create `~/.rnx/rnx-config.yml`:

```yaml
version: "3.0"
nodes:
  default:
    address: "localhost:50051"
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
    pass
```

## Common Patterns

### Error Handling

```python
from joblet import JobletClient, JobNotFoundError, ConnectionError

try:
    with JobletClient() as client:
        job = client.jobs.run_job(name="test", command="echo", args=["hello"])
except ConnectionError as e:
    print(f"Failed to connect: {e}")
except JobNotFoundError as e:
    print(f"Job not found: {e}")
```

### Wait for Completion

```python
import time

while True:
    status = client.jobs.get_job_status(job_uuid)
    if status["status"] in ["COMPLETED", "FAILED", "STOPPED"]:
        break
    time.sleep(1)
```

### Resource Cleanup

```python
try:
    job = client.jobs.run_job(...)
    # Do work
finally:
    client.jobs.delete_job(job["job_uuid"])
```

## Service Status

```bash
# Check Joblet service (Linux systemd)
sudo systemctl status joblet

# View service logs
sudo journalctl -u joblet -f
```
