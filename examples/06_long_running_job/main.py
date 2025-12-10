#!/usr/bin/env python3
"""
Long-Running Job with Live and Historical Logs Demo

This example demonstrates:
1. Running a long-running job (equivalent to:
   rnx job run bash -c 'for i in {1..600}; do echo "Counter: $i"; sleep 0.1; done')
2. Streaming logs in real-time while the job is running
3. Waiting for job completion
4. Retrieving all logs after the job finishes (historical + any missed logs)

This showcases the SDK's ability to:
- Stream live logs as they're produced
- Seamlessly retrieve complete logs after job completion
- Handle both live and historical log access
"""

import time

from joblet import JobletClient


def main():
    print("=== Long-Running Job with Live and Historical Logs Demo ===\n")

    # SDK automatically uses mTLS and loads certificates from ~/.rnx/rnx-config.yml
    with JobletClient() as client:
        # 1. Submit a long-running job (60 seconds, 600 lines)
        print("Step 1: Submitting long-running job...")
        cmd = 'for i in {1..600}; do echo "Counter: $i"; sleep 0.1; done'
        print(f"Command: bash -c '{cmd}'")
        print()

        job = client.jobs.run_job(
            name="long-counter",
            command="bash",
            args=["-c", 'for i in {1..600}; do echo "Counter: $i"; sleep 0.1; done'],
        )

        job_id = job["job_uuid"]
        print(f"✓ Job submitted: {job_id}")
        print("✓ Job will run for ~60 seconds (600 lines, 0.1s each)\n")

        # 2. Stream logs in real-time while job is running
        print("Step 2: Streaming live logs (showing first 10 seconds)...")
        print("-" * 60)

        start_time = time.time()
        line_count = 0

        # Stream logs for 10 seconds to see live output
        for chunk in client.jobs.stream_live_logs(job_id):
            print(chunk.decode(), end="", flush=True)
            line_count += 1

            # Stop after 10 seconds to demonstrate
            if time.time() - start_time > 10:
                print("\n" + "-" * 60)
                print(f"✓ Streamed {line_count} lines in 10 seconds")
                print("✓ Stopping live stream (job continues running in background)\n")
                break

        # 3. Check job status while it's still running
        print("Step 3: Checking job status while running...")
        status = client.jobs.get_job_status(job_id)
        print(f"✓ Current status: {status['status']}")
        print()

        # 4. Wait for job to complete
        print("Step 4: Waiting for job to complete...")
        print("(Job will continue for ~50 more seconds)\n")

        while True:
            status = client.jobs.get_job_status(job_id)
            if status["status"] not in ["PENDING", "RUNNING"]:
                break
            time.sleep(2)

        print(f"✓ Job completed with status: {status['status']}")
        print(f"✓ Exit code: {status.get('exit_code', 'N/A')}\n")

        # 5. Wait 5 seconds before retrieving all logs
        print("Step 5: Waiting 5 seconds before retrieving all logs...")
        time.sleep(5)
        print("✓ Wait complete\n")

        # 6. Retrieve ALL logs after job completion
        print("Step 6: Retrieving complete job logs (all 600 lines)...")
        print("-" * 60)

        all_lines = 0
        # get_job_logs() automatically fetches historical logs from persist service
        # and falls back to job service if persist is unavailable
        for chunk in client.jobs.get_job_logs(job_id):
            print(chunk.decode(), end="", flush=True)
            all_lines += 1

        print("-" * 60)
        print(f"\n✓ Retrieved {all_lines} total lines from completed job")
        print()

        # 7. Show the difference
        print("=== Summary ===")
        print(f"Live streaming (first 10s): ~{line_count} lines")
        print(f"Historical retrieval (all): {all_lines} lines")
        print(
            f"Difference: {all_lines - line_count} lines "
            "(captured while we weren't streaming)"
        )
        print()
        print("This demonstrates:")
        print("  ✓ Live logs: Stream in real-time while job runs")
        print("  ✓ Historical logs: Retrieve complete logs after completion")
        print("  ✓ No data loss: All output captured, even when not streaming")
        print()

        # Clean up
        print("Cleaning up...")
        client.jobs.delete_job(job_id)
        print("✓ Job deleted\n")


if __name__ == "__main__":
    main()
