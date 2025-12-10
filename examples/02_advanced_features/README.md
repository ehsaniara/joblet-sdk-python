# Advanced Features

Demonstrates advanced Joblet capabilities for production workloads.

## What You'll Learn

- Resource limits (CPU, memory)
- Environment variables
- Scheduled jobs
- GPU resource allocation
- Network management
- Volume management

## Run

```bash
python main.py
```

## Key Concepts

### Resource Limits

```python
job = client.jobs.run_job(
    name="resource-limited",
    command="python",
    args=["compute.py"],
    max_cpu=50,           # 50% CPU (0.5 cores)
    max_memory=104857600  # 100MB in bytes
)
```

### Environment Variables

```python
job = client.jobs.run_job(
    name="with-env",
    command="bash",
    args=["-c", "echo Hello $USER from $ENV"],
    environment={
        "USER": "Joblet",
        "ENV": "production"
    }
)
```

### Scheduled Jobs

```python
from datetime import datetime, timedelta

future = datetime.now() + timedelta(minutes=5)
schedule_time = future.strftime("%Y-%m-%dT%H:%M:%SZ")

job = client.jobs.run_job(
    name="scheduled",
    command="echo",
    args=["Running on schedule"],
    schedule=schedule_time
)
```

### GPU Resources

```python
job = client.jobs.run_job(
    name="gpu-job",
    command="nvidia-smi",
    gpu_count=1,
    gpu_memory_mb=4096,
    runtime="python-3.11-pytorch-cuda"
)
```

### Networks

```python
# Create isolated network
network = client.networks.create_network(
    name="ml-net",
    cidr="10.100.0.0/24"
)

# Use in job
job = client.jobs.run_job(
    command="python",
    args=["server.py"],
    network="ml-net"
)

# Clean up
client.networks.remove_network("ml-net")
```

### Volumes

```python
# Create persistent volume
volume = client.volumes.create_volume(
    name="data-vol",
    size_mb=1000
)

# Mount in job
job = client.jobs.run_job(
    command="python",
    args=["process.py"],
    volumes=["data-vol:/data"]
)

# Clean up
client.volumes.remove_volume("data-vol")
```
