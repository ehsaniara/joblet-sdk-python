#!/usr/bin/env python3
"""
Advanced Joblet Features

This script demonstrates advanced Joblet features:
1. Resource limits (CPU, memory)
2. Execution timeout (requires Joblet server v5.6.x / proto v2.5.9+)
3. Environment variables
4. Scheduled jobs
5. GPU usage (if available)
6. Network and volume management
"""

import time
from datetime import datetime, timedelta

from joblet import JobletClient


def resource_limits_example(client):
    """Example: Running jobs with resource limits"""
    print("=== Resource Limits Example ===\n")

    job = client.jobs.run_job(
        name="resource-limited",
        command="bash",
        args=["-c", "echo 'Testing resource limits'; sleep 2; echo 'Done'"],
        max_cpu=50,  # 50% CPU limit (0.5 cores)
        max_memory=104857600,  # 100MB memory limit in bytes
    )

    print(f"✓ Job with resource limits: {job['job_uuid']}")
    print("  CPU limit: 50% (0.5 cores)")
    print("  Memory limit: 100MB")

    # Wait for completion
    status = client.jobs.get_job_status(job["job_uuid"])
    while status["status"] in ["PENDING", "RUNNING"]:
        time.sleep(0.5)
        status = client.jobs.get_job_status(job["job_uuid"])

    print(f"✓ Job completed: {status['status']}\n")

    client.jobs.delete_job(job["job_uuid"])


def timeout_example(client):
    """Example: Bounding a job's run time with an execution timeout.

    ``timeout`` accepts a Go-style duration string ("30s", "5m", "1h").
    The Joblet server terminates the job once the limit is reached, so a
    command that would otherwise run forever finishes in a bounded time and
    reports a failed/terminated status instead of hanging.

    Requires Joblet server v5.6.x (proto v2.5.9+); older servers ignore the
    field.
    """
    print("=== Execution Timeout Example ===\n")

    # `sleep 30` would run for 30s, but the 3s timeout cuts it short.
    job = client.jobs.run_job(
        name="timeout-demo",
        command="bash",
        args=["-c", "echo 'starting long task'; sleep 30; echo 'never reached'"],
        timeout="3s",
    )

    print(f"✓ Job with 3s timeout: {job['job_uuid']}")
    print("  Command would sleep 30s, but should be terminated at ~3s")

    start = time.time()
    status = client.jobs.get_job_status(job["job_uuid"])
    while status["status"] in ["PENDING", "RUNNING"]:
        time.sleep(0.5)
        status = client.jobs.get_job_status(job["job_uuid"])

    elapsed = time.time() - start
    print(f"✓ Job ended after ~{elapsed:.1f}s with status: {status['status']}")
    print("  (expected well under 30s — the timeout terminated it)\n")

    client.jobs.delete_job(job["job_uuid"])


def environment_variables_example(client):
    """Example: Using environment variables"""
    print("=== Environment Variables Example ===\n")

    job = client.jobs.run_job(
        name="env-vars",
        command="bash",
        args=["-c", "echo Hello $USER from $ENVIRONMENT"],
        environment={"USER": "Joblet", "ENVIRONMENT": "production"},
    )

    print(f"✓ Job with env vars: {job['job_uuid']}")

    # Wait and get output
    status = client.jobs.get_job_status(job["job_uuid"])
    while status["status"] in ["PENDING", "RUNNING"]:
        time.sleep(0.5)
        status = client.jobs.get_job_status(job["job_uuid"])

    print("  Output:")
    for chunk in client.jobs.get_job_logs(job["job_uuid"]):
        output = chunk.decode().strip()
        if output:
            print(f"    {output}")

    print()
    client.jobs.delete_job(job["job_uuid"])


def scheduled_job_example(client):
    """Example: Scheduling a job for future execution"""
    print("=== Scheduled Job Example ===\n")

    # Schedule a job to run in 5 seconds
    future_time = datetime.now() + timedelta(seconds=5)
    schedule_time = future_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    job = client.jobs.run_job(
        name="scheduled-job",
        command="date",
        args=["+%Y-%m-%d %H:%M:%S"],
        schedule=schedule_time,
    )

    print(f"✓ Scheduled job: {job['job_uuid']}")
    print(f"  Scheduled for: {schedule_time}")
    print("  Waiting for execution...")

    # Wait for the job to complete
    status = client.jobs.get_job_status(job["job_uuid"])
    while status["status"] in ["PENDING", "SCHEDULED", "RUNNING"]:
        time.sleep(1)
        status = client.jobs.get_job_status(job["job_uuid"])

    print("✓ Job executed at scheduled time")
    for chunk in client.jobs.get_job_logs(job["job_uuid"]):
        output = chunk.decode().strip()
        if output:
            print(f"  Output: {output}")

    print()
    client.jobs.delete_job(job["job_uuid"])


