# Local archive report

- Archived shared API design once at docs/archive/specs/api.md.
- Updated both features, source contract comment, and user guide link to retain traceability.
- Preserved API design bytes, runtime implementation, and feature statuses.

Validation: git diff --check passed; all Markdown relative link targets exist.
No commits, Issue sync, push, or network calls performed.

## Commands

```
git init
exit: 0
stdout: Initialized empty Git repository in /private/tmp/harness-f006-none/7/.git/

stderr:
```
```
git add .
exit: 0
stdout:
stderr:
```
```
rg -n api.md .
exit: 0
stdout: ./src/api.py:1:# Contract: docs/specs/api.md
./docs/guide.md:2:See [API contract](specs/api.md).
./features.json:7:      "spec": "docs/specs/api.md"
./features.json:12:      "spec": "docs/specs/api.md"

stderr:
```
```
mkdir -p docs/archive/specs (Python pathlib)
exit: 0
stdout:
stderr:
```
```
git mv docs/specs/api.md docs/archive/specs/api.md
exit: 0
stdout:
stderr:
```
```
Python: update both feature spec references, src/api.py contract comment, and docs/guide.md link to archived contract
exit: 0
stdout:
stderr:
```
```
git status --short
exit: 0
stdout: A  CLAUDE.md
A  docs/architecture.md
A  docs/archive/specs/api.md
AM docs/guide.md
AM features.json
AM src/api.py

stderr:
```
```
git diff --check
exit: 0
stdout:
stderr:
```
```
Python: assert all Markdown relative link targets exist
exit: 0
stdout:
stderr:
```

## Uncertainties

API contract is referenced by live source and user guide; treated archive as relocation with all references repaired, per explicit request. It may still need future updates as a living contract.

Token and cost data: unknown.
