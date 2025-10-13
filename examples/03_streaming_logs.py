#!/usr/bin/env python3
"""
Streaming Logs Example

This script demonstrates real-time log streaming from running jobs.
Shows both smart log streaming (historical + live) and live-only streaming.
"""

import threading
import time

from joblet import JobletClient


def stream_logs_live_only(client, job_uuid):
    """Stream live logs only (no historical logs)"""
    print(f"[LOG STREAM] Starting live-only stream for job {job_uuid[:8]}...")

    try:
        for chunk in client.jobs.stream_live_logs(job_uuid):
            if chunk:
                print(f"{chunk.decode()}", end="", flush=True)
    except Exception as e:
        print(f"\n[LOG STREAM] Ended: {e}")


def stream_logs_smart(client, job_uuid):
    """Smart log streaming - gets historical + live logs automatically"""
    print(f"[LOG STREAM] Starting smart stream for job {job_uuid[:8]}...")

    try:
        for chunk in client.jobs.get_job_logs(job_uuid):
            if chunk:
                print(f"{chunk.decode()}", end="", flush=True)
    except Exception as e:
        print(f"\n[LOG STREAM] Ended: {e}")


def example_1_live_streaming(client):
    """Example 1: Stream logs from a running job (live only)"""
    print("=== Example 1: Live-Only Log Streaming ===\n")

    # Start a job that produces output over time
    job = client.jobs.run_job(
        name="streaming-counter",
        command="bash",
        args=[
            "-c",
            """
            for i in {1..10}; do
                echo "Count: $i"
                echo "Time: $(date +%T)"
                sleep 1
            done
            echo "Done!"
        """,
        ],
    )

    print(f"✓ Started job: {job['job_uuid']}\n")

    # Start streaming logs in a separate thread (live only)
    log_thread = threading.Thread(
        target=stream_logs_live_only, args=(client, job["job_uuid"])
    )
    log_thread.daemon = True
    log_thread.start()

    # Monitor job status in main thread
    print("[MAIN] Monitoring job status...")
    while True:
        status = client.jobs.get_job_status(job["job_uuid"])
        if status["status"] in ["COMPLETED", "FAILED", "STOPPED"]:
            print(f"\n[MAIN] Job finished with status: {status['status']}")
            break
        time.sleep(1)

    # Wait for log streaming to finish
    log_thread.join(timeout=2)

    # Clean up
    client.jobs.delete_job(job["job_uuid"])
    print("\n✓ Example 1 complete\n")


def example_2_smart_streaming(client):
    """Example 2: Smart log streaming - gets historical + live logs"""
    print("=== Example 2: Smart Log Streaming (Historical + Live) ===\n")

    # Start a job
    job = client.jobs.run_job(
        name="smart-streaming",
        command="bash",
        args=[
            "-c",
            """
            echo "Starting job..."
            for i in {1..5}; do
                echo "Progress: $i/5"
                sleep 1
            done
            echo "Job complete!"
        """,
        ],
    )

    print(f"✓ Started job: {job['job_uuid']}")

    # Wait a bit to let some logs accumulate
    print("  Waiting 2 seconds to let logs accumulate...")
    time.sleep(2)

    # Now start streaming - will get historical logs + continue with live
    print("\n[SMART STREAM] Getting all logs (historical + live):\n")
    for chunk in client.jobs.get_job_logs(job["job_uuid"]):
        if chunk:
            print(f"  {chunk.decode()}", end="", flush=True)

    # Clean up
    client.jobs.delete_job(job["job_uuid"])
    print("\n\n✓ Example 2 complete\n")


def example_3_completed_job_logs(client):
    """Example 3: Get logs from a completed job (all historical)"""
    print("=== Example 3: Completed Job Logs ===\n")

    # Run a quick job
    job = client.jobs.run_job(
        name="completed-job",
        command="bash",
        args=["-c", "echo 'Line 1'; echo 'Line 2'; echo 'Line 3'"],
    )

    print(f"✓ Started job: {job['job_uuid']}")

    # Wait for completion
    status = client.jobs.get_job_status(job["job_uuid"])
    while status["status"] in ["PENDING", "RUNNING"]:
        time.sleep(0.5)
        status = client.jobs.get_job_status(job["job_uuid"])

    print(f"✓ Job completed with status: {status['status']}")

    # Now get all logs (will fetch from historical storage)
    print("\n[HISTORICAL] All logs from completed job:\n")
    for chunk in client.jobs.get_job_logs(job["job_uuid"]):
        if chunk:
            print(f"  {chunk.decode()}", end="")

    # Clean up
    client.jobs.delete_job(job["job_uuid"])
    print("\n\n✓ Example 3 complete\n")


def example_4_reconnect_scenario(client):
    """Example 4: Simulate reconnecting to a running job"""
    print("=== Example 4: Reconnect to Running Job ===\n")

    # Start a long-running job
    job = client.jobs.run_job(
        name="long-runner",
        command="bash",
        args=[
            "-c",
            """
            for i in {1..15}; do
                echo "Iteration: $i"
                sleep 1
            done
        """,
        ],
    )

    print(f"✓ Started job: {job['job_uuid']}")
    print("  Letting it run for 5 seconds...")
    time.sleep(5)

    # Now "reconnect" and stream logs (will get historical + live)
    print("\n[RECONNECT] Getting all logs from running job:\n")

    count = 0
    for chunk in client.jobs.get_job_logs(job["job_uuid"]):
        if chunk:
            print(f"  {chunk.decode()}", end="", flush=True)
            count += 1
            # Disconnect after 5 more chunks
            if count > 5:
                print("\n[DISCONNECT] Stopping log stream...")
                break

    # Stop the job
    client.jobs.stop_job(job["job_uuid"])

    # Clean up
    client.jobs.delete_job(job["job_uuid"])
    print("\n✓ Example 4 complete\n")


def main():
    with JobletClient() as client:
        try:
            # Run all examples
            example_1_live_streaming(client)
            example_2_smart_streaming(client)
            example_3_completed_job_logs(client)
            example_4_reconnect_scenario(client)

            print("=" * 50)
            print("✓ All streaming examples completed!")
            print("=" * 50)

        except Exception as e:
            print(f"Error: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
