#!/usr/bin/env python3
"""
Live smoke test for the Joblet Python SDK.

Unlike the unit suite (which mocks gRPC), this script makes REAL gRPC calls to a
running Joblet server. Run it once against a v5.6.x server before tagging an SDK
release to confirm the regenerated proto v2.5.9 stubs actually round-trip on the
wire — especially the v2.5.9 ``timeout`` field.

Connection
----------
The client auto-discovers connection settings the same way the examples do.
Provide them via environment variables::

    export JOBLET_HOST=10.0.0.5
    export JOBLET_PORT=50051
    export JOBLET_CA_CERT=/path/to/ca-cert.pem
    export JOBLET_CLIENT_CERT=/path/to/client-cert.pem
    export JOBLET_CLIENT_KEY=/path/to/client-key.pem

...or via a Joblet config file (``--config /path/rnx-config.yml --node NAME``).

Usage
-----
    python scripts/smoke_test.py                 # use env vars
    python scripts/smoke_test.py --config rnx-config.yml --node default

Exit code is 0 only if every check passes; non-zero otherwise. Nothing is left
behind on the server — every job/volume/network it creates is deleted.
"""

import argparse
import sys
import time
import uuid

from joblet import JobletClient, __version__
from joblet._proto_generation_info import PROTO_TAG

# Unique suffix so repeated runs / parallel servers never collide on names.
RUN_ID = uuid.uuid4().hex[:8]

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
INFO = "  "


class SmokeResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []

    def check(self, name, ok, detail=""):
        mark = PASS if ok else FAIL
        line = f"{mark} {name}"
        if detail:
            line += f"  ({detail})"
        print(line)
        if ok:
            self.passed += 1
        else:
            self.failed += 1
            self.failures.append(name)

    def info(self, msg):
        print(f"{INFO}{msg}")


def _wait_for_terminal(client, job_uuid, timeout_s=60):
    """Block until a job leaves PENDING/SCHEDULED/RUNNING, return final status dict."""
    deadline = time.time() + timeout_s
    status = client.jobs.get_job_status(job_uuid)
    while status["status"] in ("PENDING", "SCHEDULED", "RUNNING", "INITIALIZING"):
        if time.time() > deadline:
            break
        time.sleep(0.5)
        status = client.jobs.get_job_status(job_uuid)
    return status


