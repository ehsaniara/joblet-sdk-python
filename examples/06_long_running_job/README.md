# Long-Running Job Demo

Demonstrates managing long-running jobs with live and historical logs.

## What You'll Learn

- Running long-duration jobs
- Streaming logs during execution
- Retrieving complete logs after completion
- No data loss between streaming sessions

## Run

```bash
python main.py
```

This example runs a 60-second job that outputs 600 lines.

## Key Concepts

### Submit Long-Running Job

```python
job = client.jobs.run_job(
    name="long-counter",
    command="bash",
    args=["-c", "for i in {1..600}; do echo Counter: $i; sleep 0.1; done"]
)
```

### Stream Live (Partial)

Watch output in real-time, then disconnect:

```python
start = time.time()
for chunk in client.jobs.stream_live_logs(job["job_uuid"]):
    print(chunk.decode(), end="", flush=True)

    # Stop streaming after 10 seconds
    if time.time() - start > 10:
        break  # Job continues running
```

### Wait for Completion

```python
while True:
    status = client.jobs.get_job_status(job["job_uuid"])
    if status["status"] not in ["PENDING", "RUNNING"]:
        break
    time.sleep(2)

print(f"Exit code: {status.get('exit_code')}")
```

### Retrieve Complete Logs

After job finishes, get ALL output:

```python
all_lines = 0
for chunk in client.jobs.get_job_logs(job["job_uuid"]):
    print(chunk.decode(), end="")
    all_lines += 1

print(f"Total lines retrieved: {all_lines}")  # 600
```

## No Data Loss

```
Live streaming (10 seconds): ~100 lines
Historical retrieval:        600 lines (complete!)

Difference: 500 lines captured while not streaming
```

This demonstrates:
- Live logs stream in real-time
- Historical logs capture everything
- No output is ever lost
