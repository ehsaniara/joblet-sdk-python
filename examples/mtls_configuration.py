#!/usr/bin/env python3
"""
mTLS Configuration Examples for Joblet SDK

This example demonstrates how to configure mTLS certificates when connecting
to a Joblet server. All Joblet communication requires mutual TLS authentication
for security.
"""

import os
from pathlib import Path
from joblet import JobletClient, ConnectionError


def example_1_basic_mtls():
    """
    Example 1: Basic mTLS Connection

    Standard mTLS connection with certificate files.
    """
    print("=== Example 1: Basic mTLS Connection ===")

    # Certificate file paths
    ca_cert_path = "certs/ca-cert.pem"
    client_cert_path = "certs/client-cert.pem"
    client_key_path = "certs/client-key.pem"

    # Check if certificate files exist
    missing_files = []
    for path in [ca_cert_path, client_cert_path, client_key_path]:
        if not os.path.exists(path):
            missing_files.append(path)

    if missing_files:
        print(f"⚠️  Missing certificate files: {', '.join(missing_files)}")
        print("Please ensure all certificate files are present")
        return

    try:
        with JobletClient(
            host="joblet.company.com",
            port=50051,
            ca_cert_path=ca_cert_path,
            client_cert_path=client_cert_path,
            client_key_path=client_key_path,
        ) as client:

            if client.health_check():
                print("✅ Connected successfully with mTLS")

                # Test basic operations
                jobs = client.jobs.list_jobs()
                print(f"📊 Found {len(jobs)} jobs in the system")

                runtimes = client.runtimes.list_runtimes()
                print(f"🔧 Available runtimes: {len(runtimes)}")
            else:
                print("❌ Server not available")

    except ConnectionError as e:
        print(f"❌ Connection failed: {e}")
    except FileNotFoundError as e:
        print(f"❌ Certificate file error: {e}")
    except ValueError as e:
        print(f"❌ Certificate validation error: {e}")


