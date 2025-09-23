# Joblet Python SDK

Want to run jobs and workflows on remote servers? This Python SDK makes it dead simple to work
with [Joblet](https://github.com/ehsaniara/joblet), a powerful job orchestration system. Whether you're running a single
script or coordinating complex data pipelines, we've got you covered.

## ✨ What can you do with this?

- **🏃‍♂️ Run jobs anywhere**: Fire off scripts, commands, or entire applications on remote servers
- **🔄 Build workflows**: Chain jobs together with dependencies - like "run job B only after job A finishes"
- **⚙️ Manage environments**: Install Python, Node.js, or any runtime you need, right from your code
- **🌐 Network isolation**: Create private networks for your jobs (think microservices that need to talk)
- **💾 Persistent storage**: Mount volumes so your jobs can save and share data
- **📊 Monitor everything**: Watch CPU, memory, and system health in real-time
- **🛡️ Type-safe**: Your IDE will love you - we have hints for everything
- **⚠️ Handle errors gracefully**: Specific exceptions so you know exactly what went wrong
- **📖 Actually useful docs**: Real examples you can copy-paste and modify
- **🔗 Clean up automatically**: Use Python's `with` statement and never worry about connections

## 📦 Getting Started

### Just want to use it?

```bash
pip install joblet-sdk
```

### Want to hack on it?

```bash
git clone https://github.com/yourusername/joblet-sdk-python
cd joblet-sdk-python
pip install -e .
```

### Doing serious development?

```bash
git clone https://github.com/yourusername/joblet-sdk-python
cd joblet-sdk-python
pip install -e ".[dev]"  # Gets you all the testing and linting tools
```

## ⚡ Your first job in 30 seconds

Here's how simple it is to run a job (you'll need mTLS certificates):

```python
from joblet import JobletClient

# Connect to your Joblet server with mTLS
with JobletClient(
    host="joblet.company.com",
    port=50051,
    ca_cert_path="/path/to/ca-cert.pem",
    client_cert_path="/path/to/client-cert.pem",
    client_key_path="/path/to/client-key.pem"
) as client:

    # Make sure the server is actually there
    if not client.health_check():
        print("Hmm, can't reach the server 🤔")
        exit(1)

    print("Great! We're connected 🎉")

    # Let's run something simple
    job = client.jobs.run_job(
        command="echo",
        args=["Hello from Joblet!"],
        name="my-first-job",
        max_memory=128,  # Don't go crazy with memory
        runtime="alpine"  # Nice and lightweight
    )

    print(f"Job is running! ID: {job['job_uuid']}")

    # Watch it do its thing
    import time
    while True:
        status = client.jobs.get_job_status(job['job_uuid'])
        print(f"Status: {status['status']}")

        if status['status'] in ['completed', 'failed', 'cancelled']:
            print(f"All done! Exit code: {status['exit_code']}")
            break

        time.sleep(1)  # Check again in a second

    # See what happened
    print("Here's what the job said:")
    for log_chunk in client.jobs.get_job_logs(job['job_uuid']):
        print(log_chunk.decode('utf-8'), end='')
```

### When things need to be bulletproof

Real production code needs error handling. Here's how to do it right:

