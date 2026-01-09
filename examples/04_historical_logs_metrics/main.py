#!/usr/bin/env python3
"""
Example 04: Retrieving Job Logs and Metrics

This example demonstrates how to retrieve job logs and metrics from the server.
In proto v2.3.0, the server streams ALL available logs and metrics for a job,
and clients can filter the results as needed.

The server handles historical data internally via IPC to the persist subprocess,
providing a unified API through the JobService (port 50051).
"""

from datetime import datetime

from joblet import JobletClient


def example_get_job_logs():
    """Get all logs for a completed job"""
    print("=" * 60)
    print("Example 1: Get Job Logs")
    print("=" * 60)

    with JobletClient() as client:
        # First, run a job that generates some logs
        print("\n1. Running a sample job to generate logs...")
        job = client.jobs.run_job(
            command="bash",
            args=["-c", "for i in {1..10}; do echo 'Log line '$i; sleep 0.1; done"],
            name="log-example-job",
        )
        job_id = job["job_uuid"]
        print(f"   Job started: {job_id}")

        # Wait for job to complete
        print("\n2. Waiting for job to complete...")
        import time

        while True:
            status = client.jobs.get_job_status(job_id)
            if status["status"] in ["COMPLETED", "FAILED"]:
                print(f"   Job finished with status: {status['status']}")
                break
            time.sleep(0.5)

        # Get all logs (server streams everything)
        print("\n3. Getting all logs...")
        print("-" * 60)

        # Collect logs to show we got them all
        all_logs = b""
        for chunk in client.jobs.get_job_logs(job_id):
            all_logs += chunk

        # Decode and display
        log_text = all_logs.decode("utf-8")
        log_lines = [line for line in log_text.strip().split("\n") if line]

        print(f"   Total log lines: {len(log_lines)}")
        print("\n   Sample logs:")
        for line in log_lines[:5]:
            print(f"      {line}")

        if len(log_lines) > 5:
            print(f"      ... and {len(log_lines) - 5} more lines")


def example_get_job_metrics():
    """Get all metrics for a completed job"""
    print("\n" + "=" * 60)
    print("Example 2: Get Job Metrics")
    print("=" * 60)

    with JobletClient() as client:
        # Run a CPU-intensive job that generates metrics
        print("\n1. Running a job to generate metrics...")
        job = client.jobs.run_job(
            command="bash",
            args=["-c", "for i in {1..15}; do echo 'Working...' $i; sleep 1; done"],
            name="metrics-example-job",
            max_cpu=50,  # Limit CPU to 50%
        )
        job_id = job["job_uuid"]
        print(f"   Job started: {job_id}")

        # Wait for job to complete
        print("\n2. Waiting for job to complete (this takes ~15 seconds)...")
        import time

        while True:
            status = client.jobs.get_job_status(job_id)
            if status["status"] in ["COMPLETED", "FAILED"]:
                print(f"   Job finished with status: {status['status']}")
                break
            time.sleep(2)

        # Get all metrics (server streams everything)
        print("\n3. Getting all metrics...")
        print("-" * 60)

        # Collect all metrics
        all_metrics = list(client.jobs.get_job_metrics(job_id))

        print(f"   Total metric samples: {len(all_metrics)}")

        # Show first few samples
        print("\n   Sample metrics:")
        for metric in all_metrics[:5]:
            timestamp = datetime.fromtimestamp(metric["timestamp"] / 1e9)
            cpu = metric.get("cpu_percent", 0)
            memory = metric.get("memory_bytes", 0) / (1024 * 1024)  # Convert to MB

            print(
                f"   [{timestamp.strftime('%H:%M:%S')}] "
                f"CPU: {cpu:6.2f}%, Memory: {memory:8.2f} MB"
            )

        if len(all_metrics) > 5:
            print(f"\n   ... and {len(all_metrics) - 5} more samples")

        # Calculate statistics (client-side)
        if all_metrics:
            cpu_values = [m.get("cpu_percent", 0) for m in all_metrics]
            memory_values = [
                m.get("memory_bytes", 0) / (1024 * 1024) for m in all_metrics
            ]

            print("\n4. Statistics (calculated client-side):")
            print("-" * 60)
            if cpu_values:
                print("   CPU Usage:")
                print(f"      Average: {sum(cpu_values) / len(cpu_values):.2f}%")
                print(f"      Peak: {max(cpu_values):.2f}%")
                print(f"      Min: {min(cpu_values):.2f}%")

            if memory_values:
                print("\n   Memory Usage:")
                print(
                    f"      Average: {sum(memory_values) / len(memory_values):.2f} MB"
                )
                print(f"      Peak: {max(memory_values):.2f} MB")
                print(f"      Min: {min(memory_values):.2f} MB")


def example_client_side_filtering():
    """Demonstrate client-side filtering of logs and metrics"""
    print("\n" + "=" * 60)
    print("Example 3: Client-Side Filtering")
    print("=" * 60)

    with JobletClient() as client:
        # Run a job
        print("\n1. Running a sample job...")
        job = client.jobs.run_job(
            command="bash",
            args=[
                "-c",
                "for i in {1..20}; do echo 'Timestamp: '$(date); sleep 0.5; done",
            ],
            name="filter-example-job",
            max_cpu=75,
        )
        job_id = job["job_uuid"]
        print(f"   Job started: {job_id}")

        # Wait for completion
        print("\n2. Waiting for job to complete...")
        import time

        while True:
            status = client.jobs.get_job_status(job_id)
            if status["status"] in ["COMPLETED", "FAILED"]:
                break
            time.sleep(1)

        # Get all metrics and filter client-side
        print("\n3. Getting metrics and filtering client-side...")
        print("-" * 60)

        all_metrics = list(client.jobs.get_job_metrics(job_id))
        print(f"   Total samples: {len(all_metrics)}")

        # Example: Get only the last 5 samples (client-side filtering)
        last_5 = all_metrics[-5:] if len(all_metrics) >= 5 else all_metrics

        print("\n   Last 5 samples (client-side filter):")
        for metric in last_5:
            timestamp = datetime.fromtimestamp(metric["timestamp"] / 1e9)
            cpu = metric.get("cpu_percent", 0)
            print(f"      [{timestamp.strftime('%H:%M:%S')}] CPU: {cpu:6.2f}%")

        # Example: Filter by time range (client-side)
        if all_metrics:
            # Get metrics from the last 5 seconds
            now_ns = all_metrics[-1]["timestamp"]
            five_sec_ago_ns = now_ns - (5 * int(1e9))

            recent_metrics = [
                m for m in all_metrics if m["timestamp"] >= five_sec_ago_ns
            ]

            print("\n   Metrics from last 5 seconds (client-side filter):")
            print(f"      Found {len(recent_metrics)} samples in last 5 seconds")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Joblet SDK - Job Logs and Metrics Examples (Proto v2.3.0)")
    print("=" * 60)

    try:
        # Example 1: Get job logs
        example_get_job_logs()

        # Example 2: Get job metrics
        # Uncomment to run (takes ~15 seconds)
        # example_get_job_metrics()

        # Example 3: Client-side filtering
        # Uncomment to run
        # example_client_side_filtering()

        print("\n" + "=" * 60)
        print("Examples completed successfully!")
        print("\n" + "Note: Proto v2.3.0 simplified the API:")
        print("  - Server streams ALL logs/metrics for a job")
        print("  - Clients filter results as needed (shown in Example 3)")
        print("  - No more server-side pagination or time-range filtering")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
