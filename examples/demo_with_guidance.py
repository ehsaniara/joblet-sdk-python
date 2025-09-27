#!/usr/bin/env python3
"""
Enhanced Joblet SDK Demo

This example demonstrates the Joblet SDK with better error handling,
configuration guidance, and development-friendly features.
"""

import time
from pathlib import Path

from joblet import AuthenticationError, ConnectionError, JobletClient


def print_banner():
    """Print a friendly banner."""
    print("🚀 Joblet SDK Demo")
    print("=" * 40)


def check_configuration():
    """Check if configuration exists and provide guidance."""
    config_path = Path.home() / ".rnx" / "rnx-config.yml"

    if not config_path.exists():
        print("⚠️  No configuration file found!")
        print(f"Expected location: {config_path}")
        print("\nTo create a configuration file:")
        print("1. Run: python setup_dev.py (creates example config)")
        print("2. Edit the config with your server details")
        print("\nOr provide connection details manually:")
        print("   client = JobletClient(host='your-host', port=50051)")
        return False

    print(f"✅ Configuration file found at {config_path}")
    return True


def demo_basic_job(client):
    """Demonstrate running a basic job."""
    print("\n📋 Running basic job demo...")

    try:
        # Run a simple job
        job = client.jobs.run_job(
            command="echo",
            args=["Hello from Joblet SDK!", "Current time:", "$(date)"],
            name="demo-basic-job",
        )

        job_id = job["job_uuid"]
        print(f"✅ Job started successfully!")
        print(f"   Job ID: {job_id}")

        # Monitor job status with a timeout
        print("⏳ Waiting for job completion...")
        max_wait = 30  # Maximum wait time in seconds
        wait_time = 0

        while wait_time < max_wait:
            status = client.jobs.get_job_status(job_id)
            current_status = status["status"]
            print(f"   Status: {current_status} ({wait_time}s)")

            if current_status in ["completed", "failed"]:
                break

            time.sleep(2)
            wait_time += 2

        if wait_time >= max_wait:
            print("⚠️  Job didn't complete within timeout")
            return

        # Get and display logs
        print("\n📄 Job output:")
        try:
            logs = b"".join(client.jobs.get_job_logs(job_id))
            output = logs.decode("utf-8").strip()
            if output:
                for line in output.split("\n"):
                    print(f"   > {line}")
            else:
                print("   (No output)")
        except Exception as e:
            print(f"   ❌ Could not retrieve logs: {e}")

        # Show final status
        final_status = client.jobs.get_job_status(job_id)
        print(f"\n🏁 Job completed with status: {final_status['status']}")

    except Exception as e:
        print(f"❌ Job execution failed: {e}")


def demo_server_info(client):
    """Demonstrate getting server information."""
    print("\n🖥️  Server information demo...")

    try:
        # This would typically show system status
        print("   Server is responsive ✅")
        # Add more server info calls here if available in your API

    except Exception as e:
        print(f"❌ Could not get server info: {e}")


def main():
    """Main demo function."""
    print_banner()

    # Check configuration
    config_exists = check_configuration()

    print("\n🔌 Connecting to Joblet server...")

    # Try default connection (insecure=True by default for self-signed certs)
    print(
        "Trying default connection (bypasses SSL validation for self-signed certs)..."
    )
    try:
        with JobletClient() as client:
            if client.health_check():
                print("✅ Connected via insecure connection!")
                demo_server_info(client)
                demo_basic_job(client)
                return
            else:
                print("⚠️  Default connection failed")
    except Exception as e:
        print(f"⚠️  Default connection error: {e}")

    # If default fails, try secure connection with certificates
    print("\nTrying secure connection with certificates...")
    try:
        with JobletClient(insecure=False) as client:
            # Test connection
            if client.health_check():
                print("✅ Connected to Joblet server successfully!")

                # Run demos
                demo_server_info(client)
                demo_basic_job(client)

            else:
                print("❌ Server health check failed")
                print("Please check:")
                print("1. Server is running and accessible")
                print("2. Configuration file has correct host/port")
                print("3. Network connectivity")

    except ConnectionError as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if the Joblet server is running")
        print("2. Verify host and port in config file")
        print("3. Check network connectivity")
        print("4. Verify SSL/TLS certificates if using secure connection")

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check client certificates")
        print("2. Verify server trust configuration")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error type: {type(e).__name__}")

        # Provide helpful context
        if "grpc" in str(e).lower():
            print("\nThis looks like a gRPC-related error.")
            print("Common solutions:")
            print("1. Check if server is running on the specified port")
            print("2. Verify SSL/TLS configuration")
            print("3. Check firewall/network settings")

    print("\n" + "=" * 40)
    print("Demo complete!")


if __name__ == "__main__":
    main()
