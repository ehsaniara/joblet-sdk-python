#!/usr/bin/env python3
"""
Basic Joblet SDK Usage Examples

This script demonstrates the fundamental operations with Joblet:
1. Running a simple job
2. Checking job status
3. Getting job logs (with smart streaming)
4. Stopping a job
"""

import time

from joblet import JobletClient


def main():
    # Initialize client - uses ~/.rnx/rnx-config.yml by default
    with JobletClient() as client:
        print("=== Basic Job Example ===\n")

        # 1. Run a simple job
        job = client.jobs.run_job(
            name="hello-world", command="echo", args=["Hello from Joblet!"]
        )
        print(f"✓ Job submitted: {job['job_uuid']}")

        # 2. Check job status
        status = client.jobs.get_job_status(job["job_uuid"])
        print(f"✓ Status: {status['status']}")

        # Wait for completion
        while status["status"] in ["PENDING", "RUNNING"]:
            time.sleep(0.5)
            status = client.jobs.get_job_status(job["job_uuid"])

        print(f"✓ Final status: {status['status']}")
        print(f"✓ Exit code: {status.get('exit_code', 'N/A')}")

        # 3. Get job logs (smart streaming - gets historical + live logs)
        print("\nJob output:")
        for chunk in client.jobs.get_job_logs(job["job_uuid"]):
            print(chunk.decode(), end="")

        print("\n=== Long-Running Job with Stop ===\n")

        # Run a longer job that we can stop
        long_job = client.jobs.run_job(
            name="long-runner",
            command="bash",
            args=["-c", "for i in {1..100}; do echo Count: $i; sleep 1; done"],
        )
        print(f"✓ Long job submitted: {long_job['job_uuid']}")

        # Let it run for a few seconds
        time.sleep(3)

        # Stop the job
        result = client.jobs.stop_job(long_job["job_uuid"])
        print(f"✓ Job stopped: {result['status']}")

        # Get logs from the stopped job
        print("\nPartial output from stopped job:")
        for chunk in client.jobs.get_job_logs(long_job["job_uuid"]):
            print(chunk.decode(), end="")

        # Clean up
        client.jobs.delete_job(job["job_uuid"])
        client.jobs.delete_job(long_job["job_uuid"])
        print("\n✓ Jobs cleaned up")


if __name__ == "__main__":
    main()
