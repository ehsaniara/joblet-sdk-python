#!/usr/bin/env python3
"""
File Uploads and Dependency Management

This script demonstrates how to:
1. Upload files to jobs using helper functions
2. Upload entire directories
3. Create files on-the-fly without disk writes
4. Install Python dependencies at runtime
5. Cache dependencies in volumes for faster subsequent runs
"""

import time

from joblet import JobletClient, create_directory, upload_bytes, upload_string


def wait_for_job(client, job_uuid, timeout=60):
    """Wait for a job to complete and return its status."""
    start = time.time()
    while time.time() - start < timeout:
        status = client.jobs.get_job_status(job_uuid)
        if status["status"] in ["COMPLETED", "FAILED", "STOPPED"]:
            return status
        time.sleep(0.5)
    raise TimeoutError(f"Job {job_uuid} did not complete within {timeout}s")


def print_job_output(client, job_uuid):
    """Print the output of a completed job."""
    for chunk in client.jobs.get_job_logs(job_uuid):
        output = chunk.decode().strip()
        if output:
            for line in output.split("\n"):
                print(f"    {line}")


def basic_file_upload_example(client):
    """Example: Upload a Python script and execute it"""
    print("=== Basic File Upload Example ===\n")

    # Create a simple Python script as a string
    script = """#!/usr/bin/env python3
import sys
import os

print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Script location: {__file__}")
print("Hello from uploaded script!")
"""

    # Upload and run the script
    job = client.jobs.run_job(
        name="upload-script",
        command="python",
        args=["hello.py"],
        runtime="python-3.11",
        uploads=[
            upload_string(script, "hello.py", mode=0o755),
        ],
    )

    print(f"Job started: {job['job_uuid']}")
    status = wait_for_job(client, job["job_uuid"])
    print(f"Job status: {status['status']}")
    print("  Output:")
    print_job_output(client, job["job_uuid"])
    print()

    client.jobs.delete_job(job["job_uuid"])


def multi_file_upload_example(client):
    """Example: Upload multiple files including data and configuration"""
    print("=== Multi-File Upload Example ===\n")

    # Main script
    main_script = """#!/usr/bin/env python3
import json

# Read configuration
with open("config.json") as f:
    config = json.load(f)

# Read data
with open("data/input.txt") as f:
    data = f.read()

print(f"Config: {config}")
print(f"Data: {data}")
print(f"Result: {config['greeting']}, {data.strip()}!")
"""

    # Configuration file
    config = '{"greeting": "Hello", "version": "1.0"}'

    # Data file
    data = "World"

    job = client.jobs.run_job(
        name="multi-file",
        command="python",
        args=["main.py"],
        runtime="python-3.11",
        uploads=[
            upload_string(main_script, "main.py", mode=0o755),
            upload_string(config, "config.json"),
            create_directory("data"),
            upload_string(data, "data/input.txt"),
        ],
    )

    print(f"Job started: {job['job_uuid']}")
    status = wait_for_job(client, job["job_uuid"])
    print(f"Job status: {status['status']}")
    print("  Output:")
    print_job_output(client, job["job_uuid"])
    print()

    client.jobs.delete_job(job["job_uuid"])


def binary_file_upload_example(client):
    """Example: Upload binary data"""
    print("=== Binary File Upload Example ===\n")

    # Create some binary data (e.g., a simple serialized structure)
    binary_data = bytes([0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD])

    script = """#!/usr/bin/env python3
with open("data.bin", "rb") as f:
    data = f.read()

print(f"Binary file size: {len(data)} bytes")
print(f"Hex content: {data.hex()}")
print(f"First byte: {data[0]}, Last byte: {data[-1]}")
"""

    job = client.jobs.run_job(
        name="binary-upload",
        command="python",
        args=["read_binary.py"],
        runtime="python-3.11",
        uploads=[
            upload_string(script, "read_binary.py", mode=0o755),
            upload_bytes(binary_data, "data.bin"),
        ],
    )

    print(f"Job started: {job['job_uuid']}")
    status = wait_for_job(client, job["job_uuid"])
    print(f"Job status: {status['status']}")
    print("  Output:")
    print_job_output(client, job["job_uuid"])
    print()

    client.jobs.delete_job(job["job_uuid"])


def install_dependencies_example(client):
    """Example: Install Python packages at runtime"""
    print("=== Install Dependencies at Runtime ===\n")

    # Script that requires external packages
    script = """#!/usr/bin/env python3
import requests

# Make a simple HTTP request
response = requests.get("https://httpbin.org/json")
data = response.json()

print(f"Status: {response.status_code}")
print(f"Response keys: {list(data.keys())}")
"""

    # Wrapper script that installs dependencies first
    wrapper = """#!/bin/bash
set -e
echo "Installing dependencies..."
pip install --user --quiet requests
echo "Running script..."
python main.py
"""

    job = client.jobs.run_job(
        name="install-deps",
        command="bash",
        args=["run.sh"],
        runtime="python-3.11",
        uploads=[
            upload_string(wrapper, "run.sh", mode=0o755),
            upload_string(script, "main.py", mode=0o755),
        ],
    )

    print(f"Job started: {job['job_uuid']}")
    print("  (Installing packages may take a moment...)")
    status = wait_for_job(client, job["job_uuid"], timeout=120)
    print(f"Job status: {status['status']}")
    print("  Output:")
    print_job_output(client, job["job_uuid"])
    print()

    client.jobs.delete_job(job["job_uuid"])


