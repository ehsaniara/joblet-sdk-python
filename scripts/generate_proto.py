#!/usr/bin/env python3
"""
Generate Python proto bindings from official joblet-proto repository

This script downloads the latest proto files from the official joblet-proto
repository and generates Python bindings for use in the SDK.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result


def check_dependencies():
    """Check if required tools are available."""
    tools = ["git", "python", "protoc"]

    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ {tool} is not available or not working properly")
                return False
            else:
                print(f"✅ {tool} is available")
        except FileNotFoundError:
            print(f"❌ {tool} is not installed")
            return False

    # Check for required Python packages
    try:
        import grpc_tools

        print("✅ grpcio-tools is available")
    except ImportError:
        print("❌ grpcio-tools is not installed. Run: pip install grpcio-tools")
        return False

    return True


def clone_joblet_proto(temp_dir, version=None):
    """Clone the official joblet-proto repository."""
    repo_url = "https://github.com/ehsaniara/joblet-proto.git"
    repo_dir = os.path.join(temp_dir, "joblet-proto")

    print(f"🔄 Cloning {repo_url}...")
    run_command(["git", "clone", repo_url, repo_dir])

    # Check out specific version if requested
    if version:
        print(f"🔄 Checking out version: {version}")
        try:
            run_command(["git", "checkout", version], cwd=repo_dir)
        except:
            print(f"❌ Failed to checkout version {version}. Available tags:")
            result = run_command(["git", "tag", "-l"], cwd=repo_dir)
            print(result.stdout)
            sys.exit(1)

    # Get current commit info
    result = run_command(["git", "rev-parse", "HEAD"], cwd=repo_dir)
    commit_hash = result.stdout.strip()

    result = run_command(["git", "log", "-1", "--format=%s"], cwd=repo_dir)
    commit_message = result.stdout.strip()

    # Get tag info if on a tag
    try:
        result = run_command(
            ["git", "describe", "--exact-match", "--tags", "HEAD"], cwd=repo_dir
        )
        tag_name = result.stdout.strip()
        print(
            f"📋 Using tag: {tag_name} (commit: {commit_hash[:8]} - {commit_message})"
        )
    except:
        print(f"📋 Using commit: {commit_hash[:8]} - {commit_message}")
        tag_name = None

    return repo_dir, commit_hash, tag_name


def generate_python_bindings(proto_dir, output_dir):
    """Generate Python protobuf bindings."""
    proto_file = os.path.join(proto_dir, "proto", "joblet.proto")

    if not os.path.exists(proto_file):
        print(f"❌ Proto file not found: {proto_file}")
        sys.exit(1)

    print(f"🔄 Generating Python bindings from {proto_file}...")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate Python protobuf bindings
    cmd = [
        "python",
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={os.path.join(proto_dir, 'proto')}",
        f"--python_out={output_dir}",
        f"--pyi_out={output_dir}",  # Generate type stubs
        f"--grpc_python_out={output_dir}",
        "joblet.proto",
    ]

    run_command(cmd)

    # Verify generated files
    expected_files = ["joblet_pb2.py", "joblet_pb2_grpc.py", "joblet_pb2.pyi"]
    for file_name in expected_files:
        file_path = os.path.join(output_dir, file_name)
        if os.path.exists(file_path):
            print(f"✅ Generated: {file_name}")
        else:
            print(f"❌ Missing: {file_name}")


def update_generation_info(output_dir, commit_hash, tag_name=None):
    """Create a file with generation information."""
    info_file = os.path.join(output_dir, "_proto_generation_info.py")

    tag_info = f'PROTO_TAG = "{tag_name}"' if tag_name else "PROTO_TAG = None"

    content = f'''"""
Proto Generation Information

