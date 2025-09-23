"""
Joblet Python SDK - Main Client Module

This module provides the main JobletClient class which serves as the primary
entry point for interacting with a Joblet job orchestration server. The client
handles mTLS authentication, connection management, service initialization, and
provides a clean interface to all Joblet functionality.

All Joblet communication requires mutual TLS (mTLS) authentication for security.

Example:
    Basic usage with mTLS certificates:

    >>> from joblet import JobletClient
    >>> with JobletClient(
    ...     host="joblet.company.com",
    ...     port=50051,
    ...     ca_cert_path="/path/to/ca-cert.pem",
    ...     client_cert_path="/path/to/client-cert.pem",
    ...     client_key_path="/path/to/client-key.pem"
    ... ) as client:
    ...     if client.health_check():
    ...         job = client.jobs.run_job(command="echo", args=["Hello"])
    ...         print(f"Job started: {job['job_uuid']}")

    Environment-based certificate configuration:

    >>> import os
    >>> with JobletClient(
    ...     host=os.getenv('JOBLET_HOST', 'localhost'),
    ...     port=int(os.getenv('JOBLET_PORT', '50051')),
    ...     ca_cert_path=os.getenv('JOBLET_CA_CERT_PATH'),
    ...     client_cert_path=os.getenv('JOBLET_CLIENT_CERT_PATH'),
    ...     client_key_path=os.getenv('JOBLET_CLIENT_KEY_PATH')
    ... ) as client:
    ...     jobs = client.jobs.list_jobs()
    ...     print(f"Found {len(jobs)} jobs")
"""

import grpc
from typing import Optional, Dict, Any
from .services import (
    JobService,
    NetworkService,
    VolumeService,
    MonitoringService,
    RuntimeService
)
from .exceptions import ConnectionError


