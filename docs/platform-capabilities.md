# Platform capability matrix — 2026-10-05

| Capability | Claude Code | Codex CLI 0.158.0 | Codex App / Cloud |
|---|---|---|---|
| Skill discovery | Existing plugin manifest retained; structural regressions | 19 project skills discovered by app-server | Not verified |
| Planning/TDD/verify/archive | Existing behavior retained; 9 shell regressions | Actual isolated CLI execution + explicit local verification | Not verified |
| SessionStart | Existing hooks unchanged | Separate JSON adapter; protocol fixtures pass | Not verified |
| Stop verification | Existing hooks unchanged | Separate opt-in adapter; failure block once; native trust required | Not verified |
| PreTool protection | Existing Claude registration | Not registered; native permissions are the boundary | Not claimed |
| Issue sync / auto-commit | Existing opt-in behavior retained | Not registered; new project defaults disabled | Not claimed |
| Commands and named agents | Claude-specific | References only; map actual host tools/model choice | Not verified |
| Runtime checkpoints | Legacy claude-progress | Neutral harness-progress, read-only legacy fallback | Manual script requires local shell |

Installing project skills does not register hooks. Plugin hooks must be reviewed through the host's native trust flow; automated hook lifecycle execution is not claimed from fixture tests. All project initialization and regression checks are offline and require no third-party Python packages or credentials.
