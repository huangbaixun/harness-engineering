# Hook contracts (2.4.0)

Use native host documentation for event schemas and trust:
- Claude: https://code.claude.com/docs/en/hooks
- OpenAI: https://developers.openai.com/plugins/build/plugins

Hooks are supplemental control points. Their existence does not prove checks run,
intercept git commit, satisfy acceptance criteria or secure arbitrary shell access.
CI, pre-commit and explicit verified commands may enforce the relevant rule better.

## Current registration

Claude hooks/hooks.json: SessionStart, real Stop verification, separately opt-in
Issue synchronization, direct-file Read/Edit/Write guard. No progress auto-commit,
empty formatter or telemetry default. Codex selects hooks/codex.json explicitly via
root plugin.json extensions.com.openai, preserving native hook trust.

Project adoption alone registers none of these and changes no permissions.
SessionStart returns bounded state in additionalContext, not full router instructions
or an unconditional full-test itinerary. It prefers neutral progress and supports
legacy reads. Claude's separate enabled Issue pull preserves root/legacy location
precedence. No enabled configuration means no sync call.

## Verification

Configure .harness/config.json verification_commands as nonempty argv arrays.
Shared harness_runtime.py verify executes without shell parsing, propagates failures,
and suppresses successful/noisy command output. Run failed commands explicitly for
diagnostics. Empty or invalid configuration is not success. Stop uses native JSON
blocking feedback once; stop_hook_active avoids loops without certifying completion.

Explicit commits remain user/workflow operations after reviewing the index. The
retired stop-commit-progress compatibility entry only warns and changes nothing.
Do not use --no-verify or commit unrelated staged files through a lifecycle hook.

## Direct-path guard and observability

claude_hook.py protect parses native stdin and validates recognized direct-file
paths including resolved aliases. It allows non-secret example env fixtures. It
does not parse Bash, support every tool, or replace sandbox/native permissions.
Malformed direct events fail visibly without echoing raw input; jq is unnecessary.

Optional observe requires telemetry_enabled:true and explicit registration/invocation.
It reads native event metadata, omits raw inputs/outputs/session identifiers, and
writes .harness/telemetry.jsonl. Unknown duration/tokens/cost remain null. Native host
observability is the source for real usage measurements.

## Validation limits

Offline fixtures cover protocol, error propagation, staged-state preservation,
legacy precedence, path spaces and opt-in isolation. Live trust/lifecycle and native
Windows execution require their own evidence. Missing Git Bash is a visible failure,
not a passed check; Bash compatibility wrappers preserve JSON protocol output.
