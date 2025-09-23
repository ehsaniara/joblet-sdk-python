#!/usr/bin/env python3
"""Example of streaming job output in real-time."""

from joblet import JobletClient


def main():
    # Uses config from ~/.rnx/rnx-config.yml by default
    # The server requires TLS certificates (self-signed with OpenSSL)
    with JobletClient(insecure=False) as client:
        print(f"Connecting to {client.host}:{client.port}")
        if not client.health_check():
            print("Server not available")
            return

        print("Server is available!")

        # Create a bash script that prints counter every 100ms for 60 seconds
        # 60 seconds / 0.1 second = 600 iterations
        bash_script = """
        for i in $(seq 1 600); do
            echo "Counter: $i - Time: $(date +%H:%M:%S.%3N)"
            sleep 0.1
        done
        echo "Completed 60 seconds of counting!"
        """

        # Run the job
        job = client.jobs.run_job(
            command="bash", args=["-c", bash_script], name="streaming-counter-job"
        )

        print(f"Job started: {job['job_uuid']}")
        print("Streaming output (press Ctrl+C to stop)...\n")

        # Stream logs in real-time
        try:
            # Get log stream
            log_stream = client.jobs.get_job_logs(job["job_uuid"])

            # Process logs as they arrive
            for log_chunk in log_stream:
                # Print without buffering
                print(log_chunk.decode(), end="", flush=True)

        except KeyboardInterrupt:
            print("\n\nStopped streaming (job may still be running)")
        except Exception as e:
            print(f"\nError streaming logs: {e}")

        # Get final job status
        final_status = client.jobs.get_job_status(job["job_uuid"])
        print(f"\n\nFinal job status: {final_status['status']}")

        if final_status["exit_code"] is not None:
            print(f"Exit code: {final_status['exit_code']}")


if __name__ == "__main__":
    main()
