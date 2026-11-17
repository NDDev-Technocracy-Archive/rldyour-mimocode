set shell := ["bash", "-euo", "pipefail", "-c"]

# Lists the available project commands.
default:
    @just --list

# Installs the unchanged test dependency into the selected Python runtime.
setup:
    python3 -m pip install --user -r .github/requirements-test.txt

# Checks the static source contracts and CI without tests or network access.
check: check-source check-ci

# Applies formatting to the command interface.
fix:
    just --fmt

# Runs the existing pytest behavior suite; the doctor uses a local fake runtime.
test:
    python3 -m pytest -q

# Runs the source checks and existing behavior suite on a prepared executor.
verify: check test

# Runs the original fast-validator sequence, including pytest.
[group('validation')]
validate:
    bash scripts/validate_fast.sh

# Checks all fourteen existing source contracts without runtime or provider execution.
[group('validation')]
check-source:
    just --fmt --check
    PYTHONDONTWRITEBYTECODE=1 bash scripts/validate_fast.sh --skip-tests

# Preserves the runtime baseline and MCP dependency policy checks.
[group('validation')]
check-dependencies:
    python3 -B scripts/validate_mimocode_runtime_baseline.py --strict
    python3 -B scripts/validate_mimocode_mcp_inventory.py --strict

# Checks workflow and shell sources and every available Git commit for secrets.
[group('validation')]
check-ci:
    actionlint
    zizmor --offline --no-progress .github/workflows/validate.yml .github/workflows/cross-platform.yml .github/workflows/dependency-check.yml .github/workflows/pytest.yml .github/workflows/security.yml .github/dependabot.yml
    GIT_NO_LAZY_FETCH=1 gitleaks git --no-banner --redact .

# Runs exactly the existing four Windows behavior modules.
[group('validation')]
test-windows:
    python3 -m pytest -q tests/test_mimocode_config.py tests/test_mimocode_memory_boundary.py tests/test_mimocode_projection.py tests/test_release_assets.py
