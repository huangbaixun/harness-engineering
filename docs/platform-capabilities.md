# Platform capability matrix — 2026-10-05 (2.4.0)

| Capability | Claude Code | Codex CLI | App / Cloud |
|---|---|---|---|
| Discovery | Project .claude/skills and compatibility plugin entry; initialization fixtures pass | Project .agents/skills; prior CLI discovery of 19 skills; portable manifest validated locally | Not verified |
| Workflows | Shared skills and preserved upstream bytes; scenario evaluations | Shared skills; prior isolated CLI workflow smoke | Not verified |
| SessionStart | Shared bounded JSON context; protocol fixtures | Shared bounded JSON context; protocol fixtures | Not verified |
| Stop | Real configured argv checks; one feedback request; lifecycle not verified | Same verifier; one feedback request; lifecycle not verified | Not verified |
| Direct-file guard | Read/Edit/Write recognized secret filenames; no shell parsing; native permissions retained | Not registered; native permissions retained | Not claimed |
| Issue sync | Separate opt-in root/legacy features.json configuration preserved | Not registered | Not claimed |
| Progress auto-commit | Retired, unregistered warning stub | Not registered | Not claimed |
| Formatting / telemetry | Empty formatter retired; observe is manually opt-in sanitized event metadata | No default formatter/telemetry | Not claimed |
| Checkpoints | Shared neutral writes; legacy read-only fallback | Same | Requires a local shell |
| Model routing | Host/user selection, no fixed agent aliases | Host/user selection | Not claimed |

Project adoption activates no hooks and changes no settings/permissions. Portable
root plugin.json is canonical; explicit OpenAI hook override replaces default Claude
hook discovery. Compatibility entries are retained. Native trust review cannot be
bypassed. Fixtures establish adapter behavior, not actual trusted lifecycle loading.

Local initialization/regressions require Python 3.10+ standard library and Bash,
no credentials or network. Windows wrappers were checked on the Bash path only;
native Windows execution is not verified. Existing 2.3.0 installs require reviewed
migration; conflict-first initialization does not overwrite existing runtime files.