class JobletClient:
    """
    Main client for interacting with Joblet server.

    The JobletClient provides a high-level interface to all Joblet services including
    job execution, workflow management, runtime environments, networking, storage,
    and system monitoring. It manages the underlying gRPC connection and provides
    lazy-loaded service instances for optimal performance.

    This class is designed to be used as a context manager to ensure proper cleanup
    of network resources, though it can also be used directly with manual cleanup.

    Attributes:
        host (str): The hostname or IP address of the Joblet server
        port (int): The port number of the Joblet server
        ca_cert_path (str): Path to the CA certificate file
        client_cert_path (str): Path to the client certificate file
        client_key_path (str): Path to the client private key file
        jobs (JobService): Service for managing jobs and workflows
        networks (NetworkService): Service for managing networks
        volumes (VolumeService): Service for managing storage volumes
        monitoring (MonitoringService): Service for system monitoring
        runtimes (RuntimeService): Service for managing execution runtimes

    Example:
        >>> # Using context manager (recommended)
        >>> with JobletClient(
        ...     host="joblet.company.com",
        ...     ca_cert_path="/certs/ca.pem",
        ...     client_cert_path="/certs/client.pem",
        ...     client_key_path="/certs/client.key"
        ... ) as client:
        ...     jobs = client.jobs.list_jobs()
        ...     print(f"Found {len(jobs)} jobs")

        >>> # Manual cleanup
        >>> client = JobletClient(
        ...     host="remote-server",
        ...     port=50051,
        ...     ca_cert_path="/certs/ca.pem",
        ...     client_cert_path="/certs/client.pem",
        ...     client_key_path="/certs/client.key"
        ... )
        >>> try:
        ...     status = client.monitoring.get_system_status()
        ... finally:
        ...     client.close()
    """

    def __init__(
        self,
        ca_cert_path: str,
        client_cert_path: str,
        client_key_path: str,
        host: str = "localhost",
        port: int = 50051,
        options: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new Joblet client connection with mTLS authentication.

        Creates a secure mTLS connection to the specified Joblet server using
        the provided certificate files. All Joblet communication requires
        mutual TLS authentication for security.

        Args:
            host (str, optional): Hostname or IP address of the Joblet server.
                Defaults to "localhost".
            port (int, optional): Port number of the Joblet server.
                Defaults to 50051 (standard gRPC port).
            ca_cert_path (str): Path to the CA certificate file (.pem format)
                that signed the server's certificate.
            client_cert_path (str): Path to the client certificate file (.pem format)
                used for client authentication.
            client_key_path (str): Path to the client private key file (.pem format)
                corresponding to the client certificate.
            options (Dict[str, Any], optional): Additional gRPC channel options
                such as timeouts, keepalive settings, etc. See gRPC documentation
                for available options.

        Raises:
            ConnectionError: If the connection to the Joblet server fails.
                This can happen due to network issues, incorrect host/port,
                authentication failures, or server unavailability.
            FileNotFoundError: If any of the certificate files cannot be found.
            ValueError: If certificate files are invalid or malformed.

        Example:
            >>> # Standard mTLS connection
            >>> client = JobletClient(
            ...     host="joblet.company.com",
            ...     port=50051,
            ...     ca_cert_path="/path/to/ca-cert.pem",
            ...     client_cert_path="/path/to/client-cert.pem",
            ...     client_key_path="/path/to/client-key.pem"
            ... )

            >>> # With custom gRPC options
            >>> options = {
            ...     'grpc.keepalive_time_ms': 30000,
            ...     'grpc.keepalive_timeout_ms': 5000,
            ... }
            >>> client = JobletClient(
            ...     host="joblet.company.com",
            ...     port=50051,
            ...     ca_cert_path="/certs/ca.pem",
            ...     client_cert_path="/certs/client.pem",
            ...     client_key_path="/certs/client.key",
            ...     options=options
            ... )

            >>> # Environment-based certificate paths
            >>> import os
            >>> client = JobletClient(
            ...     host=os.getenv('JOBLET_HOST'),
            ...     ca_cert_path=os.getenv('JOBLET_CA_CERT'),
            ...     client_cert_path=os.getenv('JOBLET_CLIENT_CERT'),
            ...     client_key_path=os.getenv('JOBLET_CLIENT_KEY')
            ... )
        """
        # Store connection parameters
        self.host = host
        self.port = port
        self.ca_cert_path = ca_cert_path
        self.client_cert_path = client_cert_path
        self.client_key_path = client_key_path
        self._channel = None
        self._options = options or {}

        # Service instances - initialized lazily for better performance
        # These will be created only when first accessed
        self._job_service = None
        self._network_service = None
        self._volume_service = None
        self._monitoring_service = None
        self._runtime_service = None

        # Establish the connection to the server immediately
        self._connect()

    def _connect(self):
        """
        Establish the mTLS gRPC connection to the Joblet server.

        This method loads the required certificate files and creates a secure
        mTLS connection using mutual TLS authentication.

        Raises:
            ConnectionError: If the connection cannot be established due to
                network issues, authentication failures, or server problems.
            FileNotFoundError: If any certificate files cannot be found.
            ValueError: If certificate files are invalid or malformed.
        """
        try:
            # Load certificate files
            try:
                with open(self.ca_cert_path, 'rb') as f:
                    ca_cert = f.read()
                with open(self.client_cert_path, 'rb') as f:
                    client_cert = f.read()
                with open(self.client_key_path, 'rb') as f:
                    client_key = f.read()
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Certificate file not found: {e.filename}")
            except Exception as e:
                raise ValueError(f"Error reading certificate files: {e}")

            # Validate certificate content
            if not ca_cert:
                raise ValueError(f"CA certificate file is empty: {self.ca_cert_path}")
            if not client_cert:
                raise ValueError(
                    f"Client certificate file is empty: {self.client_cert_path}"
                )
            if not client_key:
                raise ValueError(
                    f"Client key file is empty: {self.client_key_path}"
                )

            # Basic format validation
            if b'BEGIN CERTIFICATE' not in ca_cert:
                raise ValueError(f"Invalid CA certificate format: {self.ca_cert_path}")
            if b'BEGIN CERTIFICATE' not in client_cert:
                raise ValueError(
                    f"Invalid client certificate format: {self.client_cert_path}"
                )
            if b'BEGIN' not in client_key or b'PRIVATE KEY' not in client_key:
                raise ValueError(
                    f"Invalid private key format: {self.client_key_path}"
                )

            # Create mTLS credentials
            credentials = grpc.ssl_channel_credentials(
                root_certificates=ca_cert,
                private_key=client_key,
                certificate_chain=client_cert
            )

            # Construct the target address for the gRPC connection
            target = f"{self.host}:{self.port}"

            # Create secure mTLS channel
            self._channel = grpc.secure_channel(
                target,
                credentials,
                options=list(self._options.items())
            )

        except (FileNotFoundError, ValueError) as e:
            # Re-raise certificate-related errors as-is
            raise e
        except Exception as e:
            # Wrap any other connection errors in our custom exception type
            target = f"{self.host}:{self.port}"
            raise ConnectionError(
                f"Failed to connect to Joblet server at {target}: {e}"
            )

    def close(self):
        """
        Close the connection to the Joblet server and clean up resources.

        This method should be called when you're done using the client to
        ensure proper cleanup of network resources. If using the client as
        a context manager, this is called automatically.

        Note:
            After calling close(), the client should not be used for further
            operations. Create a new client instance if needed.
        """
        if self._channel:
            self._channel.close()
            self._channel = None

    def __enter__(self):
        """
        Context manager entry point.

        Returns:
            JobletClient: Self, to allow usage in 'with' statements.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.

        Automatically closes the connection when exiting the 'with' block,
        ensuring proper cleanup regardless of how the block exits.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        self.close()

    @property
    def jobs(self) -> JobService:
        """
        Access the Job Service for managing jobs and workflows.

        The JobService provides methods for running individual jobs, managing
        multi-job workflows, monitoring execution status, streaming logs, and
        handling job lifecycle operations like stopping and deletion.

        Returns:
            JobService: A service instance for job and workflow operations.

        Example:
            >>> with JobletClient() as client:
            ...     # Run a simple job
            ...     job = client.jobs.run_job(command="echo", args=["Hello"])
            ...
            ...     # Monitor the job
            ...     status = client.jobs.get_job_status(job['job_uuid'])
            ...     print(f"Job status: {status['status']}")
        """
        if not self._job_service:
            self._job_service = JobService(self._channel)
        return self._job_service

    @property
    def networks(self) -> NetworkService:
        """
        Access the Network Service for managing isolated networks.

        The NetworkService allows you to create, list, and remove virtual networks
        that provide isolated communication environments for your jobs. This is
        useful for multi-container applications or when you need network isolation.

        Returns:
            NetworkService: A service instance for network operations.

        Example:
            >>> with JobletClient() as client:
            ...     # Create a new network
            ...     network = client.networks.create_network(
            ...         name="my-app-network",
            ...         cidr="10.0.1.0/24"
            ...     )
            ...     print(f"Created network: {network['name']}")
        """
        if not self._network_service:
            self._network_service = NetworkService(self._channel)
        return self._network_service

    @property
    def volumes(self) -> VolumeService:
        """
        Access the Volume Service for managing persistent storage.

        The VolumeService enables creation and management of storage volumes
        that can be mounted into jobs for persistent data storage. Supports
        both filesystem and memory-based volumes with configurable sizes.

        Returns:
            VolumeService: A service instance for volume operations.

        Example:
            >>> with JobletClient() as client:
            ...     # Create a persistent volume
            ...     volume = client.volumes.create_volume(
            ...         name="data-storage",
            ...         size="5GB",
            ...         volume_type="filesystem"
            ...     )
            ...     print(f"Volume path: {volume['path']}")
        """
        if not self._volume_service:
            self._volume_service = VolumeService(self._channel)
        return self._volume_service

    @property
    def monitoring(self) -> MonitoringService:
        """
        Access the Monitoring Service for system health and metrics.

        The MonitoringService provides real-time system status information,
        streaming metrics for CPU, memory, disk, and network usage, and overall
        system health monitoring capabilities.

        Returns:
            MonitoringService: A service instance for monitoring operations.

        Example:
            >>> with JobletClient() as client:
            ...     # Get current system status
            ...     status = client.monitoring.get_system_status()
            ...     print(f"CPU usage: {status['cpu']['usage_percent']:.1f}%")
            ...
            ...     # Stream real-time metrics
            ...     for metrics in client.monitoring.stream_system_metrics():
            ...         print(f"Memory: {metrics['memory']['usage_percent']:.1f}%")
        """
        if not self._monitoring_service:
            self._monitoring_service = MonitoringService(self._channel)
        return self._monitoring_service

    @property
    def runtimes(self) -> RuntimeService:
        """
        Access the Runtime Service for managing execution environments.

        The RuntimeService handles installation, testing, and management of
        runtime environments (like Python, Node.js, Go, etc.) that jobs can
        execute within. Supports installation from GitHub repositories and
        local sources.

        Returns:
            RuntimeService: A service instance for runtime operations.

        Example:
            >>> with JobletClient() as client:
            ...     # List available runtimes
            ...     runtimes = client.runtimes.list_runtimes()
            ...     for runtime in runtimes:
            ...         print(f"- {runtime['name']}: {runtime['language']}")
            ...
            ...     # Test a specific runtime
            ...     result = client.runtimes.test_runtime("python-3.11")
            ...     print(
            ...         f"Runtime test: {'passed' if result['success'] else 'failed'}"
            ...     )
        """
        if not self._runtime_service:
            self._runtime_service = RuntimeService(self._channel)
        return self._runtime_service

    def health_check(self) -> bool:
        """
        Perform a health check to verify server connectivity and availability.

        This method attempts to connect to the Joblet server and retrieve basic
        system status information. It's useful for verifying that the server is
        running and accessible before performing other operations.

        Returns:
            bool: True if the server is healthy and responsive, False otherwise.
                  A False return could indicate network issues, server downtime,
                  authentication problems, or server overload.

        Example:
            >>> client = JobletClient(host="joblet-server.com")
            >>> if client.health_check():
            ...     print("Server is healthy, proceeding with operations")
            ...     jobs = client.jobs.list_jobs()
            ... else:
            ...     print("Server is not available, check connection settings")

        Note:
            This method catches all exceptions and returns False rather than
            raising them, making it safe to use for conditional logic without
            needing exception handling.
        """
        try:
            # Attempt to get system status from the monitoring service
            # This verifies both connectivity and basic server functionality
            status = self.monitoring.get_system_status()
            return status.get('available', False)
        except Exception:
            # Any exception (network, auth, server error) means unhealthy
            return False
