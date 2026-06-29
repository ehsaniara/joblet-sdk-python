from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Jobs(_message.Message):
    __slots__ = ("jobs",)
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[Job]
    def __init__(
        self, jobs: _Optional[_Iterable[_Union[Job, _Mapping]]] = ...
    ) -> None: ...

class Job(_message.Message):
    __slots__ = (
        "uuid",
        "command",
        "args",
        "max_cpu",
        "cpu_cores",
        "max_memory",
        "max_io_bps",
        "status",
        "start_time",
        "end_time",
        "exit_code",
        "scheduled_time",
        "runtime",
        "environment",
        "secret_environment",
        "gpu_indices",
        "gpu_count",
        "gpu_memory_mb",
        "node_id",
        "timeout",
    )

    class EnvironmentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class SecretEnvironmentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    UUID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    MAX_CPU_FIELD_NUMBER: _ClassVar[int]
    CPU_CORES_FIELD_NUMBER: _ClassVar[int]
    MAX_MEMORY_FIELD_NUMBER: _ClassVar[int]
    MAX_IO_BPS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_TIME_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    SECRET_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    GPU_INDICES_FIELD_NUMBER: _ClassVar[int]
    GPU_COUNT_FIELD_NUMBER: _ClassVar[int]
    GPU_MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    command: str
    args: _containers.RepeatedScalarFieldContainer[str]
    max_cpu: int
    cpu_cores: str
    max_memory: int
    max_io_bps: int
    status: str
    start_time: str
    end_time: str
    exit_code: int
    scheduled_time: str
    runtime: str
    environment: _containers.ScalarMap[str, str]
    secret_environment: _containers.ScalarMap[str, str]
    gpu_indices: _containers.RepeatedScalarFieldContainer[int]
    gpu_count: int
    gpu_memory_mb: int
    node_id: str
    timeout: str
    def __init__(
        self,
        uuid: _Optional[str] = ...,
        command: _Optional[str] = ...,
        args: _Optional[_Iterable[str]] = ...,
        max_cpu: _Optional[int] = ...,
        cpu_cores: _Optional[str] = ...,
        max_memory: _Optional[int] = ...,
        max_io_bps: _Optional[int] = ...,
        status: _Optional[str] = ...,
        start_time: _Optional[str] = ...,
        end_time: _Optional[str] = ...,
        exit_code: _Optional[int] = ...,
        scheduled_time: _Optional[str] = ...,
        runtime: _Optional[str] = ...,
        environment: _Optional[_Mapping[str, str]] = ...,
        secret_environment: _Optional[_Mapping[str, str]] = ...,
        gpu_indices: _Optional[_Iterable[int]] = ...,
        gpu_count: _Optional[int] = ...,
        gpu_memory_mb: _Optional[int] = ...,
        node_id: _Optional[str] = ...,
        timeout: _Optional[str] = ...,
    ) -> None: ...

class EmptyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FileUpload(_message.Message):
    __slots__ = ("path", "content", "mode", "is_directory")
    PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    IS_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    path: str
    content: bytes
    mode: int
    is_directory: bool
    def __init__(
        self,
        path: _Optional[str] = ...,
        content: _Optional[bytes] = ...,
        mode: _Optional[int] = ...,
        is_directory: bool = ...,
    ) -> None: ...

