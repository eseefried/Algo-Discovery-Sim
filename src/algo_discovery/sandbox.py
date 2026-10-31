"""Docker-only execution. Never fall back to importing generated code on the host."""

import json
import os
import selectors
import subprocess
import tempfile
import time
from pathlib import Path
from uuid import uuid4

from .code_schemas import CircuitValidation, Reference

WORKER_IMAGE = "algo-discovery-qiskit:local"


def docker_command(name: str, image_id: str, directory: Path) -> list[str]:
    return [
        "docker",
        "run",
        "--rm",
        "--name",
        name,
        "--pull=never",
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--pids-limit=64",
        "--memory=1g",
        "--memory-swap=1g",
        "--cpus=1",
        "--user=65534:65534",
        "--log-driver=none",
        "--tmpfs=/tmp:rw,noexec,nosuid,size=32m",
        "--ulimit=nofile=128:128",
        "--env=OPENBLAS_NUM_THREADS=1",
        "--env=OMP_NUM_THREADS=1",
        "--env=RAYON_NUM_THREADS=1",
        "--env=QISKIT_PARALLEL=FALSE",
        "--mount",
        f"type=bind,src={directory},dst=/input,readonly",
        image_id,
        "python",
        "-I",
        "-B",
        "/input/worker.py",
    ]


def bounded_run(command: list[str], timeout: float = 30, max_bytes: int = 8 * 1024 * 1024) -> bytes:
    """Bound host-side buffering as well as worker wall time."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = bytearray()
    deadline = time.monotonic() + timeout
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("Circuit worker exceeded its wall-time limit.")
                if not selector.select(min(remaining, 0.25)):
                    continue
                chunk = os.read(process.stdout.fileno(), 65536)
                if not chunk:
                    break
                output.extend(chunk)
                if len(output) > max_bytes:
                    raise ValueError("Circuit worker exceeded its output limit.")
        process.wait(timeout=max(0.1, deadline - time.monotonic()))
        if process.returncode:
            raise ValueError("Circuit worker failed; check Docker availability and circuit limits.")
        return bytes(output)
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        process.stdout.close()


def validate_in_docker(
    source: str, instance: dict, reference: Reference, *, timeout: float = 30
) -> tuple[CircuitValidation, str | None]:
    try:
        inspect = subprocess.run(
            ["docker", "image", "inspect", WORKER_IMAGE, "--format", "{{.Id}}"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        image_id = inspect.stdout.strip()
        if not image_id.startswith("sha256:") or len(image_id) != 71:
            raise ValueError("Invalid worker image ID.")
    except (OSError, subprocess.SubprocessError, ValueError):
        return CircuitValidation(
            status="unavailable",
            reference=reference,
            detail="Docker worker unavailable. Build it with: "
            "docker build -t algo-discovery-qiskit:local runtime",
        ), None
    name = "algo-discovery-" + uuid4().hex
    try:
        with tempfile.TemporaryDirectory(prefix="algo-circuit-") as temporary:
            directory = Path(temporary)
            directory.chmod(0o755)
            (directory / "circuit.py").write_text(source, encoding="utf-8")
            (directory / "instance.json").write_text(
                json.dumps(instance, allow_nan=False), encoding="utf-8"
            )
            (directory / "worker.py").write_text(
                Path(__file__).with_name("circuit_worker.py").read_text(), encoding="utf-8"
            )
            for path in directory.iterdir():
                path.chmod(0o444)
            wire = json.loads(bounded_run(docker_command(name, image_id, directory), timeout))
        if not isinstance(wire, dict):
            raise TypeError("Worker must return a JSON object.")
        if not wire.get("ok"):
            return CircuitValidation(
                status="failed",
                reference=reference,
                worker_image_id=image_id,
                detail="Isolated build failed: " + str(wire.get("error", "unknown error"))[:1000],
            ), None
        from .verification import assess_wire

        return assess_wire(wire, instance, reference, image_id)
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError, TimeoutError):
        return CircuitValidation(
            status="failed",
            reference=reference,
            worker_image_id=image_id,
            detail="Worker timed out, exceeded limits, or returned invalid circuit/reference data.",
        ), None
    finally:
        try:
            subprocess.run(
                ["docker", "rm", "-f", name], capture_output=True, timeout=10, check=False
            )
        except (OSError, subprocess.SubprocessError):
            pass
