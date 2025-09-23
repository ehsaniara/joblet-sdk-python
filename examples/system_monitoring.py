#!/usr/bin/env python3
"""System monitoring example with mTLS authentication"""

from joblet import JobletClient
import os
import time
import json


def print_metrics(metrics, title="System Metrics"):
    """Pretty print system metrics"""
    print(f"\n=== {title} ===")
    print(f"Timestamp: {metrics['timestamp']}")

    if "host" in metrics:
        host = metrics["host"]
        print(f"\nHost Info:")
        print(f"  Hostname: {host['hostname']}")
        print(f"  OS: {host['os']} {host['platform_version']}")
        print(f"  Architecture: {host['architecture']}")
        print(f"  CPU Count: {host['cpu_count']}")
        print(f"  Total Memory: {host['total_memory'] / (1024**3):.2f} GB")

    if "cpu" in metrics:
        cpu = metrics["cpu"]
        print(f"\nCPU Metrics:")
        print(f"  Cores: {cpu['cores']}")
        print(f"  Usage: {cpu['usage_percent']:.2f}%")
        print(f"  Load Average: {cpu['load_average']}")

    if "memory" in metrics:
        memory = metrics["memory"]
        total_gb = memory["total_bytes"] / (1024**3)
        used_gb = memory["used_bytes"] / (1024**3)
        print(f"\nMemory Metrics:")
        print(f"  Total: {total_gb:.2f} GB")
        print(f"  Used: {used_gb:.2f} GB ({memory['usage_percent']:.2f}%)")
        print(f"  Available: {memory['available_bytes'] / (1024**3):.2f} GB")

    if "disks" in metrics:
        print(f"\nDisk Metrics:")
        for disk in metrics["disks"]:
            total_gb = disk["total_bytes"] / (1024**3)
            used_gb = disk["used_bytes"] / (1024**3)
            print(f"  {disk['device']} ({disk['mount_point']}):")
            print(f"    Total: {total_gb:.2f} GB")
            print(f"    Used: {used_gb:.2f} GB ({disk['usage_percent']:.2f}%)")

    if "networks" in metrics:
        print(f"\nNetwork Metrics:")
        for net in metrics["networks"]:
            rx_mb = net["bytes_received"] / (1024**2)
            tx_mb = net["bytes_sent"] / (1024**2)
            print(f"  {net['interface']}:")
            print(f"    RX: {rx_mb:.2f} MB ({net['receive_rate']:.2f} B/s)")
            print(f"    TX: {tx_mb:.2f} MB ({net['transmit_rate']:.2f} B/s)")


def main():
    # Connect to Joblet server
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

        # Get current system status
        print("\n--- Getting system status ---")
        try:
            status = client.monitoring.get_system_status()
            print_metrics(status, "Current System Status")

            if "server_version" in status:
                version = status["server_version"]
                print(f"\nServer Version Info:")
                print(f"  Version: {version['version']}")
                print(f"  Component: {version['component']}")
                print(f"  Platform: {version['platform']}")
                print(f"  Build Date: {version['build_date']}")

        except Exception as e:
            print(f"Failed to get system status: {e}")
            return

        # Stream system metrics for a few iterations
        print("\n--- Streaming system metrics ---")
        print("Streaming metrics for 30 seconds (press Ctrl+C to stop)...")

        try:
            count = 0
            for metrics in client.monitoring.stream_system_metrics(interval_seconds=5):
                count += 1
                print_metrics(metrics, f"Streamed Metrics #{count}")

                if count >= 6:  # Stop after 6 iterations (30 seconds)
                    break

        except KeyboardInterrupt:
            print("\nStopped streaming metrics")
        except Exception as e:
            print(f"Failed to stream metrics: {e}")

        print("\nMonitoring example completed")


if __name__ == "__main__":
    main()
