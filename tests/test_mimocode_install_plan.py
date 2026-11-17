from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_install_plan_is_json_event_and_does_not_require_runtime() -> None:
    proc = subprocess.run(
        ["bash", "scripts/install_system_mimocode.sh", "--plan"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    event = json.loads(proc.stdout)
    assert event["event"] == "mimocode-install-plan"
    assert event["mode"] == "plan"


@pytest.mark.parametrize("matches_baseline", [True, False])
def test_doctor_reports_the_fake_runtime_without_probing_an_installed_provider(
    tmp_path: Path, matches_baseline: bool
) -> None:
    baseline = json.loads((ROOT / "config/mimocode-baseline.json").read_text())
    version = baseline["target_runtime_version"] if matches_baseline else "0.0.0"
    binary = tmp_path / "mimo"
    trace = tmp_path / "arguments.txt"
    binary.write_text(
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > "
        + shlex.quote(str(trace))
        + "\nprintf '%s\\n' "
        + shlex.quote(f"mimo {version} token=fixture-value")
        + "\n"
    )
    binary.chmod(0o755)
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"BASH_ENV", "ENV"}
    }
    environment["PATH"] = str(tmp_path) + os.pathsep + environment.get("PATH", "")
    proc = subprocess.run(
        ["bash", "scripts/doctor_system_mimocode.sh", "--redact"],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    event = json.loads(proc.stdout)
    assert event["status"] == ("OK" if matches_baseline else "NOT_PROVEN")
    assert event["runtime"] == "mimocode"
    assert "fixture-value" not in event["version"]
    assert trace.read_text().splitlines() == ["--version"]