def run_smoke(client, r: SmokeResult):
    # --- 1. health / connectivity -----------------------------------------
    try:
        healthy = client.health_check()
        r.check("health_check() reports server reachable", bool(healthy))
    except Exception as e:
        r.check("health_check()", False, f"{type(e).__name__}: {e}")
        r.info("Cannot reach server — aborting remaining checks.")
        return

    # --- 2. system status (response parsing) ------------------------------
    try:
        status = client.monitoring.get_system_status()
        ok = isinstance(status, dict) and "available" in status
        r.check("monitoring.get_system_status() parses", ok)
        if ok and isinstance(status.get("host"), dict):
            host = status["host"]
            r.info(
                f"host: {host.get('hostname', '?')} "
                f"{host.get('os', '?')}/{host.get('architecture', '?')} "
                f"kernel {host.get('kernel_version', '?')}"
            )
    except Exception as e:
        r.check("monitoring.get_system_status()", False, f"{type(e).__name__}: {e}")

    # --- 3. basic job round-trip ------------------------------------------
    basic_uuid = None
    try:
        job = client.jobs.run_job(
            name=f"smoke-basic-{RUN_ID}",
            command="echo",
            args=["hello-from-smoke-test"],
        )
        basic_uuid = job.get("job_uuid")
        r.check("jobs.run_job() returns a job_uuid", bool(basic_uuid), basic_uuid or "")

        final = _wait_for_terminal(client, basic_uuid)
        r.check(
            "basic job reaches a terminal state",
            final["status"] in ("COMPLETED", "EXITED", "FAILED", "STOPPED"),
            final["status"],
        )

        logs = b"".join(chunk for chunk in client.jobs.get_job_logs(basic_uuid))
        got = b"hello-from-smoke-test" in logs
        r.check(
            "job logs contain expected output",
            got,
            logs.decode(errors="replace").strip()[:60],
        )
    except Exception as e:
        r.check("basic job round-trip", False, f"{type(e).__name__}: {e}")
    finally:
        if basic_uuid:
            try:
                client.jobs.delete_job(basic_uuid)
            except Exception:
                pass

    # --- 4. timeout field (proto v2.5.9) ----------------------------------
    # `sleep 30` would run for 30s; a 3s timeout must terminate it early.
    timeout_uuid = None
    try:
        job = client.jobs.run_job(
            name=f"smoke-timeout-{RUN_ID}",
            command="bash",
            args=["-c", "echo start; sleep 30; echo never"],
            timeout="3s",
        )
        timeout_uuid = job.get("job_uuid")
        start = time.time()
        final = _wait_for_terminal(client, timeout_uuid, timeout_s=30)
        elapsed = time.time() - start
        # The job must NOT run the full 30s — being terminated well under it is
        # the proof the server saw and honored the timeout field.
        terminated_early = elapsed < 20 and final["status"] in (
            "FAILED",
            "STOPPED",
            "TIMEOUT",
            "EXITED",
            "COMPLETED",
        )
        r.check(
            "timeout='3s' terminates a 30s job early (proto v2.5.9)",
            terminated_early,
            f"ended after {elapsed:.1f}s, status={final['status']}",
        )
    except Exception as e:
        r.check("timeout field round-trip", False, f"{type(e).__name__}: {e}")
    finally:
        if timeout_uuid:
            try:
                client.jobs.delete_job(timeout_uuid)
            except Exception:
                pass

    # --- 5. list endpoints (best-effort; non-fatal) -----------------------
    for label, fn in (
        ("jobs.list_jobs()", lambda: client.jobs.list_jobs()),
        ("volumes.list_volumes()", lambda: client.volumes.list_volumes()),
        ("networks.list_networks()", lambda: client.networks.list_networks()),
        ("runtimes.list_runtimes()", lambda: client.runtimes.list_runtimes()),
    ):
        try:
            result = fn()
            r.check(
                f"{label} returns a list",
                isinstance(result, list),
                f"{len(result)} item(s)",
            )
        except Exception as e:
            r.check(label, False, f"{type(e).__name__}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Live smoke test for the Joblet Python SDK"
    )
    parser.add_argument("--host", help="Server host (overrides JOBLET_HOST)")
    parser.add_argument("--port", type=int, help="Server port (overrides JOBLET_PORT)")
    parser.add_argument("--config", help="Path to a Joblet/rnx config file")
    parser.add_argument(
        "--node", default="default", help="Node name within the config file"
    )
    args = parser.parse_args()

    print(f"Joblet SDK smoke test — SDK v{__version__}, proto stubs {PROTO_TAG}")
    print(f"Run ID: {RUN_ID}\n")

    client_kwargs = {}
    if args.host:
        client_kwargs["host"] = args.host
    if args.port:
        client_kwargs["port"] = args.port
    if args.config:
        client_kwargs["config_path"] = args.config
        client_kwargs["node_name"] = args.node

    r = SmokeResult()
    try:
        with JobletClient(**client_kwargs) as client:
            run_smoke(client, r)
    except Exception as e:
        print(f"{FAIL} Could not initialize JobletClient: {type(e).__name__}: {e}")
        print(
            "\nProvide connection details via JOBLET_* env vars or --config."
            " See --help."
        )
        return 2

    print()
    total = r.passed + r.failed
    if r.failed == 0:
        print(
            f"{PASS} ALL {total} CHECKS PASSED"
            f" — SDK v{__version__} round-trips with this server."
        )
        return 0
    print(f"{FAIL} {r.failed}/{total} checks FAILED: {', '.join(r.failures)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