```python
from joblet import (
    JobletClient,
    JobNotFoundError,
    ConnectionError,
    JobletException
)
import logging
import time

# Set up some logging so you know what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_data_processing_job():
    """This is how you'd do it in production."""

    try:
        # Use mTLS for production - security is built-in
        with JobletClient(
            host="joblet.production.com",
            port=50051,
            ca_cert_path="/etc/joblet/certs/ca.pem",
            client_cert_path="/etc/joblet/certs/client.pem",
            client_key_path="/etc/joblet/certs/client.key"
        ) as client:

            # Always check if the server is actually working
            if not client.health_check():
                raise ConnectionError("Server isn't responding properly")

            # Now run something more realistic
            job = client.jobs.run_job(
                command="python",
                args=["process_data.py", "--batch-size", "1000"],
                name=f"data-processing-{int(time.time())}",  # Unique names are good
                max_cpu=80,  # Don't hog all the CPU
                max_memory=2048,  # 2GB should be plenty
                runtime="python-3.11-ml",  # We need those ML libraries
                environment={
                    "ENV": "production",
                    "LOG_LEVEL": "INFO"
                },
                secret_environment={
                    "DATABASE_URL": "postgresql://...",  # Keep secrets separate
                    "API_KEY": "secret-key"
                },
                volumes=["data-volume:/data", "logs-volume:/logs"],  # Persistent storage
                network="processing-network"  # Isolated network
            )

            logger.info(f"Started job: {job['job_uuid']}")
            return job['job_uuid']

    except ConnectionError as e:
        logger.error(f"Can't connect to server: {e}")
        raise
    except JobNotFoundError as e:
        logger.error(f"Something went wrong with the job: {e}")
        raise
    except JobletException as e:
        logger.error(f"Joblet had an issue: {e}")
        raise
    except Exception as e:
        logger.error(f"Something unexpected happened: {e}")
        raise

# Let's use it
if __name__ == "__main__":
    try:
        job_uuid = run_data_processing_job()
        print(f"✅ Job is running: {job_uuid}")
    except Exception as e:
        print(f"❌ Something went wrong: {e}")
        exit(1)
```

## 🔐 mTLS Security (Required)

Security is baked in - all Joblet connections require mutual TLS (mTLS) authentication. You'll need three certificate
files to connect.

### The essentials you need

Every connection requires these three files:

- **CA Certificate** (`ca-cert.pem`) - Verifies the server's identity
- **Client Certificate** (`client-cert.pem`) - Proves your identity to the server
- **Client Private Key** (`client-key.pem`) - Your secret key (keep it safe!)

### Basic mTLS connection

```python
from joblet import JobletClient

# All three certificates are required
with JobletClient(
    host="joblet.company.com",
    port=50051,
    ca_cert_path="/path/to/ca-cert.pem",
    client_cert_path="/path/to/client-cert.pem",
    client_key_path="/path/to/client-key.pem"
) as client:
    if client.health_check():
        print("🔐 Securely connected!")
```

### Production-ready (environment variables)

Don't hardcode certificate paths in your code:

```python
import os
from joblet import JobletClient

# Set these environment variables:
# export JOBLET_HOST=joblet.company.com
# export JOBLET_PORT=50051
# export JOBLET_CA_CERT_PATH=/etc/ssl/certs/ca-cert.pem
# export JOBLET_CLIENT_CERT_PATH=/etc/ssl/certs/client-cert.pem
# export JOBLET_CLIENT_KEY_PATH=/etc/ssl/private/client-key.pem

with JobletClient(
    host=os.getenv('JOBLET_HOST', 'localhost'),
    port=int(os.getenv('JOBLET_PORT', '50051')),
    ca_cert_path=os.getenv('JOBLET_CA_CERT_PATH'),
    client_cert_path=os.getenv('JOBLET_CLIENT_CERT_PATH'),
    client_key_path=os.getenv('JOBLET_CLIENT_KEY_PATH')
) as client:
    print("🌍 Production-ready connection!")
```

### Custom gRPC options

Need keepalive or other gRPC settings?

```python
from joblet import JobletClient

# Custom connection settings
options = {
    'grpc.keepalive_time_ms': 30000,     # Ping every 30 seconds
    'grpc.keepalive_timeout_ms': 5000,   # Wait 5 seconds for response
    'grpc.keepalive_permit_without_calls': True
}

with JobletClient(
    host="joblet.company.com",
    port=50051,
    ca_cert_path="/certs/ca-cert.pem",
    client_cert_path="/certs/client-cert.pem",
    client_key_path="/certs/client-key.pem",
    options=options
) as client:
    print("⚙️ Connected with custom settings!")
```

Need more examples? Check out [`examples/mtls_configuration.py`](examples/mtls_configuration.py) for certificate
validation, environment-based config, and troubleshooting tips.

## 📚 Real examples you can actually use

We've put together some examples that show real-world usage (not just "hello world" stuff):

