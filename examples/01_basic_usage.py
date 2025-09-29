#!/usr/bin/env python3
"""
Basic Joblet SDK Usage Examples

This script demonstrates the fundamental operations with Joblet:
1. Running a simple job
2. Checking job status
3. Getting job logs
4. Canceling a job
"""

import time

from joblet import JobletClient


def main():
    # Initialize client
    client = JobletClient(host="localhost", port=8080)

    print("=== Basic Job Example ===\n")

    # 1. Run a simple job
    job = client.run_job(
        name="hello-world", command="echo", args=["Hello from Joblet!"]
    )
    print(f"✓ Job submitted: {job.uuid}")

    # 2. Check job status
    status = client.get_job_status(job.uuid)
    print(f"✓ Status: {status.status}")

    # Wait for completion
    while status.status in ["pending", "running"]:
        time.sleep(1)
        status = client.get_job_status(job.uuid)

    print(f"✓ Final status: {status.status}")
    print(f"✓ Exit code: {status.exit_code}")

    # 3. Get job logs
    print("\nJob output:")
    for chunk in client.get_job_logs(job.uuid):
        print(chunk.decode(), end="")

    print("\n=== Long-Running Job with Cancellation ===\n")

    # Run a longer job that we can cancel
    long_job = client.run_job(
        name="long-runner",
        command="bash",
        args=["-c", "for i in {1..100}; do echo $i; sleep 1; done"],
    )
    print(f"✓ Long job submitted: {long_job.uuid}")

    # Let it run for a few seconds
    time.sleep(3)

    # Cancel the job
    result = client.cancel_job(long_job.uuid)
    print(f"✓ Job canceled: {result.status}")

    # Clean up
    client.delete_job(job.uuid)
    client.delete_job(long_job.uuid)
    print("\n✓ Jobs cleaned up")


if __name__ == "__main__":
    main()
