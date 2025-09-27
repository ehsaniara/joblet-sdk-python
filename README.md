# Joblet Python SDK

The official Python SDK for [Joblet](https://github.com/ehsaniara/joblet) - a distributed job orchestration system with GPU support.

## Installation

```bash
pip install joblet-sdk
```

## Quick Start

```python
from joblet import JobletClient

# Connect to your Joblet server
with JobletClient(
    host="your-joblet-server.com",
    port=50051,
    ca_cert_path="ca.pem",
    client_cert_path="client.pem",
    client_key_path="client.key"
) as client:
    # Run a simple job
    job = client.jobs.run_job(
        command="echo",
        args=["Hello, Joblet!"],
        name="my-first-job"
    )
    print(f"Job started: {job['job_uuid']}")
```

## Configuration

Create `~/.rnx/rnx-config.yml`:

```yaml
version: "3.0"
nodes:
  default:
    address: "your-joblet-server:50051"
    cert: |
      -----BEGIN CERTIFICATE-----
      # Your client certificate
      -----END CERTIFICATE-----
    key: |
      -----BEGIN PRIVATE KEY-----
      # Your client private key
      -----END PRIVATE KEY-----
    ca: |
      -----BEGIN CERTIFICATE-----
      # Your CA certificate
      -----END CERTIFICATE-----
```

## GPU Support

```python
# Run GPU-accelerated job
job = client.jobs.run_job(
    command="nvidia-smi",
    name="gpu-job",
    gpu_count=1,
    gpu_memory_mb=4096,
    runtime="python-3.11-ml"
)
```

## Features

- **Job Management** - Run single jobs or complex workflows
- **GPU Support** - Native GPU acceleration for ML/AI workloads
- **Resource Management** - CPU, memory, and GPU limits
- **Workflows** - Chain jobs with dependencies
- **Monitoring** - Real-time job status and logs
- **Security** - mTLS encryption and authentication

## API Reference

### Jobs
- `client.jobs.run_job()` - Execute a job
- `client.jobs.cancel_job()` - Cancel a scheduled job
- `client.jobs.stop_job()` - Stop a running job
- `client.jobs.get_job_status()` - Get job status
- `client.jobs.get_job_logs()` - Retrieve job logs
- `client.jobs.run_workflow()` - Execute a workflow

### Resources
- `client.networks` - Network management
- `client.volumes` - Storage management
- `client.monitoring` - System monitoring
- `client.runtimes` - Runtime environments

## Development

```bash
# Clone and setup
git clone https://github.com/ehsaniara/joblet-sdk-python.git
cd joblet-sdk-python
pip install -e .[dev]

# Run tests
pytest tests/

# Format code
black joblet/ examples/
```

## Examples

See the `examples/` directory for more detailed usage examples:
- `basic_job.py` - Simple job execution
- `gpu_example.py` - GPU-accelerated workloads
- `workflow_example.py` - Complex workflows

## License

MIT License - see LICENSE file for details.
