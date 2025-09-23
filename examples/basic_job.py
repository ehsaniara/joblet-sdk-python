#!/usr/bin/env python3
"""Basic job execution example with mTLS authentication"""

import os
import time

from joblet import JobletClient


def main():
    # Get certificate paths from environment variables
    ca_cert_path = os.getenv("JOBLET_CA_CERT_PATH", "certs/ca-cert.pem")
    client_cert_path = os.getenv("JOBLET_CLIENT_CERT_PATH", "certs/client-cert.pem")
    client_key_path = os.getenv("JOBLET_CLIENT_KEY_PATH", "certs/client-key.pem")

    # Connect to Joblet server with mTLS
    with JobletClient(
        host=os.getenv("JOBLET_HOST", "localhost"),
        port=int(os.getenv("JOBLET_PORT", "50051")),
        ca_cert_path=ca_cert_path,
        client_cert_path=client_cert_path,
        client_key_path=client_key_path,
    ) as client:

        # Check server health
        if not client.health_check():
            print("Joblet server is not available")
            return

        print("Connected to Joblet server")

        # Run a simple job
        print("\n--- Running a simple job ---")
        job_response = client.jobs.run_job(
            command="echo",
            args=["Hello, World!"],
            name="hello-world-job",
            max_memory=100,  # 100MB
            runtime="python-3.11",
        )

        job_uuid = job_response["job_uuid"]
        print(f"Job started with UUID: {job_uuid}")
        print(f"Status: {job_response['status']}")

        # Monitor job status
        print("\n--- Monitoring job ---")
        while True:
            status = client.jobs.get_job_status(job_uuid)
            print(f"Status: {status['status']}")

            if status["status"] in ["completed", "failed", "cancelled"]:
                print(f"Exit code: {status['exit_code']}")
                break

            time.sleep(1)

        # Get job logs
        print("\n--- Job logs ---")
        try:
            logs = b""
            for chunk in client.jobs.get_job_logs(job_uuid):
                logs += chunk

            print(logs.decode("utf-8"))
        except Exception as e:
            print(f"Failed to get logs: {e}")

        # List all jobs
        print("\n--- All jobs ---")
        jobs = client.jobs.list_jobs()
        for job in jobs:
            print(f"- {job['uuid']}: {job['name']} ({job['status']})")


if __name__ == "__main__":
    main()
