# Joblet Python SDK Examples

Welcome to the Joblet Python SDK examples! This directory contains practical examples to help you get started with
running jobs on your Joblet cluster using Python.

## Quick Setup

### Option 1: Install from PyPI (Recommended for projects)

Add to your `requirements.txt`:

```
joblet-sdk>=0.1.0
```

Or install directly:

```bash
pip install joblet-sdk
```

### Option 2: Install from GitHub (Latest development version)

Add to your `requirements.txt`:

```
joblet-sdk @ git+https://github.com/ehsaniara/joblet-sdk-python.git@main
```

Or install directly:

```bash
pip install git+https://github.com/ehsaniara/joblet-sdk-python.git
```

### Option 3: Development Setup (For contributing)

```bash
# Clone the repository
git clone https://github.com/ehsaniara/joblet-sdk-python.git
cd joblet-sdk-python

# Install in development mode
pip install -e .
```

### 2. Configure Your Connection

The SDK needs to know how to connect to your Joblet server. Create a config file at `~/.rnx/rnx-config.yml`:

```bash
mkdir -p ~/.rnx
```

Then create `~/.rnx/rnx-config.yml` with your server details:

```yaml
version: "3.0"

nodes:
  default:
    address: "your-joblet-server:50051"
    cert: |
      -----BEGIN CERTIFICATE-----
      # Your client certificate here
      -----END CERTIFICATE-----
    key: |
      -----BEGIN PRIVATE KEY-----
      # Your client private key here
      -----END PRIVATE KEY-----
    ca: |
      -----BEGIN CERTIFICATE-----
      # Your CA certificate here
      -----END CERTIFICATE-----
```

> **Note:** Replace `your-joblet-server` with your actual Joblet server address. The certificates are provided by your
> Joblet administrator.

### 3. Test Your Setup

```bash
cd examples
python basic_job.py
```

If everything is configured correctly, you should see output like:

```
Connecting to your-joblet-server:50051
Server is available!
Job started: abc123...
Status: RUNNING
Status: COMPLETED
Output: Hello, World!
```

## Examples Overview

### 🚀 `basic_job.py`

A simple "Hello World" example that demonstrates:

- Connecting to the Joblet server
- Running a basic echo command
- Monitoring job status
- Retrieving job output

**Run it:**

```bash
python basic_job.py
```

### 📊 `streaming_counter.py`

Shows real-time log streaming from a long-running job:

- Creates a counter that increments every 100ms for 60 seconds
- Streams output in real-time as the job runs
- Demonstrates handling of long-running jobs

**Run it:**

```bash
python streaming_counter.py
```

### 🤖 `ml_runtime_example.py`

Demonstrates using specialized runtimes:

- Runs a job with the `python-3.11-ml` runtime
- Tests available ML libraries (NumPy, Pandas, Scikit-learn)
- Shows how to specify custom runtimes for your jobs

**Run it:**

```bash
python ml_runtime_example.py
```

## Common Issues & Solutions

### "Server not available"

- **Check your config**: Verify the server address in `~/.rnx/rnx-config.yml`
- **Network connectivity**: Make sure you can reach the Joblet server
- **Certificates**: Ensure your certificates are valid and properly formatted

### "Connection error" or SSL issues

- **Certificate format**: Make sure certificates don't have extra spaces or wrong line endings
- **Server compatibility**: The server requires TLS - the `insecure=True` flag won't work with most Joblet deployments

### "Runtime not found"

- **Check available runtimes**: Use `rnx runtime list` to see what's available on your server
- **Runtime name**: Make sure you're using the exact runtime name from the server

## Using in Your Projects

### Production Project Setup

Create a `requirements.txt` file in your project:

```txt
# requirements.txt
joblet-sdk>=0.1.0,<1.0.0  # Pin major version for stability
pyyaml>=6.0                # If you need custom config handling
```

Or use `pyproject.toml` for modern Python projects:

```toml
[project]
dependencies = [
    "joblet-sdk>=0.1.0,<1.0.0",
    "pyyaml>=6.0",
]
```

### Example Project Structure

```
your-project/
├── requirements.txt       # Dependencies
├── config/
│   └── joblet-config.yml # Your Joblet configuration
├── jobs/
│   ├── data_processing.py
│   └── ml_training.py
└── main.py
```

### Sample Usage in Your Code

```python
# main.py
from joblet import JobletClient

def run_data_job():
    with JobletClient(insecure=False) as client:
        job = client.jobs.run_job(
            command="python3",
            args=["jobs/data_processing.py"],
            name="data-processing-job",
            runtime="python-3.11-ml"
        )
        return job['job_uuid']

if __name__ == "__main__":
    job_id = run_data_job()
    print(f"Started job: {job_id}")
```

### Version Management

- **Development**: Use `joblet-sdk @ git+https://...` to get latest features
- **Staging/Production**: Use specific versions like `joblet-sdk==0.1.0` for reproducibility
- **Version ranges**: Use `joblet-sdk>=0.1.0,<1.0.0` for automatic patch updates

## Advanced Usage

### Custom Job Parameters

```python
from joblet import JobletClient

with JobletClient(insecure=False) as client:
    job = client.jobs.run_job(
        command="python3",
        args=["-c", "print('Custom job!')"],
        name="my-custom-job",
        runtime="python-3.11-ml",  # Use specific runtime
        cpu_limit=50,              # Limit CPU usage
        memory_limit=512,          # Limit memory (MB)
        timeout=300                # Job timeout (seconds)
    )
```

### Streaming Logs

```python
# Stream logs in real-time
for log_chunk in client.jobs.get_job_logs(job_uuid):
    print(log_chunk.decode(), end='', flush=True)
```

### Job Status Monitoring

```python
import time

while True:
    status = client.jobs.get_job_status(job_uuid)
    if status['status'].lower() in ['completed', 'failed', 'cancelled']:
        break
    time.sleep(1)

print(f"Final status: {status['status']}")
print(f"Exit code: {status['exit_code']}")
```

## Contributing

Found a bug or want to add a new example? We'd love your contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Submit a pull request


- 🐛 **Issues**: Report problems on the [GitHub Issues page](https://github.com/ehsaniara/joblet-sdk-python/issues)
- 💬 **Questions**: Ask your Joblet administrator for server-specific configuration
