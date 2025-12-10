# Basic Usage

Demonstrates fundamental Joblet SDK operations.

## What You'll Learn

- Connecting to a Joblet server
- Running simple jobs
- Checking job status
- Getting job logs
- Stopping running jobs
- Cleaning up jobs

## Run

```bash
python main.py
```

## Key Concepts

### Connect to Joblet

```python
from joblet import JobletClient

# Uses ~/.rnx/rnx-config.yml by default
with JobletClient() as client:
    # Your code here
    pass
```

### Run a Job

```python
job = client.jobs.run_job(
    name="hello-world",
    command="echo",
    args=["Hello from Joblet!"]
)
print(f"Job ID: {job['job_uuid']}")
```

### Check Status

```python
status = client.jobs.get_job_status(job["job_uuid"])
print(f"Status: {status['status']}")  # PENDING, RUNNING, COMPLETED, FAILED
```

### Get Logs

```python
for chunk in client.jobs.get_job_logs(job["job_uuid"]):
    print(chunk.decode(), end="")
```

### Stop a Job

```python
client.jobs.stop_job(job["job_uuid"])
```

### Clean Up

```python
client.jobs.delete_job(job["job_uuid"])
```
