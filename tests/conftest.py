"""
Pytest configuration and shared fixtures for Joblet SDK tests
"""

import os
import tempfile
from typing import Any, Dict
from unittest.mock import MagicMock, Mock

import grpc
import pytest

from joblet import JobletClient
from joblet.services import (
    JobService,
    MonitoringService,
    NetworkService,
    RuntimeService,
    VolumeService,
)


@pytest.fixture
def mock_grpc_channel():
    """Create a mock gRPC channel"""
    channel = Mock(spec=grpc.Channel)
    return channel


@pytest.fixture
def temp_cert_files():
    """Create temporary certificate files for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock certificate content
        ca_cert_content = b"""-----BEGIN CERTIFICATE-----
MIICljCCAX4CCQCKOtxqyugdLjANBgkqhkiG9w0BAQsFADA...
-----END CERTIFICATE-----"""

        client_cert_content = b"""-----BEGIN CERTIFICATE-----
MIICljCCAX4CCQCKOtxqyugdLjANBgkqhkiG9w0BAQsFADA...
-----END CERTIFICATE-----"""

        client_key_content = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...
-----END PRIVATE KEY-----"""

        # Write certificate files
        ca_cert_path = os.path.join(temp_dir, "ca-cert.pem")
        client_cert_path = os.path.join(temp_dir, "client-cert.pem")
        client_key_path = os.path.join(temp_dir, "client-key.pem")

        with open(ca_cert_path, "wb") as f:
            f.write(ca_cert_content)
        with open(client_cert_path, "wb") as f:
            f.write(client_cert_content)
        with open(client_key_path, "wb") as f:
            f.write(client_key_content)

        yield {
            "ca_cert_path": ca_cert_path,
            "client_cert_path": client_cert_path,
            "client_key_path": client_key_path,
        }


@pytest.fixture
def mock_job_service():
    """Create a mock JobService"""
    service = Mock(spec=JobService)
    return service


@pytest.fixture
def mock_network_service():
    """Create a mock NetworkService"""
    service = Mock(spec=NetworkService)
    return service


@pytest.fixture
def mock_volume_service():
    """Create a mock VolumeService"""
    service = Mock(spec=VolumeService)
    return service


@pytest.fixture
def mock_monitoring_service():
    """Create a mock MonitoringService"""
    service = Mock(spec=MonitoringService)
    return service


@pytest.fixture
def mock_runtime_service():
    """Create a mock RuntimeService"""
    service = Mock(spec=RuntimeService)
    return service


@pytest.fixture
def sample_job_response():
    """Sample job response data"""
    return {
        "job_uuid": "test-job-123",
        "status": "running",
        "command": "echo",
        "args": ["hello", "world"],
        "max_cpu": 50,
        "cpu_cores": "",
        "max_memory": 1024,
        "max_iobps": 0,
        "start_time": "2023-01-01T12:00:00Z",
        "end_time": "",
        "exit_code": 0,
        "scheduled_time": "",
    }


@pytest.fixture
def sample_workflow_response():
    """Sample workflow response data"""
    return {
        "workflow_uuid": "test-workflow-456",
        "status": "running",
    }


@pytest.fixture
def sample_system_status():
    """Sample system status data"""
    return {
        "timestamp": "2023-01-01T12:00:00Z",
        "available": True,
        "host": {
            "hostname": "test-host",
            "os": "linux",
            "platform": "ubuntu",
            "platform_version": "20.04",
            "cpu_count": 4,
            "total_memory": 8589934592,  # 8GB
        },
        "cpu": {
            "cores": 4,
            "usage_percent": 25.5,
            "load_average": [1.0, 1.2, 1.1],
        },
        "memory": {
            "total_bytes": 8589934592,
            "used_bytes": 2147483648,  # 2GB
            "usage_percent": 25.0,
        },
    }


@pytest.fixture
def sample_runtime_list():
    """Sample runtime list data"""
    return [
        {
            "name": "python:3.11",
            "language": "python",
            "version": "3.11.0",
            "description": "Python 3.11 runtime environment",
            "size_bytes": 1073741824,  # 1GB
            "packages": ["pip", "setuptools", "wheel"],
            "available": True,
            "requirements": {
                "architectures": ["amd64", "arm64"],
                "gpu": False,
            },
        },
        {
            "name": "node:18",
            "language": "javascript",
            "version": "18.17.0",
            "description": "Node.js 18 runtime environment",
            "size_bytes": 536870912,  # 512MB
            "packages": ["npm", "yarn"],
            "available": True,
            "requirements": {
                "architectures": ["amd64"],
                "gpu": False,
            },
        },
    ]


@pytest.fixture
def sample_network_list():
    """Sample network list data"""
    return [
        {
            "name": "default",
            "cidr": "172.17.0.0/16",
            "bridge": "docker0",
            "job_count": 0,
        },
        {
            "name": "custom-network",
            "cidr": "10.0.1.0/24",
            "bridge": "br-custom",
            "job_count": 2,
        },
    ]


@pytest.fixture
def sample_volume_list():
    """Sample volume list data"""
    return [
        {
            "name": "data-volume",
            "size": "10GB",
            "type": "filesystem",
            "path": "/var/joblet/volumes/data-volume",
            "created_time": "2023-01-01T12:00:00Z",
            "job_count": 1,
        },
        {
            "name": "temp-volume",
            "size": "1GB",
            "type": "memory",
            "path": "/tmp/joblet/temp-volume",
            "created_time": "2023-01-01T12:30:00Z",
            "job_count": 0,
        },
    ]