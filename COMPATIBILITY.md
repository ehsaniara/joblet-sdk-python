# Version Compatibility

This document describes the version compatibility between the Joblet Python SDK, joblet-proto definitions, and the Joblet server.

## Compatibility Matrix

| SDK Version | joblet-proto | Joblet Server | grpcio   | Python   | Notes |
|-------------|--------------|---------------|----------|----------|-------|
| 2.5.1       | v2.5.4       | ≥2.5.0        | ≥1.75.1  | 3.9-3.12 | AWS Secrets Manager, Parameter Store, env vars support |
| 2.5.0       | v2.5.4       | ≥2.5.0        | ≥1.75.1  | 3.9-3.12 | New exception hierarchy, input validation |
| 2.4.1       | v2.5.4       | ≥2.4.0        | ≥1.75.1  | 3.9-3.12 | Unified upload() function |
| 2.4.0       | v2.5.4       | ≥2.4.0        | ≥1.75.1  | 3.9-3.12 | Runtime build API with OverlayFS isolation |
| 2.3.0       | v2.5.0       | ≥2.3.0        | ≥1.60.0  | 3.9-3.12 | Telematics API (eBPF events) |
| 2.2.0       | v2.4.0       | ≥2.2.0        | ≥1.60.0  | 3.9-3.12 | Workflow removal |
| 2.1.0       | v2.3.x       | ≥2.1.0        | ≥1.60.0  | 3.9-3.12 | Smart log streaming |
| 2.0.0       | v2.0.x       | ≥2.0.0        | ≥1.50.0  | 3.9-3.12 | Initial release |

## Version Policy

### Semantic Versioning

This SDK follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, dependency updates

### Proto Compatibility

The SDK includes pre-generated protobuf bindings. The proto version is tracked in:
- `joblet/_proto_generation_info.py` - Contains `PROTO_TAG` and `PROTO_COMMIT_HASH`

When upgrading the SDK, proto changes are handled automatically. You don't need to regenerate protos unless you're contributing to development.

### Server Compatibility

- **Forward compatible**: Newer SDK versions work with older servers (missing features return errors gracefully)
- **Backward compatible**: Older SDK versions work with newer servers (new server features won't be accessible)

For best results, keep SDK and server versions aligned on the same minor version.

## Checking Versions

### SDK Version

```python
import joblet
print(joblet.__version__)  # e.g., "2.5.1"
```

### Proto Version

```python
from joblet._proto_generation_info import PROTO_TAG, PROTO_COMMIT_HASH
print(f"Proto: {PROTO_TAG} ({PROTO_COMMIT_HASH[:8]})")
```

### Server Version

```python
from joblet import JobletClient

with JobletClient(config_path="~/.rnx/rnx-config.yml") as client:
    status = client.monitoring.get_system_status()
    if "server_version" in status:
        sv = status["server_version"]
        print(f"Server: {sv['version']} (proto: {sv['proto_tag']})")
```

## Dependencies

### Runtime Dependencies

These are installed automatically when you `pip install joblet-sdk-python`:

| Package    | Version   | Purpose |
|------------|-----------|---------|
| grpcio     | ≥1.75.1   | gRPC framework for server communication |
| protobuf   | ≥4.25.0   | Protocol buffer serialization |
| pyyaml     | ≥6.0      | YAML configuration file parsing |

### Development Dependencies

Install with `pip install -e .[dev]`:

| Package       | Version   | Purpose |
|---------------|-----------|---------|
| grpcio-tools  | ≥1.75.1   | Proto file generation |
| pytest        | ≥7.0      | Testing framework |
| mypy          | ≥1.0      | Type checking |
| pre-commit    | ≥3.0      | Git hooks |

## Troubleshooting

### Version Mismatch Errors

If you see:
```
RuntimeError: The grpc package installed is at version X.Y.Z,
but the generated code depends on grpcio>=1.75.1
```

**Solution**: Upgrade grpcio:
```bash
pip install --upgrade grpcio>=1.75.1
```

### Proto Mismatch with Server

If server returns unexpected fields or missing data:

1. Check server version: `client.monitoring.get_system_status()["server_version"]`
2. Compare with SDK's proto version in `_proto_generation_info.py`
3. Upgrade SDK or server to match versions

### Feature Not Available

If a method raises `NotImplementedError` or returns unexpected errors:

- The server may be running an older version that doesn't support the feature
- Check the compatibility matrix above for feature availability

## Related Projects

- [Joblet](https://github.com/ehsaniara/joblet) - Main orchestration system (server)
- [joblet-proto](https://github.com/ehsaniara/joblet-proto) - Protocol Buffer definitions
- [joblet-sdk-python](https://github.com/ehsaniara/joblet-sdk-python) - This SDK
