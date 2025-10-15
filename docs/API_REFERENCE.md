# Joblet Python SDK - API Reference

Complete API reference for the Joblet Python SDK.

## Table of Contents

- [JobletClient](#jobletclient)
- [JobService](#jobservice)
- [NetworkService](#networkservice)
- [VolumeService](#volumeservice)
- [MonitoringService](#monitoringservice)
- [RuntimeService](#runtimeservice)

---

## JobletClient

Main client class for connecting to Joblet server.

### Constructor

```python
JobletClient(
    host: Optional[str] = None,
    port: Optional[int] = None,
    ca_cert_path: Optional[str] = None,
    client_cert_path: Optional[str] = None,
    client_key_path: Optional[str] = None,
    config_path: Optional[str] = None,
    node_name: str = "default"
)
```

**Parameters:**
- `host`: Server hostname (optional if using config file)
- `port`: Server port (default: 50051)
- `ca_cert_path`: Path to CA certificate (required, or from config)
- `client_cert_path`: Path to client certificate (required, or from config)
- `client_key_path`: Path to client private key (required, or from config)
- `config_path`: Path to config file (default: ~/.rnx/rnx-config.yml)
- `node_name`: Node name in config file (default: "default")

**Note:** Joblet always requires mTLS authentication. Certificates can be provided
explicitly or loaded from the config file.

**Example:**
```python
# Using config file (recommended)
with JobletClient() as client:
    pass

# Explicit configuration
with JobletClient(
    host="joblet.example.com",
    port=50051,
    ca_cert_path="/path/to/ca.pem",
    client_cert_path="/path/to/client.pem",
    client_key_path="/path/to/client-key.pem"
) as client:
    pass
```

### Properties

#### jobs
```python
@property
def jobs(self) -> JobService
```
Access the Job Service for managing jobs and workflows.

#### persist
```python
@property
def persist(self) -> PersistService
```
**Deprecated**: Access the Persist Service for querying historical logs and metrics.
Use `client.jobs.query_logs()` and `client.jobs.query_metrics()` instead.

Historical queries now go through the main JobletService (port 50051), which internally
proxies requests to joblet-persist via Unix socket IPC. This property is maintained for
backward compatibility.

#### networks
```python
@property
def networks(self) -> NetworkService
```
Access the Network Service for managing virtual networks.

#### volumes
```python
@property
def volumes(self) -> VolumeService
```
Access the Volume Service for managing persistent storage.

#### monitoring
```python
@property
def monitoring(self) -> MonitoringService
```
Access the Monitoring Service for system health and metrics.

#### runtimes
```python
@property
def runtimes(self) -> RuntimeService
```
Access the Runtime Service for managing execution environments.

#### node_id
```python
@property
def node_id(self) -> Optional[str]
```
Get the node ID from configuration. Returns None if not configured.

**Example:**
```python
with JobletClient() as client:
    if client.node_id:
        print(f"Connected to node: {client.node_id}")
```

### Configuration File Format

The SDK can load connection information from `~/.rnx/rnx-config.yml`:

```yaml
version: "3.0"
nodes:
  default:
    address: "joblet-server:50051"  # Required - single endpoint for all operations
    nodeId: "node-001"  # Optional: unique node identifier
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

  production:
    address: "prod-joblet:50051"  # Required - single endpoint
    nodeId: "prod-node-001"  # Optional
    cert: |
      [Production certificate]
    key: |
      [Production key]
    ca: |
      [Production CA]
```

**Configuration Fields:**
- `address` - **Required**: Joblet service endpoint (default port 50051)
  - Single endpoint for all operations including historical queries
  - Joblet internally handles persistence via Unix socket IPC
- `nodeId` - Optional: Unique identifier for the node
- `cert` - Client certificate for mTLS authentication
- `key` - Client private key for mTLS authentication
- `ca` - CA certificate for server verification (can also be placed as `~/.rnx/ca.crt`)

**Note**: Joblet runs as a unified Linux systemd service. All operations go through the main service on port 50051, which transparently handles both live streaming and historical queries via internal Unix socket communication with joblet-persist.

**Using Multiple Nodes:**
```python
# Connect to default node
with JobletClient() as client:
    pass

# Connect to production node
with JobletClient(node_name="production") as client:
    pass
```

### Methods

#### health_check()
```python
def health_check(self) -> bool
```
Check if the Joblet server is available and responsive.

**Returns:** True if server is healthy, False otherwise

**Example:**
```python
if client.health_check():
    print("Server is healthy")
else:
    print("Server is unavailable")
```

---

## JobService

Service for managing jobs and workflows.

### Job Management

#### run_job()
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
    uploads: Optional[List[Dict[str, Any]]] = None,
    gpu_count: Optional[int] = None,
    gpu_memory_mb: Optional[int] = None
) -> Dict[str, Any]
```

Run a new job on the Joblet server.

**Example:**
```python
job = client.jobs.run_job(
    command="python",
    args=["train.py", "--epochs", "100"],
    name="ml-training",
    max_cpu=400,  # 4 cores
    max_memory=8192,  # 8GB
    gpu_count=1,
    runtime="python-3.11-ml",
    environment={"BATCH_SIZE": "32"}
)
print(f"Job ID: {job['job_uuid']}")
```

#### get_job_status()
```python
def get_job_status(job_uuid: str) -> Dict[str, Any]
```

Get the current status of a job.

**Returns:** Dictionary with job status, timing, resources, etc.

**Example:**
```python
status = client.jobs.get_job_status(job_uuid)
print(f"Status: {status['status']}")
print(f"Exit code: {status['exit_code']}")
```

#### stop_job()
```python
def stop_job(job_uuid: str) -> Dict[str, Any]
```

Stop a running job (sends SIGTERM).

#### cancel_job()
```python
def cancel_job(job_uuid: str) -> Dict[str, Any]
```

Cancel a scheduled job (before it starts).

#### delete_job()
```python
def delete_job(job_uuid: str) -> Dict[str, Any]
```

Delete a job (removes from history).

### Log Streaming

#### get_job_logs()
```python
def get_job_logs(
    job_uuid: str,
    include_historical: bool = True
) -> Iterator[bytes]
```

**Smart log streaming** - automatically fetches historical logs then streams live logs.

This method intelligently handles both historical and live logs:
1. First fetches any historical logs (internally from joblet-persist via IPC)
2. Then streams live logs from the running job

All operations go through a single endpoint (port 50051), with internal Unix socket
proxying for historical data.

**Parameters:**
- `job_uuid`: Job UUID or short UUID prefix
- `include_historical`: If True, fetch historical logs first (default: True)

**Returns:** Iterator yielding log chunks as bytes

**Example:**
```python
# Get all logs (historical + live) - works for any job!
for chunk in client.jobs.get_job_logs(job_uuid):
    print(chunk.decode('utf-8'), end='', flush=True)

# Get only live logs (skip historical)
for chunk in client.jobs.get_job_logs(job_uuid, include_historical=False):
    print(chunk.decode('utf-8'), end='', flush=True)
```

**Behavior:**
- **Completed job**: Fetches all logs from historical storage
- **Running job**: Streams live logs as they're generated
- **Reconnecting**: Shows historical logs, then continues with live stream
- **Graceful fallback**: Works even if historical data unavailable

#### stream_live_logs()
```python
def stream_live_logs(job_uuid: str) -> Iterator[bytes]
```

Stream only live logs (convenience method that skips historical logs).

**Example:**
```python
for chunk in client.jobs.stream_live_logs(job_uuid):
    print(chunk.decode('utf-8'), end='', flush=True)
```

### Workflow Management

#### run_workflow()
```python
def run_workflow(
    workflow: str,
    yaml_content: Optional[str] = None,
    workflow_files: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]
```

Run a multi-job workflow.

#### get_workflow_status()
```python
def get_workflow_status(workflow_uuid: str) -> Dict[str, Any]
```

Get workflow status and all job statuses.

#### list_workflows()
```python
def list_workflows(include_completed: bool = False) -> List[Dict[str, Any]]
```

List all workflows.

### Historical Data Queries

#### query_logs()
```python
def query_logs(
    job_id: str,
    stream: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    limit: int = 0,
    offset: int = 0
) -> Iterator[Dict[str, Any]]
```

Query historical logs for a job from persistent storage.

**Note**: All queries go through the JobletService (port 50051), which internally proxies
requests to joblet-persist via Unix socket IPC.

**Parameters:**
- `job_id`: Job UUID
- `stream`: Stream filter ("stdout", "stderr", or None for both)
- `start_time`: Start time in Unix nanoseconds
- `end_time`: End time in Unix nanoseconds
- `limit`: Maximum lines to return (0 = all)
- `offset`: Skip lines

**Returns:** Iterator yielding log line dictionaries

**Example:**
```python
# Query all logs
for log in client.jobs.query_logs(job_id="abc123"):
    timestamp = datetime.fromtimestamp(log['timestamp'] / 1e9)
    content = log['content'].decode('utf-8')
    print(f"[{timestamp}] {content}")

# Query only stdout logs
for log in client.jobs.query_logs(job_id="abc123", stream="stdout"):
    print(log['content'].decode('utf-8'))

# Query with time range
five_sec_ago = int((time.time() - 5) * 1e9)
now = int(time.time() * 1e9)
for log in client.jobs.query_logs(job_id="abc123", start_time=five_sec_ago, end_time=now):
    print(log['content'].decode('utf-8'))
```

#### query_metrics()
```python
def query_metrics(
    job_id: str,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    limit: int = 0,
    offset: int = 0
) -> Iterator[Dict[str, Any]]
```

Query historical metrics for a job from persistent storage.

**Note**: All queries go through the JobletService (port 50051), which internally proxies
requests to joblet-persist via Unix socket IPC.

**Parameters:**
- `job_id`: Job UUID
- `start_time`: Start time in Unix nanoseconds
- `end_time`: End time in Unix nanoseconds
- `limit`: Maximum samples to return (0 = all)
- `offset`: Skip samples

**Returns:** Iterator yielding metric dictionaries with CPU, memory, GPU, disk, and network data

**Example:**
```python
for metric in client.jobs.query_metrics(job_id="abc123"):
    cpu = metric['data'].get('cpu_usage', 0)
    memory_mb = metric['data'].get('memory_usage', 0) / (1024 * 1024)
    print(f"CPU: {cpu:.2f}%, Memory: {memory_mb:.2f} MB")
```

---

## NetworkService

Service for managing isolated virtual networks.

### create_network()
```python
def create_network(name: str, cidr: str) -> Dict[str, Any]
```

Create a new network.

**Example:**
```python
network = client.networks.create_network(
    name="ml-network",
    cidr="10.0.1.0/24"
)
```

### list_networks()
```python
def list_networks() -> List[Dict[str, Any]]
```

List all networks.

### remove_network()
```python
def remove_network(name: str) -> Dict[str, Any]
```

Remove a network.

---

## VolumeService

Service for managing persistent storage volumes.

### create_volume()
```python
def create_volume(
    name: str,
    size: str,
    volume_type: str = "filesystem"
) -> Dict[str, Any]
```

Create a new volume.

**Example:**
```python
volume = client.volumes.create_volume(
    name="data-vol",
    size="10GB",
    volume_type="filesystem"
)
```

### list_volumes()
```python
def list_volumes() -> List[Dict[str, Any]]
```

List all volumes.

### remove_volume()
```python
def remove_volume(name: str) -> Dict[str, Any]
```

Remove a volume.

---

## MonitoringService

Service for system health and metrics streaming.

### get_system_status()
```python
def get_system_status() -> Dict[str, Any]
```

Get current system status.

**Example:**
```python
status = client.monitoring.get_system_status()
print(f"CPU: {status['cpu']['usage_percent']:.1f}%")
print(f"Memory: {status['memory']['usage_percent']:.1f}%")
```

### stream_system_metrics()
```python
def stream_system_metrics(
    interval_seconds: int = 5,
    metric_types: Optional[List[str]] = None
) -> Iterator[Dict[str, Any]]
```

Stream real-time system metrics.

**Example:**
```python
for metrics in client.monitoring.stream_system_metrics(interval_seconds=2):
    cpu = metrics['cpu']['usage_percent']
    memory = metrics['memory']['usage_percent']
    print(f"CPU: {cpu:.1f}%, Memory: {memory:.1f}%")

    if cpu > 90:
        break
```

---

## RuntimeService

Service for managing execution environments.

### list_runtimes()
```python
def list_runtimes() -> List[Dict[str, Any]]
```

List all available runtimes.

### get_runtime_info()
```python
def get_runtime_info(runtime: str) -> Dict[str, Any]
```

Get detailed information about a runtime.

### test_runtime()
```python
def test_runtime(runtime: str) -> Dict[str, Any]
```

Test if a runtime is working correctly.

**Example:**
```python
result = client.runtimes.test_runtime("python-3.11")
if result['success']:
    print("Runtime is working!")
else:
    print(f"Runtime test failed: {result['error']}")
```

### install_runtime_from_github()
```python
def install_runtime_from_github(
    runtime_spec: str,
    repository: str,
    branch: str = "main",
    path: str = "",
    force_reinstall: bool = False
) -> Dict[str, Any]
```

Install a runtime from a GitHub repository.

### remove_runtime()
```python
def remove_runtime(runtime: str) -> Dict[str, Any]
```

Remove an installed runtime.

---

## Error Handling

All SDK methods raise specific exception types for different error conditions:

### Exception Classes

```python
from joblet import (
    JobletException,          # Base exception
    ConnectionError,          # Connection failures
    AuthenticationError,      # Authentication failures
    JobNotFoundError,         # Job not found
    WorkflowNotFoundError,    # Workflow not found
    RuntimeNotFoundError,     # Runtime not found
    NetworkError,             # Network operation errors
    VolumeError,              # Volume operation errors
    ValidationError,          # Input validation errors
    TimeoutError              # Operation timeouts
)
```

**Example:**
```python
from joblet import JobletClient, JobNotFoundError, ConnectionError

try:
    with JobletClient() as client:
        status = client.jobs.get_job_status("invalid-uuid")
except JobNotFoundError as e:
    print(f"Job not found: {e}")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Related Projects

- **[Joblet](https://github.com/ehsaniara/joblet)** - Main orchestration system (server-side)
- **[joblet-proto](https://github.com/ehsaniara/joblet-proto)** - Protocol Buffer definitions
- **rnx** - Official CLI tool (included in Joblet repo)

---

## See Also

- [User Guide](USER_GUIDE.md) - Detailed usage guide and best practices
- [Examples](../examples/) - Complete example scripts
- [CHANGELOG](../CHANGELOG.md) - Version history and changes
- [Joblet Installation Guide](https://github.com/ehsaniara/joblet/blob/main/docs/INSTALLATION.md) - Server setup
