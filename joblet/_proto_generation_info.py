"""
Proto Generation Information

This file contains information about when and how the proto bindings were generated.
Generated automatically by scripts/generate_proto.py
"""

import subprocess

# Source repository information
PROTO_REPOSITORY = "https://github.com/ehsaniara/joblet-proto"
PROTO_COMMIT_HASH = "e3e3a9ea35a90208fdfb94f40ce37d150e2cbe3b"
PROTO_TAG = "v1.0.1"
GENERATION_TIMESTAMP = "Tue Sep 23 04:38:52 AM UTC 2025"

# Protocol buffer compiler version
try:
    PROTOC_VERSION = subprocess.run(
        ["protoc", "--version"], capture_output=True, text=True
    ).stdout.strip()
except Exception:
    PROTOC_VERSION = "unknown"

# Python grpcio-tools version
try:
    import grpc_tools

    GRPCIO_TOOLS_VERSION = grpc_tools.__version__
except Exception:
    GRPCIO_TOOLS_VERSION = "unknown"
