# Smart Log Streaming

Demonstrates intelligent log streaming that works like `rnx job log`.

## What You'll Learn

- Automatic historical + live log handling
- Seamless access to any job's logs
- Reconnecting with full history
- Live-only streaming option

## Run

```bash
python main.py
```

## How It Works

`client.jobs.get_job_logs()` automatically handles:

1. **Completed Jobs**: Fetches from historical storage
2. **Running Jobs**: Streams live logs
3. **Reconnecting**: Gets historical logs, then continues live

All through a single API call - just like `rnx job log`.

## Key Concepts

### Universal Log Access

```python
# Works for ANY job - running or completed
for chunk in client.jobs.get_job_logs(job_uuid):
    print(chunk.decode(), end="")
```

### Completed Job Logs

```python
# Run and wait for completion
job = client.jobs.run_job(...)
while status["status"] not in ["COMPLETED", "FAILED"]:
    time.sleep(0.5)
    status = client.jobs.get_job_status(job["job_uuid"])

# Get all historical logs
for chunk in client.jobs.get_job_logs(job["job_uuid"]):
    print(chunk.decode(), end="")
```

### Running Job Logs

```python
# Start a long-running job
job = client.jobs.run_job(
    command="bash",
    args=["-c", "for i in {1..60}; do echo $i; sleep 1; done"]
)

# Stream logs as they're produced
for chunk in client.jobs.get_job_logs(job["job_uuid"]):
    print(chunk.decode(), end="", flush=True)
```

### Reconnect Mid-Job

```python
# Start job
job = client.jobs.run_job(...)

# Let it run for a while
time.sleep(10)

# Reconnect - seamlessly gets:
# 1. Historical logs (everything that happened)
# 2. Live logs (continuing stream)
for chunk in client.jobs.get_job_logs(job["job_uuid"]):
    print(chunk.decode(), end="", flush=True)
```

### Skip Historical (Live Only)

```python
# Only see new output (skip what already happened)
for chunk in client.jobs.stream_live_logs(job_uuid):
    print(chunk.decode(), end="", flush=True)
```

## Architecture

```
┌─────────────┐
│   Client    │
│ get_job_logs│
└──────┬──────┘
       │ gRPC (port 50051)
       ▼
┌─────────────┐
│   Joblet    │
│   Server    │
└──────┬──────┘
       │ Internal IPC
       ▼
┌─────────────┐
│   Persist   │ (historical data)
└─────────────┘
```

The server handles historical data internally - clients just call one method.
