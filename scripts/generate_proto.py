#!/usr/bin/env python3
"""
Proto file generation script for joblet-sdk-python

This script downloads proto files from the joblet-proto repository and
generates Python bindings compatible with the current gRPC version.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

    if check and result.returncode != 0:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)

    return result


def get_grpc_version():
    """Get the current grpcio-tools version."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", "import grpc_tools; print('unknown')"],
            capture_output=True,
            text=True,
        )
        # Try to get version from pip
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "grpcio-tools"],
            capture_output=True,
            text=True,
        )
        for line in result.stdout.split("\n"):
            if line.startswith("Version:"):
                return line.split(":")[1].strip()
    except Exception:
        pass
    return "unknown"


def get_protoc_version():
    """Get the protoc compiler version."""
    try:
        result = subprocess.run(["protoc", "--version"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return "unknown"


def list_available_tags():
    """List available proto versions from the remote repository."""
    print("Available proto versions:")
    try:
        result = run_command(
            [
                "git",
                "ls-remote",
                "--tags",
                "--refs",
                "https://github.com/ehsaniara/joblet-proto.git",
            ],
            check=False,
        )

        tags = []
        for line in result.stdout.split("\n"):
            if line and "refs/tags/" in line:
                tag = line.split("refs/tags/")[-1]
                if tag.startswith("v"):
                    tags.append(tag)

        # Sort versions (simple lexicographic sort)
        tags.sort(reverse=True)
        for tag in tags:
            print(f"  {tag}")

        return tags
    except Exception as e:
        print(f"Error listing tags: {e}")
        return []


def generate_proto_files(version="latest", force=False):
    """Generate proto files from the specified version."""

    # Get current directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    joblet_dir = project_root / "joblet"

    print(f"Project root: {project_root}")
    print(f"Joblet directory: {joblet_dir}")

    # Create temporary directory for cloning
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        proto_repo = temp_path / "joblet-proto"

        # Clone the proto repository
        print(f"Cloning proto repository to {proto_repo}")
        if version == "latest":
            run_command(
                [
                    "git",
                    "clone",
                    "https://github.com/ehsaniara/joblet-proto.git",
                    str(proto_repo),
                ]
            )
            # Get the latest tag
            result = run_command(
                ["git", "describe", "--tags", "--abbrev=0"], cwd=proto_repo
            )
            version = result.stdout.strip()
            print(f"Latest version: {version}")
        else:
            run_command(
                [
                    "git",
                    "clone",
                    "https://github.com/ehsaniara/joblet-proto.git",
                    str(proto_repo),
                ]
            )
            run_command(["git", "checkout", version], cwd=proto_repo)

        # Get commit hash for version tracking
        result = run_command(["git", "rev-parse", "HEAD"], cwd=proto_repo)
        commit_hash = result.stdout.strip()

        # Find proto files
        proto_files = list(proto_repo.glob("**/*.proto"))
        if not proto_files:
            print("No .proto files found in the repository")
            sys.exit(1)

        print(f"Found {len(proto_files)} proto files")
        for proto_file in proto_files:
            print(f"  {proto_file.relative_to(proto_repo)}")

        # Generate Python bindings
        print("Generating Python bindings...")

        # Ensure joblet directory exists
        joblet_dir.mkdir(exist_ok=True)

        # Generate for each proto file
        for proto_file in proto_files:
            # Find the relative path from the proto repo
            rel_path = proto_file.relative_to(proto_repo)

            # Run protoc with grpc_tools
            cmd = [
                sys.executable,
                "-m",
                "grpc_tools.protoc",
                f"--proto_path={proto_repo}",
                f"--python_out={joblet_dir}",
                f"--grpc_python_out={joblet_dir}",
                f"--pyi_out={joblet_dir}",
                str(rel_path),
            ]

            run_command(cmd)

            print(f"Generated bindings for {rel_path}")

        # Fix import paths in generated gRPC files
        print("Fixing import paths in generated files...")
        for grpc_file in joblet_dir.glob("*_grpc.py"):
            with open(grpc_file, "r") as f:
                content = f.read()

            # Fix proto import paths - replace "from proto import" with "from . import"
            content = content.replace("from proto import", "from . import")

            with open(grpc_file, "w") as f:
                f.write(content)

            print(f"Fixed imports in {grpc_file.name}")

        # Update generation info file
        generation_info = f'''"""
Proto Generation Information

This file contains information about when and how the proto bindings were generated.
Generated automatically by scripts/generate_proto.py
"""

import subprocess

# Source repository information
PROTO_REPOSITORY = "https://github.com/ehsaniara/joblet-proto"
PROTO_COMMIT_HASH = "{commit_hash}"
PROTO_TAG = "{version}"
GENERATION_TIMESTAMP = "{datetime.now(timezone.utc).strftime('%a %b %d %I:%M:%S %p UTC %Y')}"

# Protocol buffer compiler version
try:
    PROTOC_VERSION = subprocess.run(
        ["protoc", "--version"], capture_output=True, text=True
    ).stdout.strip()
except Exception:
    PROTOC_VERSION = "unknown"

# Python grpcio-tools version
GRPCIO_TOOLS_VERSION = "{get_grpc_version()}"
'''

        with open(joblet_dir / "_proto_generation_info.py", "w") as f:
            f.write(generation_info)

        print(f"✅ Proto files generated successfully!")
        print(f"   Version: {version}")
        print(f"   Commit: {commit_hash}")
        print(f"   gRPC Tools: {get_grpc_version()}")

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate proto files for joblet-sdk-python"
    )
    parser.add_argument(
        "--version",
        default="latest",
        help="Proto version to generate (default: latest)",
    )
    parser.add_argument(
        "--list-tags", action="store_true", help="List available proto versions"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force regeneration even if files exist"
    )

    args = parser.parse_args()

    if args.list_tags:
        list_available_tags()
        return

    generate_proto_files(args.version, args.force)


if __name__ == "__main__":
    main()