This file contains information about when and how the proto bindings were generated.
Generated automatically by scripts/generate_proto.py
"""

# Source repository information
PROTO_REPOSITORY = "https://github.com/ehsaniara/joblet-proto"
PROTO_COMMIT_HASH = "{commit_hash}"
{tag_info}
GENERATION_TIMESTAMP = "{subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()}"

# Protocol buffer compiler version
import subprocess
try:
    PROTOC_VERSION = subprocess.run(["protoc", "--version"], capture_output=True, text=True).stdout.strip()
except:
    PROTOC_VERSION = "unknown"

# Python grpcio-tools version
try:
    import grpc_tools
    GRPCIO_TOOLS_VERSION = grpc_tools.__version__
except:
    GRPCIO_TOOLS_VERSION = "unknown"
'''

    with open(info_file, "w") as f:
        f.write(content)

    print(f"✅ Created generation info: {info_file}")


def main():
    """Main generation process."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Python proto bindings from joblet-proto repository"
    )
    parser.add_argument(
        "--version", help="Specific git tag or commit to checkout (default: latest)"
    )
    parser.add_argument(
        "--list-tags", action="store_true", help="List available tags and exit"
    )
    args = parser.parse_args()

    print("🔐 Joblet SDK - Proto Generation Script")
    print("=" * 50)

    # Check if we're in the right directory
    script_dir = Path(__file__).parent
    sdk_root = script_dir.parent
    joblet_dir = os.path.join(sdk_root, "joblet")

    if not os.path.exists(joblet_dir):
        print("❌ This script must be run from the SDK root directory")
        print("Current working directory should contain 'joblet' package")
        sys.exit(1)

    print(f"📁 SDK root directory: {sdk_root}")
    print(f"📁 Output directory: {joblet_dir}")

    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Missing dependencies. Please install required tools.")
        sys.exit(1)

    # Handle list tags option
    if args.list_tags:
        print("\n🔄 Fetching available tags...")
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_url = "https://github.com/ehsaniara/joblet-proto.git"
            repo_dir = os.path.join(temp_dir, "joblet-proto")
            run_command(["git", "clone", repo_url, repo_dir])
            result = run_command(
                ["git", "tag", "-l", "--sort=-version:refname"], cwd=repo_dir
            )
            tags = result.stdout.strip().split("\n")
            if tags and tags[0]:
                print("\n📋 Available tags (newest first):")
                for tag in tags[:10]:  # Show latest 10 tags
                    print(f"  - {tag}")
                if len(tags) > 10:
                    print(f"  ... and {len(tags) - 10} more")
            else:
                print("📋 No tags found in repository")
        return

    # Create temporary directory for cloning
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n📁 Using temporary directory: {temp_dir}")

        # Clone the joblet-proto repository
        repo_dir, commit_hash, tag_name = clone_joblet_proto(temp_dir, args.version)

        # Generate Python bindings
        print("\n🔄 Generating proto bindings...")
        generate_python_bindings(repo_dir, joblet_dir)

        # Update generation info
        print("\n📝 Creating generation info...")
        update_generation_info(joblet_dir, commit_hash, tag_name)

    print("\n🎉 Proto generation completed successfully!")
    print("\nGenerated files:")
    for file_name in [
        "joblet_pb2.py",
        "joblet_pb2_grpc.py",
        "joblet_pb2.pyi",
        "_proto_generation_info.py",
    ]:
        file_path = os.path.join(joblet_dir, file_name)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✅ {file_name} ({size:,} bytes)")

    print(f"\n📋 Proto source: https://github.com/ehsaniara/joblet-proto")
    if tag_name:
        print(f"📋 Version: {tag_name} (commit: {commit_hash[:8]})")
    else:
        print(f"📋 Commit: {commit_hash[:8]}")
    print("\nYou can now use the updated proto bindings in your SDK!")
    print("\nUsage examples:")
    print("  python scripts/generate_proto.py --list-tags    # Show available versions")
    print("  python scripts/generate_proto.py --version v1.0.1  # Use specific version")
    print("  python scripts/generate_proto.py               # Use latest version")


if __name__ == "__main__":
    main()