| Example                                                           | Description                          | Use Case                        |
|-------------------------------------------------------------------|--------------------------------------|---------------------------------|
| [`basic_job.py`](examples/basic_job.py)                           | Simple job execution with monitoring | Single-task automation          |
| [`workflow_example.py`](examples/workflow_example.py)             | Multi-job workflow with dependencies | Data pipelines, ETL processes   |
| [`system_monitoring.py`](examples/system_monitoring.py)           | Real-time system metrics streaming   | Infrastructure monitoring       |
| [`runtime_management.py`](examples/runtime_management.py)         | Runtime installation and testing     | Environment management          |
| [`network_volume_example.py`](examples/network_volume_example.py) | Network and storage operations       | Microservices, data persistence |
| [`ssl_certificates.py`](examples/ssl_certificates.py)             | SSL/TLS certificate configuration    | Secure production deployments   |

### Give them a try

```bash
# Jump into the examples
cd examples

# Start with the basics
python basic_job.py

# Or point it at your own server
JOBLET_HOST=your-server.com python workflow_example.py
```

## 🏗️ Cool stuff you can build

### Building data pipelines with workflows

Here's how to chain multiple jobs together:

```python
from joblet import JobletClient
import yaml

# Define a complex data processing workflow
workflow_definition = """
version: "1.0"
name: "ml-training-pipeline"

jobs:
  # Data extraction
  - name: "extract-data"
    command: "python"
    args: ["extract.py", "--source", "database"]
    runtime: "python-3.11"
    max_memory: 1024
    volumes: ["data-lake:/data"]

  # Data preprocessing
  - name: "preprocess-data"
    command: "python"
    args: ["preprocess.py", "--input", "/data/raw"]
    runtime: "python-3.11-ml"
    depends_on: ["extract-data"]
    max_memory: 2048
    volumes: ["data-lake:/data"]

  # Model training (parallel jobs)
  - name: "train-model-a"
    command: "python"
    args: ["train.py", "--model", "linear"]
    runtime: "python-3.11-ml"
    depends_on: ["preprocess-data"]
    max_memory: 4096
    volumes: ["data-lake:/data", "models:/models"]

  - name: "train-model-b"
    command: "python"
    args: ["train.py", "--model", "neural"]
    runtime: "python-3.11-ml"
    depends_on: ["preprocess-data"]
    max_memory: 8192
    max_cpu: 80
    volumes: ["data-lake:/data", "models:/models"]

  # Model evaluation
  - name: "evaluate-models"
    command: "python"
    args: ["evaluate.py", "--models", "/models"]
    runtime: "python-3.11-ml"
    depends_on: ["train-model-a", "train-model-b"]
    volumes: ["models:/models", "results:/results"]
"""

with JobletClient() as client:
    # Create necessary volumes
    client.volumes.create_volume("data-lake", "10GB")
    client.volumes.create_volume("models", "5GB")
    client.volumes.create_volume("results", "1GB")

    # Submit workflow
    workflow = client.jobs.run_workflow(
        workflow="ml-pipeline.yml",
        yaml_content=workflow_definition
    )

    print(f"🚀 Workflow started: {workflow['workflow_uuid']}")

    # Monitor workflow progress
    while True:
        status = client.jobs.get_workflow_status(workflow['workflow_uuid'])
        workflow_info = status['workflow']

        print(f"📊 Workflow: {workflow_info['status']}")
        print(f"   Total: {workflow_info['total_jobs']}")
        print(f"   Completed: {workflow_info['completed_jobs']}")
        print(f"   Failed: {workflow_info['failed_jobs']}")

        # Show individual job status
        for job in status['jobs']:
            print(f"   └─ {job['job_name']}: {job['status']}")

        if workflow_info['status'] in ['completed', 'failed']:
            break

        time.sleep(5)
```

### Real-time Monitoring Dashboard

