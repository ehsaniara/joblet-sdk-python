# Joblet Python SDK - API Reference

Everything you need to know about using the Joblet SDK! This is where we break down every method, parameter, and feature
so you can make the most of your job orchestration.

## Table of Contents

- [Client](#client)
    - [JobletClient](#jobletclient)
- [Services](#services)
    - [JobService](#jobservice)
    - [NetworkService](#networkservice)
    - [VolumeService](#volumeservice)
    - [MonitoringService](#monitoringservice)
    - [RuntimeService](#runtimeservice)
- [Exceptions](#exceptions)
- [Data Types](#data-types)

## Client

### JobletClient

Your gateway to everything Joblet! This is the main class you'll work with to run jobs, manage workflows, and monitor
your systems.

#### How to connect

```python
JobletClient(
    host: str = "localhost",
    port: int = 50051,
    ca_cert_path: str,
    client_cert_path: str,
    client_key_path: str,
    options: Optional[Dict[str, Any]] = None
)
```

**What you need:**

- `host` (str): Where your Joblet server lives (hostname or IP)
- `port` (int): Which port to connect to (usually 50051)
- `ca_cert_path` (str): Path to your CA certificate file
- `client_cert_path` (str): Path to your client certificate
- `client_key_path` (str): Path to your private key file
- `options` (dict): Extra gRPC settings if you need them

**Examples:**

```python
# Basic connection with certificates
client = JobletClient(
    host="joblet.company.com",
    port=50051,
    ca_cert_path="/certs/ca.pem",
    client_cert_path="/certs/client.pem",
    client_key_path="/certs/client.key"
)

# Using environment variables (recommended!)
import os
client = JobletClient(
    host=os.getenv('JOBLET_HOST', 'localhost'),
    port=int(os.getenv('JOBLET_PORT', '50051')),
    ca_cert_path=os.getenv('JOBLET_CA_CERT_PATH'),
    client_cert_path=os.getenv('JOBLET_CLIENT_CERT_PATH'),
    client_key_path=os.getenv('JOBLET_CLIENT_KEY_PATH')
)

# With custom connection settings
options = {
    'grpc.keepalive_time_ms': 30000,  # Keep connection alive
    'grpc.keepalive_timeout_ms': 5000
}
client = JobletClient(
    host="joblet.company.com",
    port=50051,
    ca_cert_path="/certs/ca.pem",
    client_cert_path="/certs/client.pem",
    client_key_path="/certs/client.key",
    options=options
)
```

#### What you get access to

Once you have a client, you get these handy services:

- `client.jobs` - Run jobs, manage workflows, get logs
- `client.networks` - Create isolated networks for your jobs
- `client.volumes` - Manage persistent storage
- `client.monitoring` - Check system health and get metrics
- `client.runtimes` - Manage Python, Node.js, and other runtime environments

#### Useful methods

##### health_check()

Is the server actually there and working?

```python
def health_check() -> bool
```

**Returns:** `True` if everything's good, `False` if something's wrong

**Example:**

```python
if client.health_check():
    print("🎉 Server is ready to go!")
else:
    print("😞 Server seems to be having issues")
```

##### close()

Clean up the connection when you're done.

```python
def close()
```

**Example:**

```python
client.close()  # Be nice and clean up!
```

**Pro tip:** Use `with` statements so this happens automatically:

```python
with JobletClient(...) as client:
    # Do your work here
    pass
# Connection automatically closed!
```

## Services

### JobService

This is where the magic happens! Use `client.jobs` to run commands, manage workflows, and get all the juicy details
about what's running.

#### Running jobs

##### run_job()

Fire off a new job on your Joblet server!

```python
def run_job(
    command: str,
    args: Optional[List[str]] = None,
    name: Optional[str] = None,
    max_cpu: Optional[int] = None,
    cpu_cores: Optional[str] = None,
    max_memory: Optional[int] = None,
    max_iobps: Optional[int] = None,
    schedule: Optional[str] = None,
    network: Optional[str] = None,
    volumes: Optional[List[str]] = None,
    runtime: Optional[str] = None,
    work_dir: Optional[str] = None,
    environment: Optional[Dict[str, str]] = None,
    secret_environment: Optional[Dict[str, str]] = None,
    uploads: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]
```

**What you can specify:**

- `command` (str): The main command to run (like "python" or "node")
- `args` (list): Arguments for your command (like ["script.py", "--verbose"])
- `name` (str): Give your job a nice name so you can find it later
- `max_cpu` (int): Don't hog the CPU! Limit to percentage (0-100)
- `cpu_cores` (str): Pin to specific cores ("0-1" or "2,4")
- `max_memory` (int): Memory limit in MB (be nice to other jobs!)
- `max_iobps` (int): Limit disk I/O operations per second
- `schedule` (str): Run later? Specify time in ISO format
- `network` (str): Which network to use (for isolation)
- `volumes` (list): Mount storage like ["data-vol:/data", "logs-vol:/logs"]
- `runtime` (str): Which environment to use ("python-3.11", "node-18", etc.)
- `work_dir` (str): Where to run the command inside the container
- `environment` (dict): Environment variables (visible in logs)
- `secret_environment` (dict): Secret env vars (hidden from logs)
- `uploads` (list): Files to upload before running

**What you get back:**

- `job_uuid` (str): Unique ID to track this job
- `status` (str): Current status ("pending", "running", "completed", etc.)
- `command` (str): What command is running
- `args` (list): The arguments you passed
- `start_time` (str): When it started
- `end_time` (str): When it finished (if it did)
- `exit_code` (int): Exit code (0 = success, anything else = probably bad)

**Examples:**

```python
# Simple job - just run something
job = client.jobs.run_job(
    command="echo",
    args=["Hello, World!"],
    name="my-first-job"
)
print(f"Job started: {job['job_uuid']}")

# Data processing with proper limits
job = client.jobs.run_job(
    command="python",
    args=["process_data.py", "--batch-size", "1000"],
    name="data-processing",
    max_memory=2048,  # 2GB should be enough
    max_cpu=80,       # Don't use more than 80% CPU
    runtime="python-3.11-ml",  # Use the ML runtime
    environment={"LOG_LEVEL": "INFO"},
    secret_environment={"API_KEY": "super-secret"},
    volumes=["data-storage:/data", "output:/results"]
)

# Upload files and run them
uploads = [
    {
        "path": "script.py",
        "content": b"print('Hello from uploaded script!')",
        "mode": 0o755  # Make it executable
    }
]
job = client.jobs.run_job(
    command="python",
    args=["script.py"],
    uploads=uploads,
    name="uploaded-script"
)
```

#### Checking on jobs

##### get_job_status()

What's my job doing right now?

```python
def get_job_status(job_uuid: str) -> Dict[str, Any]
```

**Give it:** The job ID you got when you started the job

**You get back:** Everything you could want to know about that job - status, exit code, when it started, resource usage,
etc.

**Example:**

```python
status = client.jobs.get_job_status("job-uuid-here")
print(f"Job is: {status['status']}")

if status['status'] == 'completed':
    if status['exit_code'] == 0:
        print("🎉 Success!")
    else:
        print(f"😞 Failed with exit code {status['exit_code']}")
elif status['status'] == 'running':
    print("🔄 Still working on it...")
```

##### stop_job()

Stop that job! (Maybe it's taking too long or you made a mistake)

```python
def stop_job(job_uuid: str) -> Dict[str, Any]
```

**Give it:** The job ID to stop

**Example:**

```python
result = client.jobs.stop_job("job-uuid-here")
print(f"Stopped job: {result['status']}")
```

##### delete_job()

Remove a job from the system completely (careful with this one!)

```python
def delete_job(job_uuid: str) -> Dict[str, Any]
```

**Give it:** The job ID to delete

**Example:**

```python
result = client.jobs.delete_job("job-uuid-here")
if result['success']:
    print("Job deleted!")
else:
    print(f"Couldn't delete: {result['message']}")
```

#### Getting logs

##### get_job_logs()

Want to see what your job is actually doing? Stream the logs in real-time!

```python
def get_job_logs(job_uuid: str) -> Iterator[bytes]
```

**Give it:** Job ID

**You get back:** A stream of log chunks as they happen

**Example:**

```python
print("📄 Job logs:")
try:
    for log_chunk in client.jobs.get_job_logs("job-uuid"):
        print(log_chunk.decode('utf-8'), end='')
except KeyboardInterrupt:
    print("\n👋 Stopped watching logs")
```

#### Listing jobs

##### list_jobs()

Show me everything that's running (or has run recently)!

```python
def list_jobs() -> List[Dict[str, Any]]
```

**You get back:** A list of all jobs with their basic info

**Example:**

```python
jobs = client.jobs.list_jobs()
print(f"Found {len(jobs)} jobs:")

for job in jobs:
    status_emoji = {
        'completed': '✅',
        'running': '🔄',
        'failed': '❌',
        'pending': '⏳'
    }.get(job['status'], '❓')

    print(f"  {status_emoji} {job['name']}: {job['status']}")
```

#### Workflows (the fancy stuff!)

##### run_workflow()

Want to run multiple jobs that depend on each other? Workflows are perfect for data pipelines, CI/CD, or any multi-step
process!

```python
def run_workflow(
    workflow: str,
    yaml_content: Optional[str] = None,
    workflow_files: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]
```

**What you need:**

- `workflow` (str): Name for your workflow
- `yaml_content` (str): The YAML definition of your workflow
- `workflow_files` (list): Extra files the workflow might need

**Example:**

```python
# A simple data pipeline workflow
workflow_yaml = """
version: "1.0"
name: "data-pipeline"
jobs:
  - name: "extract"
    command: "python"
    args: ["extract.py"]
    runtime: "python-3.11"

  - name: "transform"
    command: "python"
    args: ["transform.py"]
    depends_on: ["extract"]  # Wait for extract to finish!

  - name: "load"
    command: "python"
    args: ["load.py"]
    depends_on: ["transform"]  # Then wait for transform
"""

workflow = client.jobs.run_workflow(
    workflow="my-data-pipeline",
    yaml_content=workflow_yaml
)
print(f"🚀 Workflow started: {workflow['workflow_uuid']}")
```

##### get_workflow_status()

How's my workflow doing? Are all the jobs running smoothly?

```python
def get_workflow_status(workflow_uuid: str) -> Dict[str, Any]
```

##### list_workflows()

Show me all my workflows (running and completed ones too if you want)

```python
def list_workflows(include_completed: bool = False) -> List[Dict[str, Any]]
```

##### get_workflow_jobs()

What jobs are part of this workflow?

```python
def get_workflow_jobs(workflow_uuid: str) -> List[Dict[str, Any]]
```

### NetworkService

Need to isolate your jobs from each other? Create virtual networks! Use `client.networks` to set up private
communication channels.

##### create_network()

Make a new network for your jobs to talk to each other (but not to other jobs)

```python
def create_network(name: str, cidr: str) -> Dict[str, Any]
```

**What you need:**

- `name` (str): Give your network a name
- `cidr` (str): IP address range like "10.0.1.0/24" (don't worry, just pick something unique)

**Example:**

```python
# Create a network for microservices
network = client.networks.create_network(
    name="microservices-net",
    cidr="10.0.1.0/24"
)
print(f"🌐 Created network: {network['name']}")

# Now your jobs can use this network
job1 = client.jobs.run_job(
    command="python",
    args=["api_server.py"],
    network="microservices-net",  # Use the network!
    name="api-server"
)

job2 = client.jobs.run_job(
    command="python",
    args=["worker.py"],
    network="microservices-net",  # They can talk to each other
    name="worker"
)
```

##### list_networks()

What networks do I have available?

```python
def list_networks() -> List[Dict[str, Any]]
```

**Example:**

```python
networks = client.networks.list_networks()
for net in networks:
    print(f"📡 {net['name']}: {net['cidr']} ({net['job_count']} jobs using it)")
```

##### remove_network()

Don't need this network anymore? Remove it!

```python
def remove_network(name: str) -> Dict[str, Any]
```

**Example:**

```python
result = client.networks.remove_network("old-network")
if result['success']:
    print("🗑️ Network removed!")
```

### VolumeService

Need your jobs to save data that sticks around? Create storage volumes! Use `client.volumes` to manage persistent
storage.

##### create_volume()

Make a new storage space for your jobs to use

```python
def create_volume(
    name: str,
    size: str,
    volume_type: str = "filesystem"
) -> Dict[str, Any]
```

**What you need:**

- `name` (str): Give your volume a name
- `size` (str): How big? Like "1GB", "500MB", "10GB"
- `volume_type` (str): "filesystem" for disk storage, "memory" for super-fast RAM storage

**Example:**

```python
# Create storage for data processing
volume = client.volumes.create_volume(
    name="data-storage",
    size="5GB",
    volume_type="filesystem"
)
print(f"💾 Created volume: {volume['name']} at {volume['path']}")

# Use it in a job
job = client.jobs.run_job(
    command="python",
    args=["process_data.py"],
    volumes=["data-storage:/data"],  # Mount it at /data
    name="data-processor"
)

# Create fast temporary storage
temp_volume = client.volumes.create_volume(
    name="temp-cache",
    size="1GB",
    volume_type="memory"  # Super fast but gone when job ends
)
```

##### list_volumes()

What storage do I have available?

```python
def list_volumes() -> List[Dict[str, Any]]
```

**Example:**

```python
volumes = client.volumes.list_volumes()
for vol in volumes:
    print(f"💾 {vol['name']}: {vol['size']} ({vol['type']}) - {vol['job_count']} jobs using it")
```

##### remove_volume()

Delete a volume (careful - this removes all data!)

```python
def remove_volume(name: str) -> Dict[str, Any]
```

**Example:**

```python
result = client.volumes.remove_volume("old-data")
if result['success']:
    print("🗑️ Volume deleted!")
else:
    print(f"Couldn't delete: {result['message']}")
```

### MonitoringService

Want to keep an eye on your server? Use `client.monitoring` to check system health, CPU usage, memory, and more!

##### get_system_status()

How's my server doing right now?

```python
def get_system_status() -> Dict[str, Any]
```

**You get back:** Everything about your system - CPU, memory, disk space, network traffic, running processes, and more

**Example:**

```python
status = client.monitoring.get_system_status()

print(f"🖥️  System Status:")
print(f"   CPU: {status['cpu']['usage_percent']:.1f}%")
print(f"   Memory: {status['memory']['usage_percent']:.1f}%")
print(f"   Available: {'Yes' if status['available'] else 'No'}")

# Check disk space
for disk in status['disks']:
    print(f"   Disk {disk['device']}: {disk['usage_percent']:.1f}% used")

# See what's using the most CPU
for process in status['processes']['top_by_cpu'][:3]:
    print(f"   Top CPU: {process['name']} ({process['cpu_percent']:.1f}%)")
```

##### stream_system_metrics()

Watch your system in real-time! Perfect for monitoring during heavy workloads.

```python
def stream_system_metrics(
    interval_seconds: int = 5,
    metric_types: Optional[List[str]] = None
) -> Iterator[Dict[str, Any]]
```

**What you can specify:**

- `interval_seconds` (int): How often to update (in seconds)
- `metric_types` (list): Only show certain metrics if you want

**Example:**

```python
print("📊 Live system metrics (press Ctrl+C to stop):")
try:
    for metrics in client.monitoring.stream_system_metrics(interval_seconds=2):
        cpu = metrics['cpu']['usage_percent']
        memory = metrics['memory']['usage_percent']
        timestamp = metrics['timestamp']

        print(f"\r⏰ {timestamp} | CPU: {cpu:5.1f}% | Memory: {memory:5.1f}%", end='')

except KeyboardInterrupt:
    print("\n👋 Stopped monitoring")
```

### RuntimeService

Need Python, Node.js, or other environments for your jobs? Use `client.runtimes` to install, manage, and use different
runtime environments!

##### list_runtimes()

What programming environments do I have available?

```python
def list_runtimes() -> List[Dict[str, Any]]
```

**You get back:** All the runtime environments you can use - Python versions, Node.js, Go, etc.

**Example:**

```python
runtimes = client.runtimes.list_runtimes()
print("🚀 Available runtimes:")

for runtime in runtimes:
    status = "✅" if runtime['available'] else "❌"
    print(f"  {status} {runtime['name']}: {runtime['language']} {runtime['version']}")

    if runtime['packages']:
        print(f"     📦 Includes: {', '.join(runtime['packages'][:3])}...")
```

##### get_runtime_info()

Tell me more about this specific runtime

```python
def get_runtime_info(runtime: str) -> Dict[str, Any]
```

**Example:**

```python
info = client.runtimes.get_runtime_info("python-3.11-ml")
print(f"📋 {info['runtime']['name']}")
print(f"   Language: {info['runtime']['language']} {info['runtime']['version']}")
print(f"   Size: {info['runtime']['size_bytes'] / 1024 / 1024:.1f} MB")
print(f"   Packages: {len(info['runtime']['packages'])} installed")
```

##### test_runtime()

Is this runtime working properly?

```python
def test_runtime(runtime: str) -> Dict[str, Any]
```

**Example:**

```python
test = client.runtimes.test_runtime("python-3.11")
if test['success']:
    print(f"✅ Runtime test passed!")
    print(f"   Output: {test['output']}")
else:
    print(f"❌ Runtime test failed: {test['error']}")
```

##### install_runtime_from_github()

Install a new runtime from GitHub

```python
def install_runtime_from_github(
    runtime_spec: str,
    repository: str,
    branch: Optional[str] = None,
    path: Optional[str] = None,
    force_reinstall: bool = False,
    stream: bool = False
)
```

**Example:**

```python
# Install a custom Python runtime
install = client.runtimes.install_runtime_from_github(
    runtime_spec="python-3.12-custom",
    repository="https://github.com/company/custom-python-runtime",
    branch="main"
)
print(f"🔄 Installing runtime: {install['runtime_spec']}")
```

##### Other useful methods

```python
# Check if a runtime spec is valid
def validate_runtime_spec(runtime_spec: str) -> Dict[str, Any]

# Remove a runtime you don't need anymore
def remove_runtime(runtime: str) -> Dict[str, Any]
```

## When Things Go Wrong (Exceptions)

Sometimes stuff breaks! Here are the different types of problems you might run into, and how to handle them gracefully.

All errors inherit from `JobletException`, so you can catch them all with one catch block if you want.

**Common exceptions you'll see:**

- `ConnectionError` - Can't reach the server (network issues, wrong host/port, certificate problems)
- `AuthenticationError` - Your certificates aren't working or permissions are wrong
- `JobNotFoundError` - That job ID doesn't exist (maybe it was deleted?)
- `WorkflowNotFoundError` - That workflow ID doesn't exist
- `RuntimeNotFoundError` - Trying to use a runtime that isn't installed
- `NetworkError` - Something went wrong with network operations
- `VolumeError` - Storage volume problems
- `ValidationError` - You passed invalid parameters
- `TimeoutError` - Operation took too long

**How to handle them:**

```python
from joblet import JobletClient, JobNotFoundError, ConnectionError, JobletException

try:
    with JobletClient(
        host="joblet.company.com",
        ca_cert_path="/certs/ca.pem",
        client_cert_path="/certs/client.pem",
        client_key_path="/certs/client.key"
    ) as client:
        job = client.jobs.get_job_status("some-job-uuid")
        print(f"Job status: {job['status']}")

except JobNotFoundError:
    print("🤷 That job doesn't exist - maybe it was deleted?")

except ConnectionError as e:
    print(f"🌐 Can't connect to server: {e}")
    print("Check your host, port, and certificates!")

except AuthenticationError:
    print("🔐 Certificate authentication failed")
    print("Double-check your certificate files and permissions")

except JobletException as e:
    print(f"💥 Something else went wrong: {e}")

except Exception as e:
    print(f"😵 Unexpected error: {e}")
```

## Useful Data Types & Formats

### Job Status Values

Your jobs will be in one of these states:

- 🟡 `"pending"` - Job is waiting to start (might be queued)
- 🔵 `"running"` - Job is currently doing its thing
- 🟢 `"completed"` - Job finished successfully (exit code 0)
- 🔴 `"failed"` - Job crashed or had an error
- 🟠 `"cancelled"` - You or someone else stopped the job
- ⏰ `"scheduled"` - Job is waiting for its scheduled time

### Storage Types

When creating volumes, you can choose:

- 💾 `"filesystem"` - Regular disk storage (persistent, slower)
- ⚡ `"memory"` - RAM storage (super fast, but disappears when job ends)

### Workflow Dependencies

Want jobs to run in order? Use the `depends_on` field:

```yaml
jobs:
  - name: "download-data"
    command: "curl"
    args: [ "-o", "data.json", "https://api.example.com/data" ]

  - name: "process-data"
    command: "python"
    args: [ "process.py", "data.json" ]
    depends_on: [ "download-data" ]  # Wait for download first!

  - name: "upload-results"
    command: "python"
    args: [ "upload.py", "results.json" ]
    depends_on: [ "process-data" ]  # Then wait for processing
```

### Uploading Files

Need to get files into your job? Format them like this:

```python
uploads = [
    {
        "path": "my_script.py",
        "content": b"print('Hello from uploaded script!')",
        "mode": 0o755,  # Make it executable (Unix permissions)
        "is_directory": False
    },
    {
        "path": "config.json",
        "content": b'{"setting": "value"}',
        "mode": 0o644,  # Regular file permissions
        "is_directory": False
    }
]

job = client.jobs.run_job(
    command="python",
    args=["my_script.py"],
    uploads=uploads
)
```

### Environment Variables

Pass data to your jobs through environment variables:

```python
# Regular env vars (these will show up in logs and status)
environment = {
    "ENV": "production",
    "DEBUG": "false",
    "LOG_LEVEL": "info"
}

# Secret env vars (these get hidden from logs for security)
secret_environment = {
    "API_KEY": "super-secret-key-123",
    "DATABASE_PASSWORD": "dont-tell-anyone",
    "JWT_SECRET": "very-secret-signing-key"
}

job = client.jobs.run_job(
    command="python",
    args=["app.py"],
    environment=environment,
    secret_environment=secret_environment
)
```

---

**🎉 That's everything!** This covers all the major functionality of the Joblet Python SDK.

Want to see real examples? Check out the `examples/` directory for working code you can copy and modify.

Need help? Something not working? The error messages are pretty helpful, but feel free to check the
main [README](README.md) for more guidance!