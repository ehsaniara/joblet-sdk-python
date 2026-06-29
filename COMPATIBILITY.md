# Compatibility

This is the **Python SDK** (`joblet-sdk-python`, import `joblet`) for Joblet. It
ships generated gRPC stubs for a specific `joblet-proto` version (recorded in
`joblet/_proto_generation_info.py`). The MCP server depends on this SDK.

## Pick an SDK that matches your Joblet server's proto major

Proto **v1.x** and **v2.x** do **not** interoperate. **SDK 1.x targets proto v1;
SDK 2.x targets proto v2** — the v1.1.5 → v2.0.x jump is a breaking change. Use an
SDK whose proto major matches the Joblet server you connect to.

> Release versions are tracked by **git tag**. `pyproject.toml`'s `version` and
> `joblet/__init__.__version__` have historically been wrong (e.g. `0.1.0`,
> `3.0.0`); the **git tag / PyPI release** is authoritative.

## This SDK: version → joblet-proto

| SDK version                  | joblet-proto          | Python |
|------------------------------|-----------------------|--------|
| v1.0.7 – v1.1.5              | v1.0.6 (proto **v1**) | ≥ 3.9  |
| v2.0.1 – v2.0.2              | v2.0.3                | ≥ 3.9  |
| v2.1.0                       | v2.2.1                | ≥ 3.9  |
| v2.1.1 – v2.2.0              | v2.3.0                | ≥ 3.9  |
| v2.3.0 – v2.5.1               | v2.5.4                | ≥ 3.9  |
| **v2.5.2** (current)         | **v2.5.9**            | ≥ 3.9  |

## Full compatibility matrix

RNX ships inside the Joblet repo, so **RNX version == Joblet server version**.

| Python SDK                    | joblet-proto | Joblet server (= RNX) | MCP Server                             |
|-------------------------------|--------------|-----------------------|----------------------------------------|
| **v2.0.1 – v2.5.1** (current) | **v2.x**     | v5.0.2 – v5.6.11      | v1.1.3+ (requires SDK ≥ 2.1.1)         |
| v1.0.7 – v1.1.5               | v1.x         | v4.5.0 – v5.0.1       | v1.1.0 – v1.1.2 (requires SDK ≥ 1.1.4) |

**Recommended current stack:** SDK **v2.5.2** (proto v2.5.9) · Joblet/RNX
**v5.6.11** · MCP **v1.1.3**.

## Feature-availability floors (within proto v2)

The SDK can only use an RPC if the **Joblet server** implements it:

| SDK capability                                            | Needs proto | Min Joblet server | Notes                                                                                                           |
|-----------------------------------------------------------|-------------|-------------------|-----------------------------------------------------------------------------------------------------------------|
| `runtimes.build_runtime`                                  | v2.5.5      | v5.6.x            | Replaced `install_runtime_from_github/local` (removed).                                                         |
| `runtimes.validate_runtime_yaml`                          | v2.5.5      | v5.6.x            | Was `validate_runtime_spec`.                                                                                    |
| `jobs.get_job_telematics` / `stream_job_telematics`       | v2.5.4      | v5.5.4+           | eBPF events.                                                                                                    |
| event-based `jobs.get_job_metrics` / `stream_job_metrics` | v2.5.4      | v5.5.4+           | —                                                                                                               |
| **Workflow methods**                                      | —           | —                 | **Not in the SDK.** Workflow RPCs were removed from proto at v2.4.0 (extracted to a separate project, ADR-013). |

---
_Last reviewed: 2026-06-27._