```python
from joblet import JobletClient
import time
from datetime import datetime

def create_monitoring_dashboard():
    """Create a simple monitoring dashboard."""

    with JobletClient() as client:
        print("🖥️  Joblet System Monitor")
        print("=" * 50)

        try:
            for metrics in client.monitoring.stream_system_metrics(interval_seconds=2):
                # Clear screen (works on Unix systems)
                print("\033[2J\033[H")

                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"🕐 {timestamp} | Joblet System Status")
                print("=" * 50)

                # System overview
                host = metrics.get('host', {})
                print(f"🖥️  Host: {host.get('hostname', 'Unknown')}")
                print(f"🏗️  OS: {host.get('os', 'Unknown')} {host.get('platform_version', '')}")

                # Resource usage
                cpu = metrics.get('cpu', {})
                memory = metrics.get('memory', {})

                print(f"\n📊 Resource Usage:")
                print(f"   CPU:    {cpu.get('usage_percent', 0):.1f}% ({cpu.get('cores', 0)} cores)")
                print(f"   Memory: {memory.get('usage_percent', 0):.1f}% "
                      f"({memory.get('used_bytes', 0) / (1024**3):.1f}GB / "
                      f"{memory.get('total_bytes', 0) / (1024**3):.1f}GB)")

                # Load average
                load_avg = cpu.get('load_average', [])
                if load_avg:
                    print(f"   Load:   {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}")

                # Disk usage
                disks = metrics.get('disks', [])
                if disks:
                    print(f"\n💾 Disk Usage:")
                    for disk in disks[:3]:  # Show top 3 disks
                        print(f"   {disk['device']}: {disk['usage_percent']:.1f}% "
                              f"({disk['used_bytes'] / (1024**3):.1f}GB / "
                              f"{disk['total_bytes'] / (1024**3):.1f}GB)")

                # Network activity
                networks = metrics.get('networks', [])
                if networks:
                    print(f"\n🌐 Network Activity:")
                    for net in networks[:2]:  # Show top 2 interfaces
                        rx_mb = net['bytes_received'] / (1024**2)
                        tx_mb = net['bytes_sent'] / (1024**2)
                        print(f"   {net['interface']}: ↓{rx_mb:.1f}MB ↑{tx_mb:.1f}MB")

                print(f"\n{'─' * 50}")
                print("Press Ctrl+C to stop monitoring")

        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")

# Run the dashboard
if __name__ == "__main__":
    create_monitoring_dashboard()
```

## 🔧 When things go wrong

Don't panic! Here are the most common issues and how to fix them.

### "I can't connect to the server"

```python
from joblet import JobletClient, ConnectionError

try:
    client = JobletClient(host="localhost", port=50051)
    client.health_check()
except ConnectionError as e:
    print(f"Can't connect: {e}")
    # Things to check:
    # 1. Is the Joblet server actually running?
    # 2. Are you using the right host and port?
    # 3. Firewall blocking you?
    # 4. If using SSL, are your certificates right?
```

### "My job won't start"

```python
try:
    job = client.jobs.run_job(command="some-weird-command")
except JobletException as e:
    print(f"Job wouldn't start: {e}")
    # Usually this means:
    # 1. The runtime doesn't exist (check with client.runtimes.list_runtimes())
    # 2. The command isn't available in that runtime
    # 3. You're asking for too much memory/CPU
    # 4. Something's wrong with your file uploads or volumes
```

### "My job keeps getting killed"

```python
job = client.jobs.run_job(
    command="python",
    args=["hungry_script.py"],
    max_memory=512,  # Whoops, too small
    max_cpu=10      # Way too restrictive
)

# Check what happened
status = client.jobs.get_job_status(job['job_uuid'])
if status['exit_code'] == 137:  # This means it got killed
    print("Yep, ran out of memory. Give it more!")
```

### "I want to see what's actually happening"

```python
import logging

# Turn on debug mode to see everything
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('joblet')

# Now you'll see all the gRPC chatter
with JobletClient() as client:
    client.health_check()
```

## 📋 Some friendly advice

### Always clean up after yourself

```python
# ✅ Do this - it cleans up automatically
with JobletClient() as client:
    # Do your stuff here
    pass

# ❌ Don't do this - you might forget to close it
client = JobletClient()
try:
    # Do your stuff here
    pass
finally:
    client.close()  # Easy to forget!
```

### Catch specific problems

