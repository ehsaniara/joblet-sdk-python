#!/usr/bin/env python3
"""
Example 04: Querying Historical Logs and Metrics with PersistService

This example demonstrates how to use the PersistService to query historical
job logs and metrics from persistent storage. This is useful for analyzing
completed jobs or debugging past executions.

The PersistService connects to joblet-persist on port 50052, which provides
efficient querying of stored logs and metrics with filtering and pagination.
"""

from datetime import datetime

from joblet import JobletClient


def example_query_historical_logs():
    """Query historical logs for a completed job"""
    print("=" * 60)
    print("Example 1: Query Historical Logs")
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

        # Query historical logs using persist service
        print("\n3. Querying historical logs from persist service...")
        print("-" * 60)

        log_count = 0
        for log in client.persist.query_logs(job_id=job_id):
            log_count += 1
            timestamp = datetime.fromtimestamp(log["timestamp"] / 1e9)
            content = log["content"].decode("utf-8").strip()
            stream = log["stream"].upper()
            print(f"   [{timestamp.strftime('%H:%M:%S.%f')[:-3]}] [{stream}] {content}")

        print(f"\n   Total logs retrieved: {log_count}")

        # Query only stdout logs
        print("\n4. Querying only STDOUT logs...")
        print("-" * 60)

        stdout_count = 0
        for log in client.persist.query_logs(job_id=job_id, stream="stdout"):
            stdout_count += 1
            content = log["content"].decode("utf-8").strip()
            print(f"   STDOUT: {content}")

        print(f"\n   Total STDOUT logs: {stdout_count}")

        # Query with pagination (first 5 lines)
        print("\n5. Querying with pagination (limit=5)...")
        print("-" * 60)

        for log in client.persist.query_logs(job_id=job_id, limit=5):
            content = log["content"].decode("utf-8").strip()
            print(f"   {content}")


def example_query_historical_metrics():
    """Query historical metrics for a completed job"""
    print("\n" + "=" * 60)
    print("Example 2: Query Historical Metrics")
    print("=" * 60)

    with JobletClient() as client:
        # Run a CPU-intensive job that generates metrics
        print("\n1. Running a CPU-intensive job to generate metrics...")
        job = client.jobs.run_job(
            command="bash",
            args=["-c", "for i in {1..30}; do echo 'Working...' $i; sleep 1; done"],
            name="metrics-example-job",
            max_cpu=50,  # Limit CPU to 50%
        )
        job_id = job["job_uuid"]
        print(f"   Job started: {job_id}")

        # Wait for job to complete
        print("\n2. Waiting for job to complete (this takes ~30 seconds)...")
        import time

        while True:
            status = client.jobs.get_job_status(job_id)
            if status["status"] in ["COMPLETED", "FAILED"]:
                print(f"   Job finished with status: {status['status']}")
                break
            time.sleep(2)

        # Query historical metrics using persist service
        print("\n3. Querying historical metrics from persist service...")
        print("-" * 60)

        metrics_count = 0
        for metric in client.persist.query_metrics(job_id=job_id):
            metrics_count += 1
            timestamp = datetime.fromtimestamp(metric["timestamp"] / 1e9)
            data = metric["data"]

            # Format metrics
            cpu = data.get("cpu_usage", 0)
            memory = data.get("memory_usage", 0) / (1024 * 1024)  # Convert to MB
            gpu = data.get("gpu_usage", 0)

            print(
                f"   [{timestamp.strftime('%H:%M:%S')}] "
                f"CPU: {cpu:6.2f}%, Memory: {memory:8.2f} MB, GPU: {gpu:6.2f}%"
            )

            # Show disk I/O if available
            if "disk_io" in data:
                disk = data["disk_io"]
                read_mb = disk["read_bytes"] / (1024 * 1024)
                write_mb = disk["write_bytes"] / (1024 * 1024)
                print(
                    f"              Disk I/O - Read: {read_mb:.2f} MB, "
                    f"Write: {write_mb:.2f} MB"
                )

            # Show network I/O if available
            if "network_io" in data:
                net = data["network_io"]
                rx_mb = net["rx_bytes"] / (1024 * 1024)
                tx_mb = net["tx_bytes"] / (1024 * 1024)
                print(
                    f"              Network - RX: {rx_mb:.2f} MB, "
                    f"TX: {tx_mb:.2f} MB"
                )

        print(f"\n   Total metrics samples: {metrics_count}")

        # Query recent metrics (last 10 samples)
        print("\n4. Querying recent metrics (limit=10)...")
        print("-" * 60)

        for metric in client.persist.query_metrics(job_id=job_id, limit=10):
            timestamp = datetime.fromtimestamp(metric["timestamp"] / 1e9)
            cpu = metric["data"].get("cpu_usage", 0)
            memory = metric["data"].get("memory_usage", 0) / (1024 * 1024)
            print(
                f"   [{timestamp.strftime('%H:%M:%S')}] "
                f"CPU: {cpu:6.2f}%, Memory: {memory:8.2f} MB"
            )