def example_2_environment_based_config():
    """
    Example 2: Environment-based Configuration

    Production-ready pattern using environment variables for certificate paths.
    This is the recommended approach for production deployments.
    """
    print("\n=== Example 2: Environment-based Configuration ===")

    # Configuration from environment variables
    config = {
        "host": os.getenv("JOBLET_HOST", "localhost"),
        "port": int(os.getenv("JOBLET_PORT", "50051")),
        "ca_cert_path": os.getenv("JOBLET_CA_CERT_PATH"),
        "client_cert_path": os.getenv("JOBLET_CLIENT_CERT_PATH"),
        "client_key_path": os.getenv("JOBLET_CLIENT_KEY_PATH"),
    }

    print(f"📋 Configuration:")
    print(f"   Host: {config['host']}")
    print(f"   Port: {config['port']}")
    print(f"   CA Cert: {config['ca_cert_path'] or 'not set'}")
    print(f"   Client Cert: {config['client_cert_path'] or 'not set'}")
    print(f"   Client Key: {config['client_key_path'] or 'not set'}")

    # Validate required environment variables
    missing_vars = []
    if not config["ca_cert_path"]:
        missing_vars.append("JOBLET_CA_CERT_PATH")
    if not config["client_cert_path"]:
        missing_vars.append("JOBLET_CLIENT_CERT_PATH")
    if not config["client_key_path"]:
        missing_vars.append("JOBLET_CLIENT_KEY_PATH")

    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set all required certificate environment variables")
        return

    try:
        with JobletClient(
            host=config["host"],
            port=config["port"],
            ca_cert_path=config["ca_cert_path"],
            client_cert_path=config["client_cert_path"],
            client_key_path=config["client_key_path"],
        ) as client:

            if client.health_check():
                print("✅ Connected successfully with environment config")

                # Test the connection with system status
                status = client.monitoring.get_system_status()
                if status.get("available"):
                    print(
                        f"🖥️  Server is healthy (CPU: {status.get('cpu', {}).get('usage_percent', 'unknown'):.1f}%)"
                    )
            else:
                print("❌ Server not available")

    except ConnectionError as e:
        print(f"❌ Connection failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_3_certificate_validation():
    """
    Example 3: Certificate Validation Helper

    Utility functions to validate certificate files before attempting connection.
    """
    print("\n=== Example 3: Certificate Validation ===")

    def validate_certificate_file(cert_path, cert_type="certificate"):
        """Validate a certificate file exists and has correct format."""
        if not cert_path:
            return False, f"{cert_type} path not provided"

        if not os.path.exists(cert_path):
            return False, f"{cert_type} file not found: {cert_path}"

        try:
            with open(cert_path, "rb") as f:
                content = f.read()

            if not content:
                return False, f"{cert_type} file is empty: {cert_path}"

            # Basic format validation
            if cert_type.lower() in ["certificate", "ca certificate"]:
                if b"BEGIN CERTIFICATE" not in content:
                    return (
                        False,
                        f"{cert_type} file doesn't appear to be a valid PEM certificate",
                    )
            elif cert_type.lower() == "private key":
                if (
                    b"BEGIN PRIVATE KEY" not in content
                    and b"BEGIN RSA PRIVATE KEY" not in content
                ):
                    return (
                        False,
                        f"{cert_type} file doesn't appear to be a valid PEM private key",
                    )

            return True, f"{cert_type} file is valid"

        except Exception as e:
            return False, f"Error reading {cert_type} file: {e}"

    # Example certificate paths (from environment or default)
    cert_paths = {
        "CA Certificate": os.getenv("JOBLET_CA_CERT_PATH", "certs/ca-cert.pem"),
        "Client Certificate": os.getenv(
            "JOBLET_CLIENT_CERT_PATH", "certs/client-cert.pem"
        ),
        "Private Key": os.getenv("JOBLET_CLIENT_KEY_PATH", "certs/client-key.pem"),
    }

    print("🔍 Validating certificate files:")
    all_valid = True

    for cert_type, cert_path in cert_paths.items():
        is_valid, message = validate_certificate_file(cert_path, cert_type)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {cert_type}: {message}")

        if not is_valid:
            all_valid = False

    if all_valid:
        print("\n🎉 All certificates are valid!")
        print("You can use these certificates to connect to Joblet server")
    else:
        print("\n⚠️  Some certificate files have issues.")
        print("Please check certificate paths and permissions before connecting")


def example_4_custom_grpc_options():
    """
    Example 4: Custom gRPC Options

    Demonstrates how to use custom gRPC options with mTLS connection.
    """
    print("\n=== Example 4: Custom gRPC Options ===")

    # Certificate paths
    ca_cert_path = os.getenv("JOBLET_CA_CERT_PATH", "certs/ca-cert.pem")
    client_cert_path = os.getenv("JOBLET_CLIENT_CERT_PATH", "certs/client-cert.pem")
    client_key_path = os.getenv("JOBLET_CLIENT_KEY_PATH", "certs/client-key.pem")

    # Custom gRPC options for improved reliability
    options = {
        "grpc.keepalive_time_ms": 30000,  # Send keepalive ping every 30 seconds
        "grpc.keepalive_timeout_ms": 5000,  # Wait 5 seconds for ping ack
        "grpc.keepalive_permit_without_calls": True,  # Send pings even when no RPC
        "grpc.http2.max_pings_without_data": 0,  # Allow unlimited pings
        "grpc.http2.min_time_between_pings_ms": 10000,  # Min 10 seconds between pings
        "grpc.http2.min_ping_interval_without_data_ms": 300000,  # Min 5 minutes without data
    }

    if not all(
        os.path.exists(path)
        for path in [ca_cert_path, client_cert_path, client_key_path]
    ):
        print("⚠️  Certificate files not found, skipping example")
        return

    try:
        with JobletClient(
            host=os.getenv("JOBLET_HOST", "localhost"),
            port=int(os.getenv("JOBLET_PORT", "50051")),
            ca_cert_path=ca_cert_path,
            client_cert_path=client_cert_path,
            client_key_path=client_key_path,
            options=options,
        ) as client:

            if client.health_check():
                print("✅ Connected successfully with custom gRPC options")

                # Test streaming operation to verify keepalive settings
                print("🔄 Testing streaming metrics (press Ctrl+C to stop)...")
                try:
                    count = 0
                    for metrics in client.monitoring.stream_system_metrics(
                        interval_seconds=5
                    ):
                        count += 1
                        cpu = metrics.get("cpu", {}).get("usage_percent", 0)
                        memory = metrics.get("memory", {}).get("usage_percent", 0)
                        print(f"   {count}: CPU: {cpu:.1f}%, Memory: {memory:.1f}%")

                        if count >= 3:  # Just show 3 samples
                            print("   (stopping after 3 samples)")
                            break
                except KeyboardInterrupt:
                    print("   Streaming stopped by user")
            else:
                print("❌ Server not available")

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all mTLS configuration examples."""
    print("🔐 Joblet SDK - mTLS Configuration Examples")
    print("=" * 60)

    # Create example certificate directory structure
    print("\n📁 Setting up example certificate directory...")
    cert_dir = Path("certs")
    cert_dir.mkdir(exist_ok=True)

    # Create placeholder files for examples (not real certificates)
    placeholder_files = [
        "certs/ca-cert.pem",
        "certs/client-cert.pem",
        "certs/client-key.pem",
    ]

    for file_path in placeholder_files:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f"# Placeholder {os.path.basename(file_path)}\n")
                f.write("# Replace with your actual certificate content\n")
                if "ca-cert" in file_path or "client-cert" in file_path:
                    f.write("-----BEGIN CERTIFICATE-----\n")
                    f.write("# Your certificate content here\n")
                    f.write("-----END CERTIFICATE-----\n")
                elif "client-key" in file_path:
                    f.write("-----BEGIN PRIVATE KEY-----\n")
                    f.write("# Your private key content here\n")
                    f.write("-----END PRIVATE KEY-----\n")

    print("📝 Created placeholder certificate files (replace with real certificates)")

    # Environment setup help
    print("\n🔧 Environment Variables for Production:")
    print("   export JOBLET_HOST=your-joblet-server.com")
    print("   export JOBLET_PORT=50051")
    print("   export JOBLET_CA_CERT_PATH=/path/to/ca-cert.pem")
    print("   export JOBLET_CLIENT_CERT_PATH=/path/to/client-cert.pem")
    print("   export JOBLET_CLIENT_KEY_PATH=/path/to/client-key.pem")

    # Run examples
    try:
        example_1_basic_mtls()
        example_2_environment_based_config()
        example_3_certificate_validation()
        example_4_custom_grpc_options()

    except KeyboardInterrupt:
        print("\n👋 Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

    print("\n" + "=" * 60)
    print("🎯 Key Points:")
    print("   1. All Joblet communication requires mTLS authentication")
    print("   2. You need CA certificate, client certificate, and client private key")
    print("   3. Use environment variables for production deployments")
    print("   4. Validate certificate files before attempting connection")
    print("   5. Custom gRPC options can improve connection reliability")


if __name__ == "__main__":
    main()
