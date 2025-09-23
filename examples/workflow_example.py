#!/usr/bin/env python3
"""Workflow execution example with mTLS authentication"""

from joblet import JobletClient
import os
import time
import yaml


def main():
    # Get certificate paths from environment variables
    ca_cert_path = os.getenv('JOBLET_CA_CERT_PATH', 'certs/ca-cert.pem')
    client_cert_path = os.getenv('JOBLET_CLIENT_CERT_PATH', 'certs/client-cert.pem')
    client_key_path = os.getenv('JOBLET_CLIENT_KEY_PATH', 'certs/client-key.pem')

    # Connect to Joblet server with mTLS
    with JobletClient(
        host=os.getenv('JOBLET_HOST', 'localhost'),
        port=int(os.getenv('JOBLET_PORT', '50051')),
        ca_cert_path=ca_cert_path,
        client_cert_path=client_cert_path,
        client_key_path=client_key_path
    ) as client:

        if not client.health_check():
            print("Joblet server is not available")
            return

        print("Connected to Joblet server")

        # Define a simple workflow
        workflow_yaml = """
version: "1.0"
name: "data-processing-workflow"

jobs:
  - name: "download-data"
    command: "curl"
    args: ["-o", "data.txt", "https://httpbin.org/uuid"]
    runtime: "alpine"

  - name: "process-data"
    command: "wc"
    args: ["-l", "data.txt"]
    runtime: "alpine"
    depends_on: ["download-data"]

  - name: "cleanup"
    command: "rm"
    args: ["data.txt"]
    runtime: "alpine"
    depends_on: ["process-data"]
"""

        print("\n--- Running workflow ---")
        print("Workflow definition:")
        print(workflow_yaml)

        # Run the workflow
        workflow_response = client.jobs.run_workflow(
            workflow="data-processing-workflow.yml",
            yaml_content=workflow_yaml
        )

        workflow_uuid = workflow_response["workflow_uuid"]
        print(f"\nWorkflow started with UUID: {workflow_uuid}")
        print(f"Status: {workflow_response['status']}")

        # Monitor workflow progress
        print("\n--- Monitoring workflow ---")
        while True:
            status = client.jobs.get_workflow_status(workflow_uuid)
            workflow_info = status["workflow"]

            print(f"Workflow Status: {workflow_info['status']}")
            print(f"Total Jobs: {workflow_info['total_jobs']}")
            print(f"Completed: {workflow_info['completed_jobs']}")
            print(f"Failed: {workflow_info['failed_jobs']}")

            # Show job details
            print("\nJob Details:")
            for job in status["jobs"]:
                print(f"  - {job['job_name']}: {job['status']}")

            if workflow_info["status"] in ["completed", "failed", "cancelled"]:
                break

            print("-" * 40)
            time.sleep(3)

        # List all workflows
        print("\n--- All workflows ---")
        workflows = client.jobs.list_workflows(include_completed=True)
        for workflow in workflows:
            print(f"- {workflow['uuid']}: {workflow['workflow']} ({workflow['status']})")


if __name__ == "__main__":
    main()