def example_time_range_query():
    """Query logs and metrics within a specific time range"""
    print("\n" + "=" * 60)
    print("Example 3: Time Range Queries")
    print("=" * 60)

    with JobletClient() as client:
        # Run a long job
        print("\n1. Running a long-running job...")
        job = client.jobs.run_job(
            command="bash",
            args=[
                "-c",
                "for i in {1..20}; do echo 'Timestamp: '$(date); sleep 1; done",
            ],
            name="timerange-example-job",
        )
        job_id = job["job_uuid"]
        print(f"   Job started: {job_id}")

        import time

        time.sleep(5)  # Let it run for a bit

        # Get current time in nanoseconds
        now_ns = int(time.time() * 1e9)
        five_seconds_ago_ns = now_ns - (5 * int(1e9))

        # Query logs from the last 5 seconds
        print("\n2. Querying logs from the last 5 seconds...")
        print("-" * 60)

        recent_logs = 0
        for log in client.persist.query_logs(
            job_id=job_id, start_time=five_seconds_ago_ns, end_time=now_ns
        ):
            recent_logs += 1
            content = log["content"].decode("utf-8").strip()
            timestamp = datetime.fromtimestamp(log["timestamp"] / 1e9)
            print(f"   [{timestamp.strftime('%H:%M:%S')}] {content}")

        print(f"\n   Logs in last 5 seconds: {recent_logs}")

        # Stop the job
        print("\n3. Stopping the job...")
        client.jobs.stop_job(job_id)


def example_comprehensive_job_analysis():
    """Comprehensive analysis of a completed job using persist service"""
    print("\n" + "=" * 60)
    print("Example 4: Comprehensive Job Analysis")
    print("=" * 60)

    with JobletClient() as client:
        # Run a job that we'll analyze
        print("\n1. Running a sample job...")
        job = client.jobs.run_job(
            command="python3",
            args=[
                "-c",
                """
import time
import sys

for i in range(10):
    print(f'Processing batch {i+1}/10...', flush=True)
    # Do some work
    sum([j**2 for j in range(100000)])
    time.sleep(0.5)

print('Job completed successfully!', flush=True)
""",
            ],
            name="analysis-example-job",
            max_cpu=75,
            max_memory=256,  # 256 MB
        )
        job_id = job["job_uuid"]
        print(f"   Job ID: {job_id}")

        # Wait for completion
        print("\n2. Waiting for job to complete...")
        import time

        while True:
            status = client.jobs.get_job_status(job_id)
            if status["status"] in ["COMPLETED", "FAILED"]:
                break
            time.sleep(0.5)

        # Comprehensive analysis
        print("\n3. Analyzing job execution...")
        print("-" * 60)

        # Get job details
        job_info = client.jobs.get_job_status(job_id)
        print(f"\n   Job Status: {job_info['status']}")
        print(f"   Exit Code: {job_info['exit_code']}")
        print(f"   Start Time: {job_info['start_time']}")
        print(f"   End Time: {job_info['end_time']}")

        # Analyze logs
        print("\n4. Log Analysis:")
        print("-" * 60)
        log_lines = list(client.persist.query_logs(job_id=job_id))
        print(f"   Total log lines: {len(log_lines)}")

        if log_lines:
            first_log_time = datetime.fromtimestamp(log_lines[0]["timestamp"] / 1e9)
            last_log_time = datetime.fromtimestamp(log_lines[-1]["timestamp"] / 1e9)
            duration = (log_lines[-1]["timestamp"] - log_lines[0]["timestamp"]) / 1e9
            print(f"   First log: {first_log_time.strftime('%H:%M:%S.%f')[:-3]}")
            print(f"   Last log: {last_log_time.strftime('%H:%M:%S.%f')[:-3]}")
            print(f"   Log duration: {duration:.2f} seconds")

            print("\n   Sample logs:")
            for log in log_lines[:3]:
                content = log["content"].decode("utf-8").strip()
                print(f"      {content}")

        # Analyze metrics
        print("\n5. Metrics Analysis:")
        print("-" * 60)
        metrics = list(client.persist.query_metrics(job_id=job_id))
        print(f"   Total metric samples: {len(metrics)}")

        if metrics:
            # Calculate stats
            cpu_values = [m["data"].get("cpu_usage", 0) for m in metrics]
            memory_values = [
                m["data"].get("memory_usage", 0) / (1024 * 1024) for m in metrics
            ]

            if cpu_values:
                print("\n   CPU Usage:")
                print(f"      Average: {sum(cpu_values) / len(cpu_values):.2f}%")
                print(f"      Peak: {max(cpu_values):.2f}%")
                print(f"      Min: {min(cpu_values):.2f}%")

            if memory_values:
                print("\n   Memory Usage:")
                print(
                    f"      Average: "
                    f"{sum(memory_values) / len(memory_values):.2f} MB"
                )
                print(f"      Peak: {max(memory_values):.2f} MB")
                print(f"      Min: {min(memory_values):.2f} MB")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Joblet SDK - Historical Logs and Metrics Examples")
    print("=" * 60)

    try:
        # Example 1: Basic log queries
        example_query_historical_logs()

        # Example 2: Basic metrics queries
        # Uncomment to run (takes ~30 seconds)
        # example_query_historical_metrics()

        # Example 3: Time range queries
        # Uncomment to run
        # example_time_range_query()

        # Example 4: Comprehensive analysis
        # Uncomment to run
        # example_comprehensive_job_analysis()

        print("\n" + "=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
