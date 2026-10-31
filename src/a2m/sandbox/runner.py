"""Execute untrusted candidate code in a separate, resource-limited process.

Profiles:
  bwrap  bubblewrap: no network, read-only system, /home /mnt /srv /tmp hidden (vaults and
         papers unreadable). Preferred.
  none   plain subprocess with scrubbed env, temp cwd, and rlimits. Candidate code can still
         read files the user can read. Runs record which profile was used.
"""

from __future__ import annotations

import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HARNESS = Path(__file__).with_name("harness.py")


class SandboxError(RuntimeError):
    pass


def _bwrap_works() -> bool:
    if not shutil.which("bwrap"):
        return False
    try:
        p = subprocess.run(["bwrap", "--ro-bind", "/", "/", "--unshare-net", "--dev", "/dev",
                            "true"], capture_output=True, timeout=10, check=False)
        return p.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


class Sandbox:
    def __init__(self, profile: str = "auto", timeout_s: int = 60, memory_mb: int = 8192):
        if profile == "auto":
            profile = "bwrap" if _bwrap_works() else "none"
        elif profile == "bwrap" and not _bwrap_works():
            raise SandboxError("bwrap profile requested but bubblewrap cannot run here")
        self.profile, self.timeout_s, self.memory_mb = profile, timeout_s, memory_mb
        self.seconds_used = 0.0
        self.executions = 0
        self._cache: dict[str, dict] = {}
        self._lock = threading.Lock()

    def _command(self, workdir: str, args: list[str]) -> list[str]:
        cmd = [sys.executable, "-I", *args]
        if self.profile != "bwrap":
            return cmd
        binds = ["--ro-bind", "/", "/"]
        for hidden in ("/home", "/mnt", "/srv", "/tmp", "/root"):
            if os.path.isdir(hidden):
                binds += ["--tmpfs", hidden]
        for keep in {sys.prefix, sys.base_prefix, str(HARNESS.parent)}:
            binds += ["--ro-bind", keep, keep]
        binds += ["--bind", workdir, workdir]
        return ["bwrap", *binds, "--unshare-all", "--die-with-parent", "--dev", "/dev",
                "--proc", "/proc", "--chdir", workdir, *cmd]

    def _limits(self):
        mem = self.memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
        resource.setrlimit(resource.RLIMIT_CPU, (self.timeout_s, self.timeout_s + 5))
        resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024 * 1024,) * 2)

    def run(self, mode: str, code: str, payload: dict) -> dict:
        key = hashlib.sha256(json.dumps([mode, code, payload], sort_keys=True).encode()).hexdigest()
        with self._lock:
            if key in self._cache:
                return {**self._cache[key], "cached": True}
        with tempfile.TemporaryDirectory(prefix="a2m-") as d:
            cand, pay, out = (os.path.join(d, n) for n in ("candidate.py", "payload.json", "out.json"))
            Path(cand).write_text(code)
            Path(pay).write_text(json.dumps(payload))
            env = {"PATH": "/usr/bin:/bin", "HOME": d, "PYTHONHASHSEED": "0", "OMP_NUM_THREADS": "1",
                   "OPENBLAS_NUM_THREADS": "1", "MPLBACKEND": "Agg"}
            t0 = time.time()
            try:
                p = subprocess.run(self._command(d, [str(HARNESS), mode, cand, pay, out]), cwd=d,
                                   env=env, capture_output=True, text=True, timeout=self.timeout_s,
                                   preexec_fn=self._limits, check=False)
                stderr = p.stderr[-1500:]
            except subprocess.TimeoutExpired:
                stderr = f"timeout after {self.timeout_s}s"
            dt = time.time() - t0
            if os.path.exists(out):
                try:
                    res = json.loads(Path(out).read_text())
                except json.JSONDecodeError:
                    res = {"ok": False, "error": "candidate produced unreadable output"}
            else:
                res = {"ok": False, "error": stderr or "candidate process produced no output"}
        res["seconds"] = round(dt, 3)
        with self._lock:
            self.seconds_used += dt
            self.executions += 1
            self._cache[key] = res
        return res
