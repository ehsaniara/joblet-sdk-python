"""
Joblet SDK Exception Classes

This module defines all custom exceptions used throughout the Joblet Python SDK.
These exceptions provide specific error types that help developers handle different
types of failures that can occur when interacting with a Joblet server.

The exception hierarchy follows Python best practices with a common base class
(JobletException) that can be used to catch any SDK-related error, and specific
exception types for different categories of failures.

Example:
    >>> from joblet import JobletClient, JobNotFoundError, ConnectionError
    >>>
    >>> try:
    ...     with JobletClient() as client:
    ...         job = client.jobs.get_job_status("invalid-uuid")
    ... except JobNotFoundError:
    ...     print("That job doesn't exist")
    ... except ConnectionError:
    ...     print("Can't connect to the server")
    ... except JobletException:
    ...     print("Some other Joblet-related error occurred")
"""


class JobletException(Exception):
    """
    Base exception class for all Joblet SDK errors.

    This is the parent class for all exceptions raised by the Joblet SDK.
    You can catch this exception type to handle any SDK-related error,
    regardless of the specific cause.

    This exception should not be raised directly - use one of the more
    specific subclasses instead.

    Example:
        >>> try:
        ...     # Any Joblet SDK operation
        ...     client.jobs.run_job(...)
        ... except JobletException as e:
        ...     print(f"Joblet operation failed: {e}")
    """
    pass


class ConnectionError(JobletException):
    """
    Raised when connection to the Joblet server fails.

    This exception indicates network-level connectivity issues such as:
    - Server not reachable (wrong host/port)
    - Network timeouts or connectivity problems
    - TLS/SSL handshake failures
    - Server not responding

    Example:
        >>> try:
        ...     client = JobletClient(host="nonexistent-server.com")
        ... except ConnectionError as e:
        ...     print(f"Could not connect to server: {e}")
    """
    pass


class AuthenticationError(JobletException):
    """
    Raised when authentication with the Joblet server fails.

    This exception occurs when the server rejects the client's credentials
    or when there are authorization issues. Common causes include:
    - Invalid or expired authentication tokens
    - Insufficient permissions for the requested operation
    - Malformed authentication headers

    Example:
        >>> try:
        ...     client = JobletClient(credentials=invalid_creds)
        ...     client.jobs.list_jobs()
        ... except AuthenticationError as e:
        ...     print(f"Authentication failed: {e}")
    """
    pass


class JobNotFoundError(JobletException):
    """
    Raised when a requested job cannot be found.

    This exception is thrown when attempting to perform operations on
    a job that doesn't exist, has been deleted, or when using an
    invalid job UUID.

    Example:
        >>> try:
        ...     status = client.jobs.get_job_status("invalid-job-uuid")
        ... except JobNotFoundError as e:
        ...     print(f"Job not found: {e}")
    """
    pass


class WorkflowNotFoundError(JobletException):
    """
    Raised when a requested workflow cannot be found.

    This exception occurs when trying to access a workflow that doesn't
    exist, has been deleted, or when using an invalid workflow UUID.
    Similar to JobNotFoundError but specifically for workflow operations.

    Example:
        >>> try:
        ...     status = client.jobs.get_workflow_status("invalid-workflow-uuid")
        ... except WorkflowNotFoundError as e:
        ...     print(f"Workflow not found: {e}")
    """
    pass


class RuntimeNotFoundError(JobletException):
    """
    Raised when a requested runtime environment cannot be found.

    This exception is thrown when attempting to use, test, or get information
    about a runtime that isn't installed or doesn't exist. Common causes:
    - Referencing a runtime that hasn't been installed
    - Typos in runtime specification strings
    - Runtime was removed or became unavailable

    Example:
        >>> try:
        ...     info = client.runtimes.get_runtime_info("nonexistent-runtime")
        ... except RuntimeNotFoundError as e:
        ...     print(f"Runtime not available: {e}")
    """
    pass


class NetworkError(JobletException):
    """
    Raised when network operations fail.

    This exception covers errors related to virtual network management
    such as network creation, deletion, or configuration issues. Not to
    be confused with ConnectionError which is about connecting to the server.

    Example:
        >>> try:
        ...     client.networks.create_network("test", "invalid-cidr")
        ... except NetworkError as e:
        ...     print(f"Network operation failed: {e}")
    """
    pass


class VolumeError(JobletException):
    """
    Raised when volume operations fail.

    This exception occurs during storage volume management operations
    such as creation, mounting, deletion, or when there are insufficient
    resources or permission issues with volume operations.

    Example:
        >>> try:
        ...     client.volumes.create_volume("test", "999TB", "filesystem")
        ... except VolumeError as e:
        ...     print(f"Volume operation failed: {e}")
    """
    pass


class ValidationError(JobletException):
    """
    Raised when input validation fails.

    This exception is thrown when the SDK detects invalid input parameters
    before sending requests to the server. This includes malformed data,
    missing required fields, or values outside acceptable ranges.

    Example:
        >>> try:
        ...     client.jobs.run_job(command="", args=[])  # Empty command
        ... except ValidationError as e:
        ...     print(f"Invalid input: {e}")
    """
    pass


class TimeoutError(JobletException):
    """
    Raised when an operation times out.

    This exception occurs when operations take longer than expected or
    configured timeout values. This can happen with long-running operations
    like runtime installations or when the server is under heavy load.

    Example:
        >>> try:
        ...     # Operation that might take too long
        ...     client.runtimes.install_runtime_from_github(...)
        ... except TimeoutError as e:
        ...     print(f"Operation timed out: {e}")
    """
    pass