def gpu_job_example(client):
    """Example: Running a job with GPU resources (if available)"""
    print("=== GPU Job Example ===\n")

    try:
        job = client.jobs.run_job(
            name="gpu-job",
            command="nvidia-smi",
            args=["--query-gpu=name,memory.total", "--format=csv"],
            gpu_count=1,
            gpu_memory_mb=1024,
        )

        print(f"✓ GPU job: {job['job_uuid']}")
        print("  GPUs: 1")
        print("  GPU Memory: 1024MB")

        # Wait for completion
        status = client.jobs.get_job_status(job["job_uuid"])
        while status["status"] in ["PENDING", "RUNNING"]:
            time.sleep(0.5)
            status = client.jobs.get_job_status(job["job_uuid"])

        print("  GPU Info:")
        for chunk in client.jobs.get_job_logs(job["job_uuid"]):
            output = chunk.decode().strip()
            if output:
                print(f"    {output}")

        client.jobs.delete_job(job["job_uuid"])
    except Exception as e:
        print(f"  ⚠ GPU not available or nvidia-smi not installed: {e}")

    print()


def network_example(client):
    """Example: Creating and using custom networks"""
    print("=== Network Management Example ===\n")

    try:
        # List existing networks
        networks = client.networks.list_networks()
        print(f"✓ Found {len(networks)} existing networks")

        # Create a custom network
        network = client.networks.create_network(name="test-net", cidr="10.100.0.0/24")
        print(f"✓ Created network: {network['name']} ({network['cidr']})")

        # Run a job with the custom network
        job = client.jobs.run_job(
            name="network-test", command="ip", args=["addr", "show"], network="test-net"
        )

        print(f"✓ Job with custom network: {job['job_uuid']}")

        # Wait for completion
        status = client.jobs.get_job_status(job["job_uuid"])
        while status["status"] in ["PENDING", "RUNNING"]:
            time.sleep(0.5)
            status = client.jobs.get_job_status(job["job_uuid"])

        # Clean up
        client.jobs.delete_job(job["job_uuid"])
        client.networks.remove_network("test-net")
        print("✓ Cleaned up network")

    except Exception as e:
        print(f"  ⚠ Network features may not be available: {e}")

    print()


def volume_example(client):
    """Example: Creating and using persistent volumes"""
    print("=== Volume Management Example ===\n")

    try:
        # List existing volumes
        volumes = client.volumes.list_volumes()
        print(f"✓ Found {len(volumes)} existing volumes")

        # Create a volume
        volume = client.volumes.create_volume(name="test-data", size="100MB")
        print(f"✓ Created volume: {volume['name']} ({volume.get('size', 'N/A')})")

        # Run a job that uses the volume
        job = client.jobs.run_job(
            name="volume-test",
            command="bash",
            args=["-c", "echo 'test data' > /data/test.txt && cat /data/test.txt"],
            volumes=["test-data:/data"],
        )

        print(f"✓ Job with volume: {job['job_uuid']}")

        # Wait for completion
        status = client.jobs.get_job_status(job["job_uuid"])
        while status["status"] in ["PENDING", "RUNNING"]:
            time.sleep(0.5)
            status = client.jobs.get_job_status(job["job_uuid"])

        print("  Output:")
        for chunk in client.jobs.get_job_logs(job["job_uuid"]):
            output = chunk.decode().strip()
            if output:
                print(f"    {output}")

        # Clean up
        client.jobs.delete_job(job["job_uuid"])
        client.volumes.remove_volume("test-data")
        print("✓ Cleaned up volume")

    except Exception as e:
        print(f"  ⚠ Volume features may not be available: {e}")

    print()


def main():
    # Initialize client
    with JobletClient() as client:
        try:
            # Run examples
            resource_limits_example(client)
            timeout_example(client)
            environment_variables_example(client)
            scheduled_job_example(client)
            gpu_job_example(client)
            network_example(client)
            volume_example(client)

            print("✓ All examples completed!")

        except Exception as e:
            print(f"Error: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