class GetJobStatusRequest(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class GetJobStatusResponse(_message.Message):
    __slots__ = (
        "uuid",
        "command",
        "args",
        "max_cpu",
        "cpu_cores",
        "max_memory",
        "max_io_bps",
        "status",
        "start_time",
        "end_time",
        "exit_code",
        "scheduled_time",
        "environment",
        "secret_environment",
        "network",
        "volumes",
        "runtime",
        "work_dir",
        "uploads",
        "gpu_indices",
        "gpu_count",
        "gpu_memory_mb",
        "node_id",
        "timeout",
    )

    class EnvironmentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class SecretEnvironmentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    UUID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    MAX_CPU_FIELD_NUMBER: _ClassVar[int]
    CPU_CORES_FIELD_NUMBER: _ClassVar[int]
    MAX_MEMORY_FIELD_NUMBER: _ClassVar[int]
    MAX_IO_BPS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_TIME_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    SECRET_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    VOLUMES_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    WORK_DIR_FIELD_NUMBER: _ClassVar[int]
    UPLOADS_FIELD_NUMBER: _ClassVar[int]
    GPU_INDICES_FIELD_NUMBER: _ClassVar[int]
    GPU_COUNT_FIELD_NUMBER: _ClassVar[int]
    GPU_MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    command: str
    args: _containers.RepeatedScalarFieldContainer[str]
    max_cpu: int
    cpu_cores: str
    max_memory: int
    max_io_bps: int
    status: str
    start_time: str
    end_time: str
    exit_code: int
    scheduled_time: str
    environment: _containers.ScalarMap[str, str]
    secret_environment: _containers.ScalarMap[str, str]
    network: str
    volumes: _containers.RepeatedScalarFieldContainer[str]
    runtime: str
    work_dir: str
    uploads: _containers.RepeatedScalarFieldContainer[str]
    gpu_indices: _containers.RepeatedScalarFieldContainer[int]
    gpu_count: int
    gpu_memory_mb: int
    node_id: str
    timeout: str
    def __init__(
        self,
        uuid: _Optional[str] = ...,
        command: _Optional[str] = ...,
        args: _Optional[_Iterable[str]] = ...,
        max_cpu: _Optional[int] = ...,
        cpu_cores: _Optional[str] = ...,
        max_memory: _Optional[int] = ...,
        max_io_bps: _Optional[int] = ...,
        status: _Optional[str] = ...,
        start_time: _Optional[str] = ...,
        end_time: _Optional[str] = ...,
        exit_code: _Optional[int] = ...,
        scheduled_time: _Optional[str] = ...,
        environment: _Optional[_Mapping[str, str]] = ...,
        secret_environment: _Optional[_Mapping[str, str]] = ...,
        network: _Optional[str] = ...,
        volumes: _Optional[_Iterable[str]] = ...,
        runtime: _Optional[str] = ...,
        work_dir: _Optional[str] = ...,
        uploads: _Optional[_Iterable[str]] = ...,
        gpu_indices: _Optional[_Iterable[int]] = ...,
        gpu_count: _Optional[int] = ...,
        gpu_memory_mb: _Optional[int] = ...,
        node_id: _Optional[str] = ...,
        timeout: _Optional[str] = ...,
    ) -> None: ...

class StopJobRequest(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class StopJobResponse(_message.Message):
    __slots__ = ("uuid", "status", "end_time", "exit_code")
    UUID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    status: str
    end_time: str
    exit_code: int
    def __init__(
        self,
        uuid: _Optional[str] = ...,
        status: _Optional[str] = ...,
        end_time: _Optional[str] = ...,
        exit_code: _Optional[int] = ...,
    ) -> None: ...

class CancelJobRequest(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class CancelJobResponse(_message.Message):
    __slots__ = ("uuid", "status")
    UUID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    status: str
    def __init__(
        self, uuid: _Optional[str] = ..., status: _Optional[str] = ...
    ) -> None: ...

class DeleteJobRequest(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class DeleteJobResponse(_message.Message):
    __slots__ = ("uuid", "success", "message")
    UUID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    success: bool
    message: str
    def __init__(
        self,
        uuid: _Optional[str] = ...,
        success: bool = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class DeleteAllJobsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteAllJobsResponse(_message.Message):
    __slots__ = ("success", "message", "deleted_count", "skipped_count")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DELETED_COUNT_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_COUNT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    deleted_count: int
    skipped_count: int
    def __init__(
        self,
        success: bool = ...,
        message: _Optional[str] = ...,
        deleted_count: _Optional[int] = ...,
        skipped_count: _Optional[int] = ...,
    ) -> None: ...

class GetJobLogsRequest(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class DataChunk(_message.Message):
    __slots__ = ("payload",)
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: bytes
    def __init__(self, payload: _Optional[bytes] = ...) -> None: ...

class BuildRuntimeRequest(_message.Message):
    __slots__ = ("yaml_content", "dry_run", "verbose", "force_rebuild")
    YAML_CONTENT_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    VERBOSE_FIELD_NUMBER: _ClassVar[int]
    FORCE_REBUILD_FIELD_NUMBER: _ClassVar[int]
    yaml_content: str
    dry_run: bool
    verbose: bool
    force_rebuild: bool
    def __init__(
        self,
        yaml_content: _Optional[str] = ...,
        dry_run: bool = ...,
        verbose: bool = ...,
        force_rebuild: bool = ...,
    ) -> None: ...

class BuildRuntimeProgress(_message.Message):
    __slots__ = ("phase", "log", "result")
    PHASE_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    phase: BuildPhaseProgress
    log: BuildLogLine
    result: BuildResult
    def __init__(
        self,
        phase: _Optional[_Union[BuildPhaseProgress, _Mapping]] = ...,
        log: _Optional[_Union[BuildLogLine, _Mapping]] = ...,
        result: _Optional[_Union[BuildResult, _Mapping]] = ...,
    ) -> None: ...

class BuildPhaseProgress(_message.Message):
    __slots__ = ("phase_number", "total_phases", "phase_name", "message")
    PHASE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PHASES_FIELD_NUMBER: _ClassVar[int]
    PHASE_NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    phase_number: int
    total_phases: int
    phase_name: str
    message: str
    def __init__(
        self,
        phase_number: _Optional[int] = ...,
        total_phases: _Optional[int] = ...,
        phase_name: _Optional[str] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class BuildLogLine(_message.Message):
    __slots__ = ("level", "message", "timestamp")
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    level: str
    message: str
    timestamp: int
    def __init__(
        self,
        level: _Optional[str] = ...,
        message: _Optional[str] = ...,
        timestamp: _Optional[int] = ...,
    ) -> None: ...

class BuildResult(_message.Message):
    __slots__ = (
        "success",
        "message",
        "runtime_name",
        "runtime_version",
        "install_path",
        "size_bytes",
        "build_duration_ms",
    )
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_NAME_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_VERSION_FIELD_NUMBER: _ClassVar[int]
    INSTALL_PATH_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    BUILD_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    runtime_name: str
    runtime_version: str
    install_path: str
    size_bytes: int
    build_duration_ms: int
    def __init__(
        self,
        success: bool = ...,
        message: _Optional[str] = ...,
        runtime_name: _Optional[str] = ...,
        runtime_version: _Optional[str] = ...,
        install_path: _Optional[str] = ...,
        size_bytes: _Optional[int] = ...,
        build_duration_ms: _Optional[int] = ...,
    ) -> None: ...

class ValidateRuntimeYAMLRequest(_message.Message):
    __slots__ = ("yaml_content",)
    YAML_CONTENT_FIELD_NUMBER: _ClassVar[int]
    yaml_content: str
    def __init__(self, yaml_content: _Optional[str] = ...) -> None: ...

class ValidateRuntimeYAMLResponse(_message.Message):
    __slots__ = ("valid", "message", "errors", "warnings", "spec_info")
    VALID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    SPEC_INFO_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    message: str
    errors: _containers.RepeatedScalarFieldContainer[str]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    spec_info: RuntimeYAMLInfo
    def __init__(
        self,
        valid: bool = ...,
        message: _Optional[str] = ...,
        errors: _Optional[_Iterable[str]] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
        spec_info: _Optional[_Union[RuntimeYAMLInfo, _Mapping]] = ...,
    ) -> None: ...

class RuntimeYAMLInfo(_message.Message):
    __slots__ = (
        "name",
        "version",
        "language",
        "language_version",
        "description",
        "pip_packages",
        "npm_packages",
        "has_hooks",
        "requires_gpu",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PIP_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    NPM_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    HAS_HOOKS_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_GPU_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    language: str
    language_version: str
    description: str
    pip_packages: _containers.RepeatedScalarFieldContainer[str]
    npm_packages: _containers.RepeatedScalarFieldContainer[str]
    has_hooks: bool
    requires_gpu: bool
    def __init__(
        self,
        name: _Optional[str] = ...,
        version: _Optional[str] = ...,
        language: _Optional[str] = ...,
        language_version: _Optional[str] = ...,
        description: _Optional[str] = ...,
        pip_packages: _Optional[_Iterable[str]] = ...,
        npm_packages: _Optional[_Iterable[str]] = ...,
        has_hooks: bool = ...,
        requires_gpu: bool = ...,
    ) -> None: ...

class CreateNetworkRequest(_message.Message):
    __slots__ = ("name", "cidr")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CIDR_FIELD_NUMBER: _ClassVar[int]
    name: str
    cidr: str
    def __init__(
        self, name: _Optional[str] = ..., cidr: _Optional[str] = ...
    ) -> None: ...

class CreateNetworkResponse(_message.Message):
    __slots__ = ("name", "cidr", "bridge")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CIDR_FIELD_NUMBER: _ClassVar[int]
    BRIDGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    cidr: str
    bridge: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        cidr: _Optional[str] = ...,
        bridge: _Optional[str] = ...,
    ) -> None: ...

class RemoveNetworkRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RemoveNetworkResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class Network(_message.Message):
    __slots__ = ("name", "cidr", "bridge", "job_count")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CIDR_FIELD_NUMBER: _ClassVar[int]
    BRIDGE_FIELD_NUMBER: _ClassVar[int]
    JOB_COUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    cidr: str
    bridge: str
    job_count: int
    def __init__(
        self,
        name: _Optional[str] = ...,
        cidr: _Optional[str] = ...,
        bridge: _Optional[str] = ...,
        job_count: _Optional[int] = ...,
    ) -> None: ...

class Networks(_message.Message):
    __slots__ = ("networks",)
    NETWORKS_FIELD_NUMBER: _ClassVar[int]
    networks: _containers.RepeatedCompositeFieldContainer[Network]
    def __init__(
        self, networks: _Optional[_Iterable[_Union[Network, _Mapping]]] = ...
    ) -> None: ...

class CreateVolumeRequest(_message.Message):
    __slots__ = ("name", "size", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: str
    type: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        size: _Optional[str] = ...,
        type: _Optional[str] = ...,
    ) -> None: ...

class CreateVolumeResponse(_message.Message):
    __slots__ = ("name", "size", "type", "path")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: str
    type: str
    path: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        size: _Optional[str] = ...,
        type: _Optional[str] = ...,
        path: _Optional[str] = ...,
    ) -> None: ...

class RemoveVolumeRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RemoveVolumeResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class Volume(_message.Message):
    __slots__ = ("name", "size", "type", "path", "created_time", "job_count")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIME_FIELD_NUMBER: _ClassVar[int]
    JOB_COUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: str
    type: str
    path: str
    created_time: str
    job_count: int
    def __init__(
        self,
        name: _Optional[str] = ...,
        size: _Optional[str] = ...,
        type: _Optional[str] = ...,
        path: _Optional[str] = ...,
        created_time: _Optional[str] = ...,
        job_count: _Optional[int] = ...,
    ) -> None: ...

class Volumes(_message.Message):
    __slots__ = ("volumes",)
    VOLUMES_FIELD_NUMBER: _ClassVar[int]
    volumes: _containers.RepeatedCompositeFieldContainer[Volume]
    def __init__(
        self, volumes: _Optional[_Iterable[_Union[Volume, _Mapping]]] = ...
    ) -> None: ...

class SystemStatusResponse(_message.Message):
    __slots__ = (
        "timestamp",
        "available",
        "host",
        "cpu",
        "memory",
        "disks",
        "networks",
        "io",
        "processes",
        "cloud",
        "server_version",
    )
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    DISKS_FIELD_NUMBER: _ClassVar[int]
    NETWORKS_FIELD_NUMBER: _ClassVar[int]
    IO_FIELD_NUMBER: _ClassVar[int]
    PROCESSES_FIELD_NUMBER: _ClassVar[int]
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    SERVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    available: bool
    host: HostInfo
    cpu: CPUMetrics
    memory: MemoryMetrics
    disks: _containers.RepeatedCompositeFieldContainer[DiskMetrics]
    networks: _containers.RepeatedCompositeFieldContainer[NetworkMetrics]
    io: IOMetrics
    processes: ProcessMetrics
    cloud: CloudInfo
    server_version: ServerVersionInfo
    def __init__(
        self,
        timestamp: _Optional[str] = ...,
        available: bool = ...,
        host: _Optional[_Union[HostInfo, _Mapping]] = ...,
        cpu: _Optional[_Union[CPUMetrics, _Mapping]] = ...,
        memory: _Optional[_Union[MemoryMetrics, _Mapping]] = ...,
        disks: _Optional[_Iterable[_Union[DiskMetrics, _Mapping]]] = ...,
        networks: _Optional[_Iterable[_Union[NetworkMetrics, _Mapping]]] = ...,
        io: _Optional[_Union[IOMetrics, _Mapping]] = ...,
        processes: _Optional[_Union[ProcessMetrics, _Mapping]] = ...,
        cloud: _Optional[_Union[CloudInfo, _Mapping]] = ...,
        server_version: _Optional[_Union[ServerVersionInfo, _Mapping]] = ...,
    ) -> None: ...

class SystemMetricsResponse(_message.Message):
    __slots__ = (
        "timestamp",
        "host",
        "cpu",
        "memory",
        "disks",
        "networks",
        "io",
        "processes",
        "cloud",
    )
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    DISKS_FIELD_NUMBER: _ClassVar[int]
    NETWORKS_FIELD_NUMBER: _ClassVar[int]
    IO_FIELD_NUMBER: _ClassVar[int]
    PROCESSES_FIELD_NUMBER: _ClassVar[int]
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    host: HostInfo
    cpu: CPUMetrics
    memory: MemoryMetrics
    disks: _containers.RepeatedCompositeFieldContainer[DiskMetrics]
    networks: _containers.RepeatedCompositeFieldContainer[NetworkMetrics]
    io: IOMetrics
    processes: ProcessMetrics
    cloud: CloudInfo
    def __init__(
        self,
        timestamp: _Optional[str] = ...,
        host: _Optional[_Union[HostInfo, _Mapping]] = ...,
        cpu: _Optional[_Union[CPUMetrics, _Mapping]] = ...,
        memory: _Optional[_Union[MemoryMetrics, _Mapping]] = ...,
        disks: _Optional[_Iterable[_Union[DiskMetrics, _Mapping]]] = ...,
        networks: _Optional[_Iterable[_Union[NetworkMetrics, _Mapping]]] = ...,
        io: _Optional[_Union[IOMetrics, _Mapping]] = ...,
        processes: _Optional[_Union[ProcessMetrics, _Mapping]] = ...,
        cloud: _Optional[_Union[CloudInfo, _Mapping]] = ...,
    ) -> None: ...

class StreamMetricsRequest(_message.Message):
    __slots__ = ("interval_seconds", "metric_types")
    INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPES_FIELD_NUMBER: _ClassVar[int]
    interval_seconds: int
    metric_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        interval_seconds: _Optional[int] = ...,
        metric_types: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class HostInfo(_message.Message):
    __slots__ = (
        "hostname",
        "os",
        "kernel_version",
        "architecture",
        "boot_time",
        "uptime",
        "node_id",
        "server_ips",
        "mac_addresses",
    )
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    KERNEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    ARCHITECTURE_FIELD_NUMBER: _ClassVar[int]
    BOOT_TIME_FIELD_NUMBER: _ClassVar[int]
    UPTIME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_IPS_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    os: str
    kernel_version: str
    architecture: str
    boot_time: str
    uptime: int
    node_id: str
    server_ips: _containers.RepeatedScalarFieldContainer[str]
    mac_addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        hostname: _Optional[str] = ...,
        os: _Optional[str] = ...,
        kernel_version: _Optional[str] = ...,
        architecture: _Optional[str] = ...,
        boot_time: _Optional[str] = ...,
        uptime: _Optional[int] = ...,
        node_id: _Optional[str] = ...,
        server_ips: _Optional[_Iterable[str]] = ...,
        mac_addresses: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class CPUMetrics(_message.Message):
    __slots__ = (
        "cores",
        "usage_percent",
        "user_time",
        "system_time",
        "idle_time",
        "io_wait_time",
        "steal_time",
        "load_average",
        "per_core_usage",
    )
    CORES_FIELD_NUMBER: _ClassVar[int]
    USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    USER_TIME_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_TIME_FIELD_NUMBER: _ClassVar[int]
    IDLE_TIME_FIELD_NUMBER: _ClassVar[int]
    IO_WAIT_TIME_FIELD_NUMBER: _ClassVar[int]
    STEAL_TIME_FIELD_NUMBER: _ClassVar[int]
    LOAD_AVERAGE_FIELD_NUMBER: _ClassVar[int]
    PER_CORE_USAGE_FIELD_NUMBER: _ClassVar[int]
    cores: int
    usage_percent: float
    user_time: float
    system_time: float
    idle_time: float
    io_wait_time: float
    steal_time: float
    load_average: _containers.RepeatedScalarFieldContainer[float]
    per_core_usage: _containers.RepeatedScalarFieldContainer[float]
    def __init__(
        self,
        cores: _Optional[int] = ...,
        usage_percent: _Optional[float] = ...,
        user_time: _Optional[float] = ...,
        system_time: _Optional[float] = ...,
        idle_time: _Optional[float] = ...,
        io_wait_time: _Optional[float] = ...,
        steal_time: _Optional[float] = ...,
        load_average: _Optional[_Iterable[float]] = ...,
        per_core_usage: _Optional[_Iterable[float]] = ...,
    ) -> None: ...

class MemoryMetrics(_message.Message):
    __slots__ = (
        "total_bytes",
        "used_bytes",
        "free_bytes",
        "available_bytes",
        "usage_percent",
        "cached_bytes",
        "buffered_bytes",
        "swap_total",
        "swap_used",
        "swap_free",
    )
    TOTAL_BYTES_FIELD_NUMBER: _ClassVar[int]
    USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    FREE_BYTES_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_BYTES_FIELD_NUMBER: _ClassVar[int]
    USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    CACHED_BYTES_FIELD_NUMBER: _ClassVar[int]
    BUFFERED_BYTES_FIELD_NUMBER: _ClassVar[int]
    SWAP_TOTAL_FIELD_NUMBER: _ClassVar[int]
    SWAP_USED_FIELD_NUMBER: _ClassVar[int]
    SWAP_FREE_FIELD_NUMBER: _ClassVar[int]
    total_bytes: int
    used_bytes: int
    free_bytes: int
    available_bytes: int
    usage_percent: float
    cached_bytes: int
    buffered_bytes: int
    swap_total: int
    swap_used: int
    swap_free: int
    def __init__(
        self,
        total_bytes: _Optional[int] = ...,
        used_bytes: _Optional[int] = ...,
        free_bytes: _Optional[int] = ...,
        available_bytes: _Optional[int] = ...,
        usage_percent: _Optional[float] = ...,
        cached_bytes: _Optional[int] = ...,
        buffered_bytes: _Optional[int] = ...,
        swap_total: _Optional[int] = ...,
        swap_used: _Optional[int] = ...,
        swap_free: _Optional[int] = ...,
    ) -> None: ...

class DiskMetrics(_message.Message):
    __slots__ = (
        "device",
        "mount_point",
        "filesystem",
        "total_bytes",
        "used_bytes",
        "free_bytes",
        "usage_percent",
        "inodes_total",
        "inodes_used",
        "inodes_free",
        "inodes_usage_percent",
    )
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    MOUNT_POINT_FIELD_NUMBER: _ClassVar[int]
    FILESYSTEM_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BYTES_FIELD_NUMBER: _ClassVar[int]
    USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    FREE_BYTES_FIELD_NUMBER: _ClassVar[int]
    USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    INODES_TOTAL_FIELD_NUMBER: _ClassVar[int]
    INODES_USED_FIELD_NUMBER: _ClassVar[int]
    INODES_FREE_FIELD_NUMBER: _ClassVar[int]
    INODES_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    device: str
    mount_point: str
    filesystem: str
    total_bytes: int
    used_bytes: int
    free_bytes: int
    usage_percent: float
    inodes_total: int
    inodes_used: int
    inodes_free: int
    inodes_usage_percent: float
    def __init__(
        self,
        device: _Optional[str] = ...,
        mount_point: _Optional[str] = ...,
        filesystem: _Optional[str] = ...,
        total_bytes: _Optional[int] = ...,
        used_bytes: _Optional[int] = ...,
        free_bytes: _Optional[int] = ...,
        usage_percent: _Optional[float] = ...,
        inodes_total: _Optional[int] = ...,
        inodes_used: _Optional[int] = ...,
        inodes_free: _Optional[int] = ...,
        inodes_usage_percent: _Optional[float] = ...,
    ) -> None: ...

class NetworkMetrics(_message.Message):
    __slots__ = (
        "interface",
        "bytes_received",
        "bytes_sent",
        "packets_received",
        "packets_sent",
        "errors_in",
        "errors_out",
        "drops_in",
        "drops_out",
        "receive_rate",
        "transmit_rate",
        "ip_addresses",
        "mac_address",
    )
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    BYTES_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    BYTES_SENT_FIELD_NUMBER: _ClassVar[int]
    PACKETS_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    PACKETS_SENT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_IN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_OUT_FIELD_NUMBER: _ClassVar[int]
    DROPS_IN_FIELD_NUMBER: _ClassVar[int]
    DROPS_OUT_FIELD_NUMBER: _ClassVar[int]
    RECEIVE_RATE_FIELD_NUMBER: _ClassVar[int]
    TRANSMIT_RATE_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    interface: str
    bytes_received: int
    bytes_sent: int
    packets_received: int
    packets_sent: int
    errors_in: int
    errors_out: int
    drops_in: int
    drops_out: int
    receive_rate: float
    transmit_rate: float
    ip_addresses: _containers.RepeatedScalarFieldContainer[str]
    mac_address: str
    def __init__(
        self,
        interface: _Optional[str] = ...,
        bytes_received: _Optional[int] = ...,
        bytes_sent: _Optional[int] = ...,
        packets_received: _Optional[int] = ...,
        packets_sent: _Optional[int] = ...,
        errors_in: _Optional[int] = ...,
        errors_out: _Optional[int] = ...,
        drops_in: _Optional[int] = ...,
        drops_out: _Optional[int] = ...,
        receive_rate: _Optional[float] = ...,
        transmit_rate: _Optional[float] = ...,
        ip_addresses: _Optional[_Iterable[str]] = ...,
        mac_address: _Optional[str] = ...,
    ) -> None: ...

class IOMetrics(_message.Message):
    __slots__ = (
        "total_reads",
        "total_writes",
        "read_bytes",
        "write_bytes",
        "read_rate",
        "write_rate",
        "disk_io",
    )
    TOTAL_READS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_WRITES_FIELD_NUMBER: _ClassVar[int]
    READ_BYTES_FIELD_NUMBER: _ClassVar[int]
    WRITE_BYTES_FIELD_NUMBER: _ClassVar[int]
    READ_RATE_FIELD_NUMBER: _ClassVar[int]
    WRITE_RATE_FIELD_NUMBER: _ClassVar[int]
    DISK_IO_FIELD_NUMBER: _ClassVar[int]
    total_reads: int
    total_writes: int
    read_bytes: int
    write_bytes: int
    read_rate: float
    write_rate: float
    disk_io: _containers.RepeatedCompositeFieldContainer[DiskIOMetrics]
    def __init__(
        self,
        total_reads: _Optional[int] = ...,
        total_writes: _Optional[int] = ...,
        read_bytes: _Optional[int] = ...,
        write_bytes: _Optional[int] = ...,
        read_rate: _Optional[float] = ...,
        write_rate: _Optional[float] = ...,
        disk_io: _Optional[_Iterable[_Union[DiskIOMetrics, _Mapping]]] = ...,
    ) -> None: ...

class DiskIOMetrics(_message.Message):
    __slots__ = (
        "device",
        "reads_completed",
        "writes_completed",
        "read_bytes",
        "write_bytes",
        "read_time",
        "write_time",
        "io_time",
        "utilization",
    )
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    READS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    WRITES_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    READ_BYTES_FIELD_NUMBER: _ClassVar[int]
    WRITE_BYTES_FIELD_NUMBER: _ClassVar[int]
    READ_TIME_FIELD_NUMBER: _ClassVar[int]
    WRITE_TIME_FIELD_NUMBER: _ClassVar[int]
    IO_TIME_FIELD_NUMBER: _ClassVar[int]
    UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    device: str
    reads_completed: int
    writes_completed: int
    read_bytes: int
    write_bytes: int
    read_time: int
    write_time: int
    io_time: int
    utilization: float
    def __init__(
        self,
        device: _Optional[str] = ...,
        reads_completed: _Optional[int] = ...,
        writes_completed: _Optional[int] = ...,
        read_bytes: _Optional[int] = ...,
        write_bytes: _Optional[int] = ...,
        read_time: _Optional[int] = ...,
        write_time: _Optional[int] = ...,
        io_time: _Optional[int] = ...,
        utilization: _Optional[float] = ...,
    ) -> None: ...

class ProcessMetrics(_message.Message):
    __slots__ = (
        "total_processes",
        "running_processes",
        "sleeping_processes",
        "stopped_processes",
        "zombie_processes",
        "total_threads",
        "top_by_cpu",
        "top_by_memory",
    )
    TOTAL_PROCESSES_FIELD_NUMBER: _ClassVar[int]
    RUNNING_PROCESSES_FIELD_NUMBER: _ClassVar[int]
    SLEEPING_PROCESSES_FIELD_NUMBER: _ClassVar[int]
    STOPPED_PROCESSES_FIELD_NUMBER: _ClassVar[int]
    ZOMBIE_PROCESSES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_THREADS_FIELD_NUMBER: _ClassVar[int]
    TOP_BY_CPU_FIELD_NUMBER: _ClassVar[int]
    TOP_BY_MEMORY_FIELD_NUMBER: _ClassVar[int]
    total_processes: int
    running_processes: int
    sleeping_processes: int
    stopped_processes: int
    zombie_processes: int
    total_threads: int
    top_by_cpu: _containers.RepeatedCompositeFieldContainer[ProcessInfo]
    top_by_memory: _containers.RepeatedCompositeFieldContainer[ProcessInfo]
    def __init__(
        self,
        total_processes: _Optional[int] = ...,
        running_processes: _Optional[int] = ...,
        sleeping_processes: _Optional[int] = ...,
        stopped_processes: _Optional[int] = ...,
        zombie_processes: _Optional[int] = ...,
        total_threads: _Optional[int] = ...,
        top_by_cpu: _Optional[_Iterable[_Union[ProcessInfo, _Mapping]]] = ...,
        top_by_memory: _Optional[_Iterable[_Union[ProcessInfo, _Mapping]]] = ...,
    ) -> None: ...

class ProcessInfo(_message.Message):
    __slots__ = (
        "pid",
        "ppid",
        "name",
        "command",
        "cpu_percent",
        "memory_percent",
        "memory_bytes",
        "status",
        "start_time",
    )
    PID_FIELD_NUMBER: _ClassVar[int]
    PPID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    CPU_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    pid: int
    ppid: int
    name: str
    command: str
    cpu_percent: float
    memory_percent: float
    memory_bytes: int
    status: str
    start_time: str
    def __init__(
        self,
        pid: _Optional[int] = ...,
        ppid: _Optional[int] = ...,
        name: _Optional[str] = ...,
        command: _Optional[str] = ...,
        cpu_percent: _Optional[float] = ...,
        memory_percent: _Optional[float] = ...,
        memory_bytes: _Optional[int] = ...,
        status: _Optional[str] = ...,
        start_time: _Optional[str] = ...,
    ) -> None: ...

class CloudInfo(_message.Message):
    __slots__ = (
        "provider",
        "region",
        "zone",
        "instance_id",
        "instance_type",
        "hypervisor_type",
        "metadata",
    )

    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    HYPERVISOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    provider: str
    region: str
    zone: str
    instance_id: str
    instance_type: str
    hypervisor_type: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        provider: _Optional[str] = ...,
        region: _Optional[str] = ...,
        zone: _Optional[str] = ...,
        instance_id: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        hypervisor_type: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ServerVersionInfo(_message.Message):
    __slots__ = (
        "version",
        "git_commit",
        "git_tag",
        "build_date",
        "component",
        "go_version",
        "platform",
        "proto_commit",
        "proto_tag",
    )
    VERSION_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    GIT_TAG_FIELD_NUMBER: _ClassVar[int]
    BUILD_DATE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    GO_VERSION_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    PROTO_COMMIT_FIELD_NUMBER: _ClassVar[int]
    PROTO_TAG_FIELD_NUMBER: _ClassVar[int]
    version: str
    git_commit: str
    git_tag: str
    build_date: str
    component: str
    go_version: str
    platform: str
    proto_commit: str
    proto_tag: str
    def __init__(
        self,
        version: _Optional[str] = ...,
        git_commit: _Optional[str] = ...,
        git_tag: _Optional[str] = ...,
        build_date: _Optional[str] = ...,
        component: _Optional[str] = ...,
        go_version: _Optional[str] = ...,
        platform: _Optional[str] = ...,
        proto_commit: _Optional[str] = ...,
        proto_tag: _Optional[str] = ...,
    ) -> None: ...

class ListRuntimesResponse(_message.Message):
    __slots__ = ("runtimes",)
    RUNTIMES_FIELD_NUMBER: _ClassVar[int]
    runtimes: _containers.RepeatedCompositeFieldContainer[RuntimeInfo]
    def __init__(
        self, runtimes: _Optional[_Iterable[_Union[RuntimeInfo, _Mapping]]] = ...
    ) -> None: ...

class RuntimeInfo(_message.Message):
    __slots__ = (
        "name",
        "language",
        "version",
        "description",
        "size_bytes",
        "packages",
        "available",
        "requirements",
        "language_version",
        "libraries",
        "environment",
        "build_info",
        "original_yaml",
    )

    class EnvironmentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    PACKAGES_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_VERSION_FIELD_NUMBER: _ClassVar[int]
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    BUILD_INFO_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_YAML_FIELD_NUMBER: _ClassVar[int]
    name: str
    language: str
    version: str
    description: str
    size_bytes: int
    packages: _containers.RepeatedScalarFieldContainer[str]
    available: bool
    requirements: RuntimeRequirements
    language_version: str
    libraries: _containers.RepeatedScalarFieldContainer[str]
    environment: _containers.ScalarMap[str, str]
    build_info: RuntimeBuildInfo
    original_yaml: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        language: _Optional[str] = ...,
        version: _Optional[str] = ...,
        description: _Optional[str] = ...,
        size_bytes: _Optional[int] = ...,
        packages: _Optional[_Iterable[str]] = ...,
        available: bool = ...,
        requirements: _Optional[_Union[RuntimeRequirements, _Mapping]] = ...,
        language_version: _Optional[str] = ...,
        libraries: _Optional[_Iterable[str]] = ...,
        environment: _Optional[_Mapping[str, str]] = ...,
        build_info: _Optional[_Union[RuntimeBuildInfo, _Mapping]] = ...,
        original_yaml: _Optional[str] = ...,
    ) -> None: ...

class RuntimeBuildInfo(_message.Message):
    __slots__ = ("built_at", "built_with", "platform")
    BUILT_AT_FIELD_NUMBER: _ClassVar[int]
    BUILT_WITH_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    built_at: str
    built_with: str
    platform: str
    def __init__(
        self,
        built_at: _Optional[str] = ...,
        built_with: _Optional[str] = ...,
        platform: _Optional[str] = ...,
    ) -> None: ...

class RuntimeRequirements(_message.Message):
    __slots__ = ("architectures", "gpu")
    ARCHITECTURES_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    architectures: _containers.RepeatedScalarFieldContainer[str]
    gpu: bool
    def __init__(
        self, architectures: _Optional[_Iterable[str]] = ..., gpu: bool = ...
    ) -> None: ...

class GetRuntimeInfoRequest(_message.Message):
    __slots__ = ("runtime",)
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    runtime: str
    def __init__(self, runtime: _Optional[str] = ...) -> None: ...

class GetRuntimeInfoResponse(_message.Message):
    __slots__ = ("runtime", "found")
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    FOUND_FIELD_NUMBER: _ClassVar[int]
    runtime: RuntimeInfo
    found: bool
    def __init__(
        self, runtime: _Optional[_Union[RuntimeInfo, _Mapping]] = ..., found: bool = ...
    ) -> None: ...

class TestRuntimeRequest(_message.Message):
    __slots__ = ("runtime",)
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    runtime: str
    def __init__(self, runtime: _Optional[str] = ...) -> None: ...

class TestRuntimeResponse(_message.Message):
    __slots__ = ("success", "output", "error", "exit_code")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    output: str
    error: str
    exit_code: int
    def __init__(
        self,
        success: bool = ...,
        output: _Optional[str] = ...,
        error: _Optional[str] = ...,
        exit_code: _Optional[int] = ...,
    ) -> None: ...

class RunJobRequest(_message.Message):
    __slots__ = (
        "command",
        "args",
        "max_cpu",
        "cpu_cores",
        "max_memory",
        "max_io_bps",
        "uploads",
        "schedule",
        "network",
        "volumes",
        "runtime",
        "work_dir",
        "environment",
        "secret_environment",
        "gpu_count",
        "gpu_memory_mb",
        "timeout",
    )

    class EnvironmentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class SecretEnvironmentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    MAX_CPU_FIELD_NUMBER: _ClassVar[int]
    CPU_CORES_FIELD_NUMBER: _ClassVar[int]
    MAX_MEMORY_FIELD_NUMBER: _ClassVar[int]
    MAX_IO_BPS_FIELD_NUMBER: _ClassVar[int]
    UPLOADS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    VOLUMES_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    WORK_DIR_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    SECRET_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    GPU_COUNT_FIELD_NUMBER: _ClassVar[int]
    GPU_MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    command: str
    args: _containers.RepeatedScalarFieldContainer[str]
    max_cpu: int
    cpu_cores: str
    max_memory: int
    max_io_bps: int
    uploads: _containers.RepeatedCompositeFieldContainer[FileUpload]
    schedule: str
    network: str
    volumes: _containers.RepeatedScalarFieldContainer[str]
    runtime: str
    work_dir: str
    environment: _containers.ScalarMap[str, str]
    secret_environment: _containers.ScalarMap[str, str]
    gpu_count: int
    gpu_memory_mb: int
    timeout: str
    def __init__(
        self,
        command: _Optional[str] = ...,
        args: _Optional[_Iterable[str]] = ...,
        max_cpu: _Optional[int] = ...,
        cpu_cores: _Optional[str] = ...,
        max_memory: _Optional[int] = ...,
        max_io_bps: _Optional[int] = ...,
        uploads: _Optional[_Iterable[_Union[FileUpload, _Mapping]]] = ...,
        schedule: _Optional[str] = ...,
        network: _Optional[str] = ...,
        volumes: _Optional[_Iterable[str]] = ...,
        runtime: _Optional[str] = ...,
        work_dir: _Optional[str] = ...,
        environment: _Optional[_Mapping[str, str]] = ...,
        secret_environment: _Optional[_Mapping[str, str]] = ...,
        gpu_count: _Optional[int] = ...,
        gpu_memory_mb: _Optional[int] = ...,
        timeout: _Optional[str] = ...,
    ) -> None: ...

class RunJobResponse(_message.Message):
    __slots__ = ("job_uuid", "status")
    JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    job_uuid: str
    status: str
    def __init__(
        self, job_uuid: _Optional[str] = ..., status: _Optional[str] = ...
    ) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    def __init__(
        self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...
    ) -> None: ...

class RemoveRuntimeRequest(_message.Message):
    __slots__ = ("runtime",)
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    runtime: str
    def __init__(self, runtime: _Optional[str] = ...) -> None: ...

class RemoveRuntimeResponse(_message.Message):
    __slots__ = ("success", "message", "freed_space_bytes")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FREED_SPACE_BYTES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    freed_space_bytes: int
    def __init__(
        self,
        success: bool = ...,
        message: _Optional[str] = ...,
        freed_space_bytes: _Optional[int] = ...,
    ) -> None: ...

class StreamJobMetricsRequest(_message.Message):
    __slots__ = ("job_uuid",)
    JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    job_uuid: str
    def __init__(self, job_uuid: _Optional[str] = ...) -> None: ...

class GetJobMetricsRequest(_message.Message):
    __slots__ = ("job_uuid", "start_time", "end_time", "limit")
    JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    job_uuid: str
    start_time: int
    end_time: int
    limit: int
    def __init__(
        self,
        job_uuid: _Optional[str] = ...,
        start_time: _Optional[int] = ...,
        end_time: _Optional[int] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class JobMetricsEvent(_message.Message):
    __slots__ = (
        "timestamp",
        "job_uuid",
        "cpu_percent",
        "memory_bytes",
        "memory_limit",
        "disk_read_bytes",
        "disk_write_bytes",
        "net_recv_bytes",
        "net_sent_bytes",
        "gpu_percent",
        "gpu_memory_bytes",
    )
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    CPU_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    MEMORY_LIMIT_FIELD_NUMBER: _ClassVar[int]
    DISK_READ_BYTES_FIELD_NUMBER: _ClassVar[int]
    DISK_WRITE_BYTES_FIELD_NUMBER: _ClassVar[int]
    NET_RECV_BYTES_FIELD_NUMBER: _ClassVar[int]
    NET_SENT_BYTES_FIELD_NUMBER: _ClassVar[int]
    GPU_PERCENT_FIELD_NUMBER: _ClassVar[int]
    GPU_MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    job_uuid: str
    cpu_percent: float
    memory_bytes: int
    memory_limit: int
    disk_read_bytes: int
    disk_write_bytes: int
    net_recv_bytes: int
    net_sent_bytes: int
    gpu_percent: float
    gpu_memory_bytes: int
    def __init__(
        self,
        timestamp: _Optional[int] = ...,
        job_uuid: _Optional[str] = ...,
        cpu_percent: _Optional[float] = ...,
        memory_bytes: _Optional[int] = ...,
        memory_limit: _Optional[int] = ...,
        disk_read_bytes: _Optional[int] = ...,
        disk_write_bytes: _Optional[int] = ...,
        net_recv_bytes: _Optional[int] = ...,
        net_sent_bytes: _Optional[int] = ...,
        gpu_percent: _Optional[float] = ...,
        gpu_memory_bytes: _Optional[int] = ...,
    ) -> None: ...

class StreamJobTelematicsRequest(_message.Message):
    __slots__ = ("job_uuid", "types")
    JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    job_uuid: str
    types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, job_uuid: _Optional[str] = ..., types: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class GetJobTelematicsRequest(_message.Message):
    __slots__ = ("job_uuid", "types", "start_time", "end_time", "limit")
    JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    job_uuid: str
    types: _containers.RepeatedScalarFieldContainer[str]
    start_time: int
    end_time: int
    limit: int
    def __init__(
        self,
        job_uuid: _Optional[str] = ...,
        types: _Optional[_Iterable[str]] = ...,
        start_time: _Optional[int] = ...,
        end_time: _Optional[int] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class TelematicsEvent(_message.Message):
    __slots__ = (
        "timestamp",
        "job_uuid",
        "type",
        "exec",
        "connect",
        "accept",
        "file",
        "mmap",
        "mprotect",
        "socket_data",
    )
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EXEC_FIELD_NUMBER: _ClassVar[int]
    CONNECT_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    MMAP_FIELD_NUMBER: _ClassVar[int]
    MPROTECT_FIELD_NUMBER: _ClassVar[int]
    SOCKET_DATA_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    job_uuid: str
    type: str
    exec: TelematicsExecData
    connect: TelematicsConnectData
    accept: TelematicsAcceptData
    file: TelematicsFileData
    mmap: TelematicsMmapData
    mprotect: TelematicsMprotectData
    socket_data: TelematicsSocketDataData
    def __init__(
        self,
        timestamp: _Optional[int] = ...,
        job_uuid: _Optional[str] = ...,
        type: _Optional[str] = ...,
        exec: _Optional[_Union[TelematicsExecData, _Mapping]] = ...,
        connect: _Optional[_Union[TelematicsConnectData, _Mapping]] = ...,
        accept: _Optional[_Union[TelematicsAcceptData, _Mapping]] = ...,
        file: _Optional[_Union[TelematicsFileData, _Mapping]] = ...,
        mmap: _Optional[_Union[TelematicsMmapData, _Mapping]] = ...,
        mprotect: _Optional[_Union[TelematicsMprotectData, _Mapping]] = ...,
        socket_data: _Optional[_Union[TelematicsSocketDataData, _Mapping]] = ...,
    ) -> None: ...

class TelematicsExecData(_message.Message):
    __slots__ = ("pid", "ppid", "binary", "args", "exit_code")
    PID_FIELD_NUMBER: _ClassVar[int]
    PPID_FIELD_NUMBER: _ClassVar[int]
    BINARY_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    pid: int
    ppid: int
    binary: str
    args: _containers.RepeatedScalarFieldContainer[str]
    exit_code: int
    def __init__(
        self,
        pid: _Optional[int] = ...,
        ppid: _Optional[int] = ...,
        binary: _Optional[str] = ...,
        args: _Optional[_Iterable[str]] = ...,
        exit_code: _Optional[int] = ...,
    ) -> None: ...

class TelematicsConnectData(_message.Message):
    __slots__ = ("pid", "dst_addr", "dst_port", "protocol", "src_addr", "src_port")
    PID_FIELD_NUMBER: _ClassVar[int]
    DST_ADDR_FIELD_NUMBER: _ClassVar[int]
    DST_PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SRC_ADDR_FIELD_NUMBER: _ClassVar[int]
    SRC_PORT_FIELD_NUMBER: _ClassVar[int]
    pid: int
    dst_addr: str
    dst_port: int
    protocol: str
    src_addr: str
    src_port: int
    def __init__(
        self,
        pid: _Optional[int] = ...,
        dst_addr: _Optional[str] = ...,
        dst_port: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
        src_addr: _Optional[str] = ...,
        src_port: _Optional[int] = ...,
    ) -> None: ...

class TelematicsAcceptData(_message.Message):
    __slots__ = ("pid", "src_addr", "src_port", "dst_addr", "dst_port", "protocol")
    PID_FIELD_NUMBER: _ClassVar[int]
    SRC_ADDR_FIELD_NUMBER: _ClassVar[int]
    SRC_PORT_FIELD_NUMBER: _ClassVar[int]
    DST_ADDR_FIELD_NUMBER: _ClassVar[int]
    DST_PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    pid: int
    src_addr: str
    src_port: int
    dst_addr: str
    dst_port: int
    protocol: str
    def __init__(
        self,
        pid: _Optional[int] = ...,
        src_addr: _Optional[str] = ...,
        src_port: _Optional[int] = ...,
        dst_addr: _Optional[str] = ...,
        dst_port: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
    ) -> None: ...

class TelematicsFileData(_message.Message):
    __slots__ = ("pid", "path", "operation", "bytes", "flags")
    PID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    pid: int
    path: str
    operation: str
    bytes: int
    flags: int
    def __init__(
        self,
        pid: _Optional[int] = ...,
        path: _Optional[str] = ...,
        operation: _Optional[str] = ...,
        bytes: _Optional[int] = ...,
        flags: _Optional[int] = ...,
    ) -> None: ...

class TelematicsMmapData(_message.Message):
    __slots__ = ("pid", "addr", "length", "prot", "flags", "file_path")
    PID_FIELD_NUMBER: _ClassVar[int]
    ADDR_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    PROT_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    pid: int
    addr: int
    length: int
    prot: int
    flags: int
    file_path: str
    def __init__(
        self,
        pid: _Optional[int] = ...,
        addr: _Optional[int] = ...,
        length: _Optional[int] = ...,
        prot: _Optional[int] = ...,
        flags: _Optional[int] = ...,
        file_path: _Optional[str] = ...,
    ) -> None: ...

class TelematicsMprotectData(_message.Message):
    __slots__ = ("pid", "addr", "length", "prot")
    PID_FIELD_NUMBER: _ClassVar[int]
    ADDR_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    PROT_FIELD_NUMBER: _ClassVar[int]
    pid: int
    addr: int
    length: int
    prot: int
    def __init__(
        self,
        pid: _Optional[int] = ...,
        addr: _Optional[int] = ...,
        length: _Optional[int] = ...,
        prot: _Optional[int] = ...,
    ) -> None: ...

class TelematicsSocketDataData(_message.Message):
    __slots__ = (
        "pid",
        "direction",
        "dst_addr",
        "dst_port",
        "src_addr",
        "src_port",
        "protocol",
        "bytes",
    )
    PID_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DST_ADDR_FIELD_NUMBER: _ClassVar[int]
    DST_PORT_FIELD_NUMBER: _ClassVar[int]
    SRC_ADDR_FIELD_NUMBER: _ClassVar[int]
    SRC_PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    pid: int
    direction: str
    dst_addr: str
    dst_port: int
    src_addr: str
    src_port: int
    protocol: str
    bytes: int
    def __init__(
        self,
        pid: _Optional[int] = ...,
        direction: _Optional[str] = ...,
        dst_addr: _Optional[str] = ...,
        dst_port: _Optional[int] = ...,
        src_addr: _Optional[str] = ...,
        src_port: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
        bytes: _Optional[int] = ...,
    ) -> None: ...
