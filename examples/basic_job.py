#!/usr/bin/env python3
"""Simple example of running a job."""

import time

from joblet import JobletClient


def main():
    # Uses config from ~/.rnx/rnx-config.yml by default
    # The server requires TLS certificates (self-signed with OpenSSL)
    with JobletClient(insecure=False) as client:
        print(f"Connecting to {client.host}:{client.port}")
        if not client.health_check():
            print("Server not available")
            return

        # Run a job
        job = client.jobs.run_job(
            command="echo", args=["Hello, World!"], name="test-job"
        )

        print(f"Job started: {job['job_uuid']}")

        # Wait for completion
        while True:
            status = client.jobs.get_job_status(job["job_uuid"])
            print(f"Status: {status['status']}")

            if status["status"].lower() in ["completed", "failed"]:
                break
            time.sleep(1)

        # Show logs
        logs = b"".join(client.jobs.get_job_logs(job["job_uuid"]))
        print(f"Output: \n")
        print(f"{logs.decode()}")


if __name__ == "__main__":
    main()
