# Streaming Logs

Demonstrates real-time log streaming from running jobs.

## What You'll Learn

- Live log streaming
- Smart log streaming (historical + live)
- Concurrent log and status monitoring
- Reconnecting to running jobs

## Run

```bash
python main.py
```

## Key Concepts

### Smart Streaming (Recommended)

Gets historical logs first, then continues with live streaming:

```python
for chunk in client.jobs.get_job_logs(job_uuid):
    print(chunk.decode(), end="", flush=True)
```

This works for:
- Running jobs (streams live)
- Completed jobs (fetches historical)
- Reconnecting mid-job (historical + live)

### Live-Only Streaming

Skip historical logs and only show new output:

```python
for chunk in client.jobs.stream_live_logs(job_uuid):
    print(chunk.decode(), end="", flush=True)
```

### Concurrent Monitoring

Stream logs while monitoring status:

```python
import threading

def stream_logs(client, job_uuid):
    for chunk in client.jobs.get_job_logs(job_uuid):
        print(chunk.decode(), end="", flush=True)

# Start streaming in background
log_thread = threading.Thread(
    target=stream_logs,
    args=(client, job["job_uuid"])
)
log_thread.daemon = True
log_thread.start()

# Monitor status in main thread
while True:
    status = client.jobs.get_job_status(job["job_uuid"])
    if status["status"] in ["COMPLETED", "FAILED"]:
        break
    time.sleep(1)
```

### Reconnect Scenario

If you disconnect and reconnect, `get_job_logs()` gives you everything:

```python
# Start job
job = client.jobs.run_job(...)

# Disconnect for 10 seconds
time.sleep(10)

# Reconnect - gets ALL logs (historical + continuing live)
for chunk in client.jobs.get_job_logs(job["job_uuid"]):
    print(chunk.decode(), end="")
```
