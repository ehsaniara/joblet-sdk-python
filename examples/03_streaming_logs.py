#!/usr/bin/env python3
"""
Streaming Logs Example

This script demonstrates real-time log streaming from running jobs.
"""

import threading
import time

from joblet import JobletClient


def stream_logs(client, job_uuid):
    """Stream logs from a job in real-time"""
    print(f"[LOG STREAM] Starting for job {job_uuid}")

    try:
        for chunk in client.get_job_logs(job_uuid, stream=True):
            if chunk:
                print(f"[OUTPUT] {chunk.decode()}", end="")
    except Exception as e:
        print(f"[LOG STREAM] Ended: {e}")


def main():
    client = JobletClient(host="localhost", port=8080)

    print("=== Real-time Log Streaming Example ===\n")

    # Start a job that produces output over time
    job = client.run_job(
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

    print(f"✓ Started job: {job.uuid}\n")

    # Start streaming logs in a separate thread
    log_thread = threading.Thread(target=stream_logs, args=(client, job.uuid))
    log_thread.daemon = True
    log_thread.start()

    # Monitor job status in main thread
    print("Monitoring job status...")
    while True:
        status = client.get_job_status(job.uuid)
        if status.status in ["completed", "failed", "canceled"]:
            print(f"\n✓ Job finished with status: {status.status}")
            break
        time.sleep(1)

    # Wait for log streaming to finish
    log_thread.join(timeout=2)

    # Clean up
    client.delete_job(job.uuid)
    print("✓ Cleanup complete")


if __name__ == "__main__":
    main()
