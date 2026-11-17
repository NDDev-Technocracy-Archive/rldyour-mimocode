# AGENTS.md - rldyour-mimocode

rldyour AI CLI configuration for MiMoCode: native .mimocode config, build/plan/compose agents, persistent memory projection, commands, skills, MCP, browser routing, and runtime validation.
This is the MiMoCode adapter package for the rldyour AI CLI control plane.
It owns MiMoCode-native project configuration under `.mimocode/`, runtime
validation rules, and command/agent/skill projection.

## Source of Truth

- `config/mimocode-baseline.json`
- `.mimocode/mimocode.jsonc`
- `.mimocode/command/*.md`
- `.mimocode/agent/*.md`
- `.mimocode/skills/*/SKILL.md`
- `scripts/*.sh`, `scripts/*.py`
- `config/rldyour-contract.json`

## Native Boundaries

Use MiMoCode-native surfaces only:

- `.mimocode/`
- `mimocode` binary config layout and command handlers
- runtime validation scripts in this repo

Do not introduce Claude/Antigravity/Codex native config formats as runtime controls.

## Runtime Baseline

- MiMoCode runtime version is `0.1.5` (from `config/mimocode-baseline.json`).
- `curl` installer path and optional npm secondary channel are validated via
  dedicated runtime checks.

## Validation Commands

```bash
just check
just test
just verify
```

## Browser Boundary

- Run exact `$HOME/.local/bin/cloakbrowser-cdp-health` before every browser
  action; missing or nonzero health stops as `NOT_PROVEN`.
- Execute only exact `$HOME/.local/bin/playwright-cli` or the exact managed
  Chrome DevTools MCP transport in `.mimocode/mimocode.jsonc`.
- `webwright-task` is compatibility intent routed through `browser-review`.
  Webwright runtime execution, built-in/raw browser surfaces, direct packages,
  alternate CDP/executables/configs, and fallbacks are forbidden.

## Security Policy

- Secrets, API tokens, and local browser artifacts are never committed.
- Keep `.serena/` durable state updated while runtime artifacts stay gitignored.
- Any permission model change requires accompanying validation evidence.

## CI runner selection

Every workflow run is evidence and must finish. Use a concurrency group unique
to `github.run_id` and `cancel-in-progress: false`; never discard a queued or
running check as superseded.

A reusable workflow retains its own concurrency settings; an outer caller group
does not override them. A shared caller change must preserve the complete
run-id-unique/no-cancel contract. Fork jobs use public hosted workers only.

The shared job lifecycle prepares the environment and records the result; Just
owns the project commands. Tests put a fake `mimo` first on their child PATH and
clear shell startup injection. Installed-runtime doctor and browser/MCP/model
qualification remain separate operator actions.
