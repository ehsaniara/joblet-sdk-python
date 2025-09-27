#!/usr/bin/env python3
"""
Advanced Joblet Features

This script demonstrates advanced Joblet features:
1. Resource limits (CPU, memory)
2. Environment variables
3. File uploads
4. Scheduled jobs
5. GPU usage (if available)
"""

from datetime import datetime, timedelta

from joblet import JobletClient


def resource_limits_example(client):
    """Example: Running jobs with resource limits"""
    print("=== Resource Limits Example ===\n")

    job = client.run_job(
        name="resource-limited",
        command="stress",
        args=["--cpu", "1", "--timeout", "5s"],
        max_cpu=50,  # 50% CPU limit
        max_memory=100,  # 100MB memory limit
    )

    print(f"✓ Job with resource limits: {job.uuid}")
    print("  CPU limit: 50%")
    print("  Memory limit: 100MB")

    # Wait for completion
    status = client.wait_for_job(job.uuid, timeout=10)
    print(f"✓ Job completed: {status.status}\n")

    client.delete_job(job.uuid)


def environment_variables_example(client):
    """Example: Using environment variables"""
    print("=== Environment Variables Example ===\n")

    job = client.run_job(
        name="env-vars",
        command="bash",
        args=["-c", "echo Hello $USER from $ENVIRONMENT"],
        environment={"USER": "Joblet", "ENVIRONMENT": "production"},
    )

    print(f"✓ Job with env vars: {job.uuid}")

    # Get output
    client.wait_for_job(job.uuid, timeout=5)
    for chunk in client.get_job_logs(job.uuid):
        print(f"  Output: {chunk.decode().strip()}")

    print()
    client.delete_job(job.uuid)


def file_upload_example(client):
    """Example: Uploading files with a job"""
    print("=== File Upload Example ===\n")

    # Create a simple Python script to upload
    script_content = """#!/usr/bin/env python3
import sys
print(f"Hello from uploaded script!")
print(f"Arguments: {sys.argv[1:]}")
"""

    job = client.run_job(
        name="file-upload",
        command="python3",
        args=["/tmp/script.py", "arg1", "arg2"],
        uploads=[
            {
                "path": "/tmp/script.py",
                "content": script_content.encode(),
                "mode": 0o755,
            }
        ],
    )

    print(f"✓ Job with file upload: {job.uuid}")

    # Wait and get output
    client.wait_for_job(job.uuid, timeout=5)
    print("  Output:")
    for chunk in client.get_job_logs(job.uuid):
        print(f"    {chunk.decode().strip()}")

    print()
    client.delete_job(job.uuid)


def scheduled_job_example(client):
    """Example: Scheduling a job for future execution"""
    print("=== Scheduled Job Example ===\n")

    # Schedule a job to run in 5 seconds
    future_time = datetime.now() + timedelta(seconds=5)
    schedule_time = future_time.strftime("%Y-%m-%dT%H:%M:%S")

    job = client.run_job(
        name="scheduled-job",
        command="date",
        args=["+%Y-%m-%d %H:%M:%S"],
        schedule=schedule_time,
    )

    print(f"✓ Scheduled job: {job.uuid}")
    print(f"  Scheduled for: {schedule_time}")
    print("  Waiting for execution...")

    # Wait for the job to complete
    client.wait_for_job(job.uuid, timeout=10)

    print("✓ Job executed at scheduled time")
    for chunk in client.get_job_logs(job.uuid):
        print(f"  Output: {chunk.decode().strip()}")

    print()
    client.delete_job(job.uuid)


def gpu_job_example(client):
    """Example: Running a job with GPU resources (if available)"""
    print("=== GPU Job Example ===\n")

    try:
        job = client.run_job(
            name="gpu-job",
            command="nvidia-smi",
            args=[],
            gpu_count=1,
            gpu_memory_mb=1024,
        )

        print(f"✓ GPU job: {job.uuid}")
        print("  GPUs: 1")
        print("  GPU Memory: 1024MB")

        client.wait_for_job(job.uuid, timeout=10)

        print("  GPU Info:")
        for chunk in client.get_job_logs(job.uuid):
            output = chunk.decode()
            if output.strip():
                print(f"    {output.strip()[:100]}...")  # Show first 100 chars
                break

        client.delete_job(job.uuid)
    except Exception as e:
        print(f"  ⚠ GPU not available or nvidia-smi not installed: {e}")

    print()


def main():
    # Initialize client
    client = JobletClient(host="localhost", port=8080)

    try:
        # Run examples
        resource_limits_example(client)
        environment_variables_example(client)
        file_upload_example(client)
        scheduled_job_example(client)
        gpu_job_example(client)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up any remaining jobs
        try:
            jobs = client.list_jobs()
            for job in jobs:
                client.delete_job(job.uuid)
        except Exception:
            pass


if __name__ == "__main__":
    main()
