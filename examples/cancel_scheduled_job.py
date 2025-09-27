#!/usr/bin/env python3
"""
Example: Canceling scheduled jobs

This example demonstrates the difference between stopping running jobs
and canceling scheduled jobs:
- stop_job() → for RUNNING jobs (status becomes STOPPED)
- cancel_job() → for SCHEDULED jobs (status becomes CANCELED)
"""

import time
from datetime import datetime, timedelta

from joblet import JobletClient, JobNotFoundError


def cancel_scheduled_job_example():
    """Example of scheduling and then canceling a job"""

    # Connect to your Joblet server
    with JobletClient(
        host="joblet.example.com",  # Replace with your server
        port=50051,
        ca_cert_path="/path/to/ca-cert.pem",
        client_cert_path="/path/to/client-cert.pem",
        client_key_path="/path/to/client-key.pem",
    ) as client:

        # Schedule a job to run 5 minutes from now
        schedule_time = datetime.now() + timedelta(minutes=5)
        schedule_str = schedule_time.strftime("%Y-%m-%dT%H:%M:%S")

        print(f"📅 Scheduling job for {schedule_str}")

        # Create a scheduled job
        job = client.jobs.run_job(
            command="python",
            args=["long_running_task.py"],
            name="scheduled-data-processing",
            max_memory=2048,
            runtime="python-3.11",
            schedule=schedule_str,  # This makes it a scheduled job
        )

        job_uuid = job["job_uuid"]
        print(f"✅ Job scheduled: {job_uuid}")

        # Check the job status
        status = client.jobs.get_job_status(job_uuid)
        print(f"📊 Status: {status['status']}")  # Should be SCHEDULED

        # User changed their mind - cancel the scheduled job
        print("\n🚫 Canceling the scheduled job...")

        try:
            # Use cancel_job for SCHEDULED jobs
            result = client.jobs.cancel_job(job_uuid)
            print(f"✅ Job canceled: {result['status']}")  # Status will be CANCELED

            # Job is preserved in history with CANCELED status
            final_status = client.jobs.get_job_status(job_uuid)
            print(f"📋 Final status: {final_status['status']}")
            print("📝 Job preserved in history for audit purposes")

        except JobNotFoundError as e:
            print(f"❌ Could not cancel job: {e}")


def stop_vs_cancel_example():
    """Demonstrate the difference between stop and cancel"""

    with JobletClient(
        host="joblet.example.com",
        port=50051,
        ca_cert_path="/path/to/ca-cert.pem",
        client_cert_path="/path/to/client-cert.pem",
        client_key_path="/path/to/client-key.pem",
    ) as client:

        print("🔍 Understanding stop vs cancel:\n")
        print("=" * 50)

        # Example 1: Stopping a running job
        print("1️⃣ RUNNING job → use stop_job()")
        print("   - Job is actively executing")
        print("   - stop_job() terminates the process")
        print("   - Status becomes STOPPED")

        running_job = client.jobs.run_job(
            command="sleep",
            args=["60"],  # Will run for 60 seconds
            name="running-job-example",
        )

        time.sleep(2)  # Let it start running

        status = client.jobs.get_job_status(running_job["job_uuid"])
        if status["status"] == "RUNNING":
            client.jobs.stop_job(running_job["job_uuid"])
            print(f"   ✅ Running job stopped")

        print("\n" + "=" * 50)

        # Example 2: Canceling a scheduled job
        print("2️⃣ SCHEDULED job → use cancel_job()")
        print("   - Job is waiting for scheduled time")
        print("   - cancel_job() prevents execution")
        print("   - Status becomes CANCELED")

        schedule_time = datetime.now() + timedelta(hours=1)
        scheduled_job = client.jobs.run_job(
            command="echo",
            args=["Future task"],
            name="scheduled-job-example",
            schedule=schedule_time.strftime("%Y-%m-%dT%H:%M:%S"),
        )

        status = client.jobs.get_job_status(scheduled_job["job_uuid"])
        if status["status"] == "SCHEDULED":
            client.jobs.cancel_job(scheduled_job["job_uuid"])
            print(f"   ✅ Scheduled job canceled")

        print("\n" + "=" * 50)
        print("\n📚 Summary:")
        print("  - stop_job(): For jobs that are currently RUNNING")
        print("  - cancel_job(): For jobs that are SCHEDULED but not yet started")
        print("  - Both preserve job history for audit purposes")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--compare":
        stop_vs_cancel_example()
    else:
        cancel_scheduled_job_example()
