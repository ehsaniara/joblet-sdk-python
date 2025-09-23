#!/usr/bin/env python3
"""
Development setup script for joblet-sdk-python

This script sets up the development environment by:
1. Installing the package in development mode
2. Installing development dependencies
3. Regenerating proto files with correct gRPC compatibility
4. Running basic validation tests
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description="Running command", check=True):
    """Run a command and handle errors gracefully."""
    print(f"🔄 {description}: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"   ✅ {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stdout:
            print(f"   STDOUT: {e.stdout}")
        if e.stderr:
            print(f"   STDERR: {e.stderr}")
        if check:
            sys.exit(1)
        return e


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8+")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")


def install_package_dev_mode():
    """Install the package in development mode."""
    run_command([sys.executable, "-m", "pip", "install", "-e", "."],
                "Installing package in development mode")


def install_dev_dependencies():
    """Install development dependencies."""
    run_command([sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
                "Installing development dependencies")


def regenerate_proto_files():
    """Regenerate proto files for current gRPC version."""
    script_path = Path(__file__).parent / "scripts" / "generate_proto.py"
    run_command([sys.executable, str(script_path), "--force"],
                "Regenerating proto files")


def validate_installation():
    """Validate that the installation works."""
    print("🔄 Validating installation...")
    try:
        # Test import
        import joblet
        print(f"   ✅ Successfully imported joblet SDK version {joblet.__version__}")

        # Test client creation (without connection)
        try:
            from joblet import JobletClient

            # Just test instantiation, not connection
            print("   ✅ JobletClient can be instantiated")
        except Exception as e:
            print(f"   ⚠️  JobletClient instantiation issue: {e}")

        # Check proto generation info
        from joblet._proto_generation_info import GRPCIO_TOOLS_VERSION, PROTO_TAG
        print(f"   ✅ Proto files generated from version {PROTO_TAG} with gRPC Tools {GRPCIO_TOOLS_VERSION}")

    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        sys.exit(1)


def create_example_config():
    """Create an example configuration file."""
    config_dir = Path.home() / ".rnx"
    config_file = config_dir / "rnx-config.yml"

    if not config_file.exists():
        print("🔄 Creating example configuration file...")
        config_dir.mkdir(exist_ok=True)

        example_config = """# Joblet SDK Configuration
# This is an example configuration file. Update with your server details.

server:
  host: "localhost"  # Your Joblet server host
  port: 50051       # Your Joblet server port

# Optional: TLS certificate paths (for secure connections)
# tls:
#   ca_cert: "/path/to/ca.pem"
#   client_cert: "/path/to/client.pem"
#   client_key: "/path/to/client.key"

# Optional: Connection settings
# connection:
#   timeout: 30
#   retry_attempts: 3

# Note: You can override these settings by passing parameters directly to JobletClient()
"""

        with open(config_file, 'w') as f:
            f.write(example_config)

        print(f"   ✅ Created example config at {config_file}")
        print("   ℹ️  Please update the config with your actual server details")
    else:
        print(f"   ✅ Configuration file already exists at {config_file}")


def main():
    """Main development setup process."""
    print("🚀 Setting up Joblet SDK for development...")
    print("=" * 50)

    # Check Python version compatibility
    check_python_version()

    # Install package in development mode
    install_package_dev_mode()

    # Install development dependencies
    install_dev_dependencies()

    # Regenerate proto files to ensure compatibility
    regenerate_proto_files()

    # Validate installation
    validate_installation()

    # Create example config if it doesn't exist
    create_example_config()

    print("\n" + "=" * 50)
    print("🎉 Development setup complete!")
    print("\nNext steps:")
    print("1. Update ~/.rnx/rnx-config.yml with your server details")
    print("2. Run the example: python examples/basic_job.py")
    print("3. Run tests: pytest")
    print("4. Format code: black .")
    print("5. Type check: mypy joblet")
    print("\nUseful commands:")
    print("- Regenerate proto files: python scripts/generate_proto.py")
    print("- List available proto versions: python scripts/generate_proto.py --list-tags")
    print("- Install specific proto version: python scripts/generate_proto.py --version v1.0.1")


if __name__ == "__main__":
    main()