def requirements_file_example(client):
    """Example: Install from requirements.txt"""
    print("=== Requirements.txt Example ===\n")

    # requirements.txt content
    requirements = """# Core dependencies
requests>=2.28.0
python-dateutil>=2.8.0
"""

    # Main script using the installed packages
    script = """#!/usr/bin/env python3
import requests
from dateutil import parser
from datetime import datetime

# Parse a date string
date_str = "2024-01-15T10:30:00Z"
parsed = parser.parse(date_str)
print(f"Parsed date: {parsed}")
print(f"Day of week: {parsed.strftime('%A')}")

# Quick version check
print(f"requests version: {requests.__version__}")
"""

    # Wrapper to install from requirements.txt
    wrapper = """#!/bin/bash
set -e
echo "Installing from requirements.txt..."
pip install --user --quiet -r requirements.txt
echo "Running application..."
python main.py
"""

    job = client.jobs.run_job(
        name="requirements-install",
        command="bash",
        args=["run.sh"],
        runtime="python-3.11",
        uploads=[
            upload_string(wrapper, "run.sh", mode=0o755),
            upload_string(requirements, "requirements.txt"),
            upload_string(script, "main.py", mode=0o755),
        ],
    )

    print(f"Job started: {job['job_uuid']}")
    print("  (Installing from requirements.txt...)")
    status = wait_for_job(client, job["job_uuid"], timeout=120)
    print(f"Job status: {status['status']}")
    print("  Output:")
    print_job_output(client, job["job_uuid"])
    print()

    client.jobs.delete_job(job["job_uuid"])


def cached_dependencies_example(client):
    """Example: Cache dependencies in a volume for faster subsequent runs"""
    print("=== Cached Dependencies Example ===\n")

    volume_name = "python-packages"

    try:
        # Create the packages volume if it doesn't exist
        try:
            client.volumes.create_volume(name=volume_name, size_mb=500)
            print(f"Created volume: {volume_name}")
        except Exception:
            print(f"Volume {volume_name} already exists")

        # First run: Install packages to the volume
        setup_script = """#!/bin/bash
set -e
echo "Installing packages to cache volume..."
pip install --target=/packages --quiet requests numpy
echo "Packages installed to /packages"
ls -la /packages | head -10
"""

        print("\n  Step 1: Installing packages to cache...")
        job1 = client.jobs.run_job(
            name="cache-setup",
            command="bash",
            args=["-c", setup_script],
            runtime="python-3.11",
            volumes=[f"{volume_name}:/packages"],
        )

        status = wait_for_job(client, job1["job_uuid"], timeout=120)
        print(f"  Setup status: {status['status']}")
        print_job_output(client, job1["job_uuid"])
        client.jobs.delete_job(job1["job_uuid"])

        # Second run: Use cached packages (much faster!)
        run_script = """#!/usr/bin/env python3
import sys
sys.path.insert(0, "/packages")

import requests
import numpy as np

print("Using cached packages!")
print(f"requests version: {requests.__version__}")
print(f"numpy version: {np.__version__}")
print(f"Random array: {np.random.rand(3)}")
"""

        print("\n  Step 2: Using cached packages (should be instant)...")
        job2 = client.jobs.run_job(
            name="use-cache",
            command="python",
            args=["run.py"],
            runtime="python-3.11",
            volumes=[f"{volume_name}:/packages"],
            uploads=[
                upload_string(run_script, "run.py", mode=0o755),
            ],
        )

        status = wait_for_job(client, job2["job_uuid"])
        print(f"  Run status: {status['status']}")
        print("  Output:")
        print_job_output(client, job2["job_uuid"])
        client.jobs.delete_job(job2["job_uuid"])

        # Clean up the volume
        client.volumes.remove_volume(volume_name)
        print(f"\n  Cleaned up volume: {volume_name}")

    except Exception as e:
        print(f"  Error: {e}")
        # Try to clean up
        try:
            client.volumes.remove_volume(volume_name)
        except Exception:
            pass

    print()


def ml_runtime_example(client):
    """Example: Use pre-built ML runtime with common packages"""
    print("=== Pre-built ML Runtime Example ===\n")

    # Script using packages pre-installed in python-3.11-ml runtime
    script = """#!/usr/bin/env python3
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Create sample data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Train a simple model
model = LinearRegression()
model.fit(X, y)

# Make predictions
predictions = model.predict([[6], [7]])

print("ML Runtime Demo")
print(f"numpy version: {np.__version__}")
print(f"pandas version: {pd.__version__}")
print(f"Model coefficient: {model.coef_[0]:.2f}")
print(f"Model intercept: {model.intercept_:.2f}")
print(f"Predictions for [6, 7]: {predictions}")
"""

    job = client.jobs.run_job(
        name="ml-runtime",
        command="python",
        args=["ml_demo.py"],
        runtime="python-3.11-ml",  # Has numpy, pandas, sklearn pre-installed
        uploads=[
            upload_string(script, "ml_demo.py", mode=0o755),
        ],
    )

    print(f"Job started: {job['job_uuid']}")
    print("  (Using python-3.11-ml runtime with pre-installed packages)")
    status = wait_for_job(client, job["job_uuid"])
    print(f"Job status: {status['status']}")
    print("  Output:")
    print_job_output(client, job["job_uuid"])
    print()

    client.jobs.delete_job(job["job_uuid"])


def main():
    with JobletClient() as client:
        try:
            # Basic examples
            basic_file_upload_example(client)
            multi_file_upload_example(client)
            binary_file_upload_example(client)

            # Dependency management examples
            install_dependencies_example(client)
            requirements_file_example(client)

            # Advanced: cached dependencies
            cached_dependencies_example(client)

            # Using pre-built runtimes
            ml_runtime_example(client)

            print("All examples completed successfully!")

        except Exception as e:
            print(f"Error: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
