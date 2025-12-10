# Historical Logs and Metrics

Demonstrates retrieving logs and metrics from completed jobs.

## What You'll Learn

- Fetching all logs after job completion
- Retrieving job metrics (CPU, memory usage)
- Client-side filtering and statistics
- Time-range filtering

## Run

```bash
python main.py
```

## Key Concepts

### Get All Logs

```python
# Run a job
job = client.jobs.run_job(
    command="bash",
    args=["-c", "for i in {1..100}; do echo Line $i; done"],
    name="log-example"
)

# Wait for completion
while True:
    status = client.jobs.get_job_status(job["job_uuid"])
    if status["status"] in ["COMPLETED", "FAILED"]:
        break
    time.sleep(0.5)

# Get all logs
all_logs = b""
for chunk in client.jobs.get_job_logs(job["job_uuid"]):
    all_logs += chunk

print(all_logs.decode())
```

### Get Job Metrics

```python
# Collect all metrics
metrics = list(client.jobs.get_job_metrics(job["job_uuid"]))

for m in metrics:
    timestamp = datetime.fromtimestamp(m["timestamp"] / 1e9)
    print(f"[{timestamp}] CPU: {m['cpu_usage']:.1f}%, "
          f"Memory: {m['memory_usage'] / 1e6:.1f} MB")
```

### Calculate Statistics

```python
metrics = list(client.jobs.get_job_metrics(job_uuid))

cpu_values = [m["cpu_usage"] for m in metrics]
memory_values = [m["memory_usage"] / (1024 * 1024) for m in metrics]

print(f"CPU - Avg: {sum(cpu_values)/len(cpu_values):.1f}%, "
      f"Peak: {max(cpu_values):.1f}%")
print(f"Memory - Avg: {sum(memory_values)/len(memory_values):.1f} MB, "
      f"Peak: {max(memory_values):.1f} MB")
```

### Client-Side Time Filtering

```python
all_metrics = list(client.jobs.get_job_metrics(job_uuid))

# Get last 5 samples
last_5 = all_metrics[-5:]

# Get metrics from last 5 seconds
now_ns = all_metrics[-1]["timestamp"]
five_sec_ago = now_ns - (5 * 1_000_000_000)
recent = [m for m in all_metrics if m["timestamp"] >= five_sec_ago]
```

## API Notes

The server streams ALL available data. Filtering is done client-side for flexibility:
- No server-side pagination needed
- Filter by time, count, or any custom criteria
- Calculate statistics on complete datasets