```python
# ✅ Catch specific things so you know what went wrong
from joblet import JobNotFoundError, ConnectionError, JobletException

try:
    status = client.jobs.get_job_status(job_uuid)
except JobNotFoundError:
    logger.warning(f"That job doesn't exist: {job_uuid}")
except ConnectionError:
    logger.error("Lost connection to the server")
except JobletException as e:
    logger.error(f"Something Joblet-related broke: {e}")
```

### Don't wait forever for jobs

```python
# ✅ Set a timeout so you don't wait forever
import time

def wait_for_job(client, job_uuid, timeout=300):
    """Wait for a job to finish, but not forever."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        status = client.jobs.get_job_status(job_uuid)

        if status['status'] in ['completed', 'failed', 'cancelled']:
            return status

        time.sleep(min(5, timeout - (time.time() - start_time)))

    raise TimeoutError(f"Job {job_uuid} took too long (over {timeout} seconds)")
```

### Use environment variables like a pro

```python
# ✅ Don't hardcode server details
import os

class JobletConfig:
    def __init__(self):
        self.host = os.getenv('JOBLET_HOST', 'localhost')
        self.port = int(os.getenv('JOBLET_PORT', '50051'))
        self.secure = os.getenv('JOBLET_SECURE', 'false').lower() == 'true'
        self.timeout = int(os.getenv('JOBLET_TIMEOUT', '30'))

config = JobletConfig()
client = JobletClient(
    host=config.host,
    port=config.port,
    secure=config.secure
)
```

### Make your workflows reusable

```python
# ✅ Build workflows you can use again and again
def create_data_pipeline():
    """A data pipeline template you can customize."""
    return """
    version: "1.0"
    name: "data-pipeline"

    jobs:
      - name: "validate-input"
        command: "python"
        args: ["validate.py"]
        runtime: "python-3.11"

      - name: "process-data"
        command: "python"
        args: ["process.py"]
        runtime: "python-3.11-ml"
        depends_on: ["validate-input"]  # Wait for validation first
        max_memory: 2048

      - name: "generate-report"
        command: "python"
        args: ["report.py"]
        runtime: "python-3.11"
        depends_on: ["process-data"]  # Wait for processing
    """
```

## 📖 Need more details?

The complete API docs are in [`API_REFERENCE.md`](API_REFERENCE.md) - everything's documented there.

### Quick cheat sheet

```python
from joblet import JobletClient

with JobletClient() as client:
    # Jobs
    job = client.jobs.run_job(command="echo", args=["hello"])
    status = client.jobs.get_job_status(job['job_uuid'])
    logs = client.jobs.get_job_logs(job['job_uuid'])

    # Workflows
    workflow = client.jobs.run_workflow("workflow.yml", yaml_content)

    # Monitoring
    metrics = client.monitoring.get_system_status()

    # Runtimes
    runtimes = client.runtimes.list_runtimes()

    # Networks & Volumes
    network = client.networks.create_network("net", "10.0.1.0/24")
    volume = client.volumes.create_volume("vol", "1GB")
```

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/joblet-sdk-python
cd joblet-sdk-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests (when available)
pytest

# Format code
black joblet/
isort joblet/

# Type checking
mypy joblet/
```

### Protocol Buffer Management

The SDK automatically generates Python bindings from the
official [joblet-proto](https://github.com/ehsaniara/joblet-proto) repository.

**Current version**: `v1.0.1` (see [`joblet/_proto_generation_info.py`](joblet/_proto_generation_info.py) for details)

#### Easy way (using Makefile)

```bash
# List available proto versions
make proto-list

# Use latest version
make proto

# Use specific version
make proto PROTO_VERSION=v1.0.1

# Clean generated proto files
make proto-clean
```

#### Manual way (using script)

```bash
# Show available versions
python scripts/generate_proto.py --list-tags

# Generate from latest
python scripts/generate_proto.py

# Generate from specific version
python scripts/generate_proto.py --version v1.0.1
```

The generated files are automatically updated with version tracking and generation timestamps.

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with tests
4. Ensure code quality: `black`, `isort`, `mypy`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[Joblet](https://github.com/ehsaniara/joblet)** - The main Joblet job orchestration system
- **[Joblet Proto](https://github.com/ehsaniara/joblet-proto)** - Protocol buffer definitions

