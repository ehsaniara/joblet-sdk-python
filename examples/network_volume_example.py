#!/usr/bin/env python3
"""Network and volume management example with mTLS authentication"""

from joblet import JobletClient
import os


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

        # === Network Management ===
        print("\n=== Network Management ===")

        # List existing networks
        print("\n--- Current Networks ---")
        try:
            networks = client.networks.list_networks()
            if networks:
                for network in networks:
                    print(f"- {network['name']}: {network['cidr']} (bridge: {network['bridge']}, jobs: {network['job_count']})")
            else:
                print("No networks found")
        except Exception as e:
            print(f"Failed to list networks: {e}")

        # Create a new network
        print("\n--- Creating Network ---")
        try:
            network_result = client.networks.create_network(
                name="test-network",
                cidr="10.0.100.0/24"
            )
            print(f"Created network: {network_result['name']}")
            print(f"  CIDR: {network_result['cidr']}")
            print(f"  Bridge: {network_result['bridge']}")

        except Exception as e:
            print(f"Failed to create network: {e}")

        # List networks again to see the new one
        print("\n--- Networks After Creation ---")
        try:
            networks = client.networks.list_networks()
            for network in networks:
                print(f"- {network['name']}: {network['cidr']} (bridge: {network['bridge']}, jobs: {network['job_count']})")
        except Exception as e:
            print(f"Failed to list networks: {e}")

        # === Volume Management ===
        print("\n=== Volume Management ===")

        # List existing volumes
        print("\n--- Current Volumes ---")
        try:
            volumes = client.volumes.list_volumes()
            if volumes:
                for volume in volumes:
                    print(f"- {volume['name']}: {volume['size']} ({volume['type']}, path: {volume['path']}, jobs: {volume['job_count']})")
            else:
                print("No volumes found")
        except Exception as e:
            print(f"Failed to list volumes: {e}")

        # Create volumes
        print("\n--- Creating Volumes ---")
        volume_configs = [
            {"name": "data-volume", "size": "1GB", "type": "filesystem"},
            {"name": "cache-volume", "size": "512MB", "type": "memory"},
            {"name": "logs-volume", "size": "2GB", "type": "filesystem"}
        ]

        for config in volume_configs:
            try:
                volume_result = client.volumes.create_volume(
                    name=config["name"],
                    size=config["size"],
                    volume_type=config["type"]
                )
                print(f"Created volume: {volume_result['name']}")
                print(f"  Size: {volume_result['size']}")
                print(f"  Type: {volume_result['type']}")
                print(f"  Path: {volume_result['path']}")

            except Exception as e:
                print(f"Failed to create volume {config['name']}: {e}")

        # List volumes again
        print("\n--- Volumes After Creation ---")
        try:
            volumes = client.volumes.list_volumes()
            for volume in volumes:
                print(f"- {volume['name']}: {volume['size']} ({volume['type']}, path: {volume['path']}, jobs: {volume['job_count']})")
        except Exception as e:
            print(f"Failed to list volumes: {e}")

        # === Run Job with Network and Volume ===
        print("\n=== Running Job with Network and Volume ===")
        try:
            job_response = client.jobs.run_job(
                command="df",
                args=["-h"],
                name="disk-usage-check",
                network="test-network",
                volumes=["data-volume:/data", "cache-volume:/cache"],
                runtime="alpine",
                max_memory=128
            )

            job_uuid = job_response["job_uuid"]
            print(f"Job started with UUID: {job_uuid}")
            print(f"Using network: test-network")
            print(f"Using volumes: data-volume, cache-volume")

            # Wait for job to complete
            import time
            for _ in range(30):  # Wait up to 30 seconds
                status = client.jobs.get_job_status(job_uuid)
                if status["status"] in ["completed", "failed", "cancelled"]:
                    print(f"Job completed with status: {status['status']}")
                    break
                time.sleep(1)

        except Exception as e:
            print(f"Failed to run job with network and volume: {e}")

        # === Cleanup ===
        print("\n=== Cleanup ===")

        # Remove volumes
        volumes_to_remove = ["data-volume", "cache-volume", "logs-volume"]
        for volume_name in volumes_to_remove:
            try:
                result = client.volumes.remove_volume(volume_name)
                if result["success"]:
                    print(f"✓ Removed volume: {volume_name}")
                else:
                    print(f"✗ Failed to remove volume {volume_name}: {result['message']}")
            except Exception as e:
                print(f"✗ Error removing volume {volume_name}: {e}")

        # Remove network
        try:
            result = client.networks.remove_network("test-network")
            if result["success"]:
                print(f"✓ Removed network: test-network")
            else:
                print(f"✗ Failed to remove network: {result['message']}")
        except Exception as e:
            print(f"✗ Error removing network: {e}")

        print("\nNetwork and volume example completed")


if __name__ == "__main__":
    main()