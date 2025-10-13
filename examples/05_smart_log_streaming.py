#!/usr/bin/env python3
"""
Example 05: Smart Log Streaming (Historical + Live)

This example demonstrates the intelligent log streaming feature that
automatically handles both historical and live logs - just like 'rnx job log'.

The get_job_logs() method:
1. First fetches any historical logs from persist service (if available)
2. Then streams live logs from the job service

This provides seamless log access for both completed and running jobs
without needing to know the job's status or choose the right service.
"""

import time

from joblet import JobletClient


def example_completed_job_logs():
    """Example 1: Get logs from a completed job"""
    print("=" * 70)
    print("Example 1: Smart Log Access for Completed Job")
    print("=" * 70)

    with JobletClient() as client:
        # Run a job and let it complete
        print("\n1. Running a sample job...")
        job = client.jobs.run_job(
            command="bash",
            args=[
                "-c",
                """
                echo "Starting job..."
                echo "Processing line 1"
                sleep 1
                echo "Processing line 2"
                sleep 1
                echo "Processing line 3"
                sleep 1
                echo "Job completed successfully!"
            """,
            ],
            name="completed-job-example",
        )
        job_id = job["job_uuid"]
        print(f"   Job ID: {job_id}")

        # Wait for job to complete
        print("\n2. Waiting for job to complete...")
        while True:
            status = client.jobs.get_job_status(job_id)
            if status["status"] in ["COMPLETED", "FAILED"]:
                print(f"   Job finished with status: {status['status']}")
                break
            time.sleep(0.5)

        # Get logs using smart routing
        print("\n3. Fetching logs (automatically from historical storage)...")
        print("-" * 70)

        for chunk in client.jobs.get_job_logs(job_id):
            print(chunk.decode("utf-8"), end="")

        print("\n" + "-" * 70)
        print("✓ All logs retrieved successfully (from persist service)")


def example_running_job_logs():
    """Example 2: Stream logs from a running job in real-time"""
    print("\n" + "=" * 70)
    print("Example 2: Smart Log Streaming for Running Job")
    print("=" * 70)

    with JobletClient() as client:
        # Run a longer job
        print("\n1. Starting a long-running job...")
        job = client.jobs.run_job(
            command="bash",
            args=[
                "-c",
                """
                echo "Job started at $(date)"
                for i in {1..10}; do
                    echo "Progress: $i/10 - $(date)"
                    sleep 1
                done
                echo "Job completed at $(date)"
            """,
            ],
            name="running-job-example",
        )
        job_id = job["job_uuid"]
        print(f"   Job ID: {job_id}")

        # Wait a moment for job to start
        time.sleep(0.5)

        # Stream logs in real-time
        print("\n2. Streaming live logs...")
        print("-" * 70)

        try:
            for chunk in client.jobs.get_job_logs(job_id):
                print(chunk.decode("utf-8"), end="", flush=True)
        except KeyboardInterrupt:
            print("\n\n✓ Stopped streaming (Ctrl+C pressed)")
            return

        print("\n" + "-" * 70)
        print("✓ Live streaming completed")


def example_reconnect_to_running_job():
    """Example 3: Reconnect to running job and get all logs"""
    print("\n" + "=" * 70)
    print("Example 3: Reconnect to Running Job (Historical + Live)")
    print("=" * 70)

    with JobletClient() as client:
        # Start a long-running job
        print("\n1. Starting a long-running job...")
        job = client.jobs.run_job(
            command="bash",
            args=[
                "-c",
                """
                for i in {1..20}; do
                    echo "Iteration $i at $(date +%H:%M:%S)"
                    sleep 1
                done
            """,
            ],
            name="reconnect-example",
        )
        job_id = job["job_uuid"]
        print(f"   Job ID: {job_id}")

        # Let it run for a bit
        print("\n2. Letting job run for 5 seconds...")
        time.sleep(5)

        # Now "reconnect" and get ALL logs (historical + continuing live)
        print("\n3. Reconnecting to get all logs (historical + live)...")
        print("-" * 70)
        print("   ↓ Historical logs from persist service")
        print("   ↓ Then live logs from job service")
        print("-" * 70)

        log_count = 0
        for chunk in client.jobs.get_job_logs(job_id):
            log_count += 1
            print(chunk.decode("utf-8"), end="", flush=True)

        print("\n" + "-" * 70)
        print("✓ Retrieved all logs seamlessly (historical + live)")


def example_live_only_streaming():
    """Example 4: Stream only new logs (skip historical)"""
    print("\n" + "=" * 70)
    print("Example 4: Live-Only Log Streaming")
    print("=" * 70)

    with JobletClient() as client:
        # Start a job
        print("\n1. Starting a job...")
        job = client.jobs.run_job(
            command="bash",
            args=[
                "-c",
                """
                echo "Line 1"
                echo "Line 2"
                echo "Line 3"
                sleep 2
                echo "Line 4 (after delay)"
                echo "Line 5 (after delay)"
            """,
            ],
            name="live-only-example",
        )
        job_id = job["job_uuid"]
        print(f"   Job ID: {job_id}")

        # Wait a moment
        print("\n2. Waiting 3 seconds before connecting...")
        time.sleep(3)

        # Stream only NEW logs (skip what already happened)
        print("\n3. Streaming only new logs (skip historical)...")
        print("-" * 70)

        for chunk in client.jobs.stream_live_logs(job_id):
            print(chunk.decode("utf-8"), end="", flush=True)

        print("\n" + "-" * 70)
        print("✓ Streamed only new logs (missed lines 1-3)")


def example_with_error_handling():
    """Example 5: Error handling when persist service unavailable"""
    print("\n" + "=" * 70)
    print("Example 5: Graceful Fallback When Persist Unavailable")
    print("=" * 70)

    with JobletClient() as client:
        print("\nNote: If joblet-persist is not running, the SDK will:")
        print("  1. Try to fetch historical logs (may fail)")
        print("  2. Gracefully fall back to live streaming")
        print("  3. Continue working without errors")

        print("\n1. Starting a job...")
        job = client.jobs.run_job(
            command="echo",
            args=["This works even without persist service!"],
            name="fallback-example",
        )
        job_id = job["job_uuid"]

        print("\n2. Fetching logs...")
        print("-" * 70)

        # This will work even if persist service is unavailable
        for chunk in client.jobs.get_job_logs(job_id):
            print(chunk.decode("utf-8"), end="")

        print("-" * 70)
        print("✓ Logs retrieved successfully (with graceful fallback)")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("Joblet SDK - Smart Log Streaming Examples")
    print("Replicates 'rnx job log' behavior")
    print("=" * 70)

    try:
        # Example 1: Completed job (uses historical logs)
        example_completed_job_logs()

        # Example 2: Running job (uses live streaming)
        # Uncomment to run
        # example_running_job_logs()

        # Example 3: Reconnect to running job (uses both)
        # Uncomment to run
        # example_reconnect_to_running_job()

        # Example 4: Live-only streaming
        # Uncomment to run
        # example_live_only_streaming()

        # Example 5: Error handling
        example_with_error_handling()

        print("\n" + "=" * 70)
        print("Examples completed successfully!")
        print("\nKey takeaway: client.jobs.get_job_logs() works for ANY job")
        print("  - Completed jobs: fetches from historical storage")
        print("  - Running jobs: streams live")
        print("  - Reconnecting: shows history + continues live")
        print("=" * 70)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
