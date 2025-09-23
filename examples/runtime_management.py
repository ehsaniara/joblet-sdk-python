#!/usr/bin/env python3
"""Runtime management example with mTLS authentication"""

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

        if not client.health_check():
            print("Joblet server is not available")
            return

        print("Connected to Joblet server")

        # List available runtimes
        print("\n--- Available Runtimes ---")
        try:
            runtimes = client.runtimes.list_runtimes()

            if not runtimes:
                print("No runtimes available")
            else:
                for runtime in runtimes:
                    status = "✓" if runtime["available"] else "✗"
                    size_mb = (
                        runtime["size_bytes"] / (1024**2)
                        if runtime["size_bytes"]
                        else 0
                    )

                    print(f"{status} {runtime['name']}")
                    print(f"   Language: {runtime['language']} {runtime['version']}")
                    print(f"   Description: {runtime['description']}")
                    print(f"   Size: {size_mb:.2f} MB")

                    if runtime.get("requirements"):
                        req = runtime["requirements"]
                        print(f"   Architectures: {', '.join(req['architectures'])}")
                        if req["gpu"]:
                            print("   Requires GPU: Yes")

                    if runtime["packages"]:
                        print(f"   Packages: {', '.join(runtime['packages'][:5])}")
                        if len(runtime["packages"]) > 5:
                            print(f"   ... and {len(runtime['packages']) - 5} more")
                    print()

        except Exception as e:
            print(f"Failed to list runtimes: {e}")
            return

        # Test a specific runtime
        runtime_to_test = "python-3.11"
        print(f"--- Testing Runtime: {runtime_to_test} ---")
        try:
            # Get detailed runtime info
            runtime_info = client.runtimes.get_runtime_info(runtime_to_test)
            print(f"Runtime found: {runtime_info['name']}")
            print(f"Available: {runtime_info['available']}")

            # Test the runtime
            test_result = client.runtimes.test_runtime(runtime_to_test)
            print(f"Test successful: {test_result['success']}")
            if test_result["output"]:
                print(f"Test output: {test_result['output']}")
            if test_result["error"]:
                print(f"Test error: {test_result['error']}")

        except Exception as e:
            print(f"Runtime {runtime_to_test} not found or test failed: {e}")

        # Validate runtime specifications
        print("\n--- Validating Runtime Specifications ---")
        test_specs = [
            "python-3.11",
            "python-3.11-ml",
            "node-18",
            "go-1.21",
            "invalid-runtime-spec",
        ]

        for spec in test_specs:
            try:
                validation = client.runtimes.validate_runtime_spec(spec)
                status = "✓" if validation["valid"] else "✗"
                print(f"{status} {spec}: {validation['message']}")

                if validation["valid"] and validation.get("spec_info"):
                    info = validation["spec_info"]
                    print(f"   → Language: {info['language']} {info['version']}")
                    if info["variants"]:
                        print(f"   → Variants: {', '.join(info['variants'])}")

            except Exception as e:
                print(f"✗ {spec}: Error - {e}")

        print("\n--- Installing Runtime from GitHub (Example) ---")
        print("This example shows how to install a runtime, but won't actually install")
        print("to avoid side effects. Uncomment to try:")
        print(
            """
        # try:
        #     install_result = client.runtimes.install_runtime_from_github(
        #         runtime_spec="python-3.12-custom",
        #         repository="your-org/python-runtime",
        #         branch="main",
        #         path="runtimes/python-3.12",
        #         force_reinstall=False
        #     )
        #     print(f"Installation started: {install_result['build_job_uuid']}")
        # except Exception as e:
        #     print(f"Installation failed: {e}")
        """
        )

        print("\n--- Streaming Installation (Example) ---")
        print("This example shows how to stream installation progress:")
        print(
            """
        # for chunk in client.runtimes.install_runtime_from_github(
        #     runtime_spec="python-3.12-custom",
        #     repository="your-org/python-runtime",
        #     stream=True
        # ):
        #     if chunk["type"] == "progress":
        #         print(f"Progress: {chunk['message']} ({chunk['step']}/{chunk['total_steps']})")
        #     elif chunk["type"] == "log":
        #         print(f"Log: {chunk['data'].decode('utf-8', errors='ignore')}")
        #     elif chunk["type"] == "result":
        #         print(f"Result: {chunk['success']} - {chunk['message']}")
        """
        )

        print("\nRuntime management example completed")


if __name__ == "__main__":
    main()
