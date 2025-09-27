"""
Proto Generation Information

This file contains information about when and how the proto bindings were generated.
Generated automatically by scripts/generate_proto.py
"""

import subprocess

# Source repository information
PROTO_REPOSITORY = "https://github.com/ehsaniara/joblet-proto"
PROTO_COMMIT_HASH = "df8311dd0775169994afe38aa23abff587763e58"
PROTO_TAG = "v1.0.4"
GENERATION_TIMESTAMP = "Sat Sep 27 05:39:53 AM UTC 2025"

# Protocol buffer compiler version
try:
    PROTOC_VERSION = subprocess.run(
        ["protoc", "--version"], capture_output=True, text=True
    ).stdout.strip()
except Exception:
    PROTOC_VERSION = "unknown"

# Python grpcio-tools version
GRPCIO_TOOLS_VERSION = "1.75.0"
