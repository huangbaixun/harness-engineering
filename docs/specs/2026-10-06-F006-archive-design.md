# F006: Shared and living archive artifacts

## Intent and evidence

The user chose reliable long-task completion by a single developer as the project
focus and approved F006 as the first trial. F004/F005 closeout needed manual
exceptions for a shared design and a design consumed by released code. F008 added
an advisory keep rule but did not define classification or reference repair.

## Outcome

Archive only eligible completed artifacts. Keep shared specs until all referring
features are done, and keep living contracts afterward. Completed execution plans
can move when historical links are repaired. Report concrete inbound references,
unknowns and link repairs so a later session can understand the decision.

## Constraints

Preserve feature ownership, unrelated working-tree changes and existing metadata.
No historical F001–F003 cleanup, Issue calls, commits, push, deployment or global
configuration. No upstream skill edits. Stable rules remain in the skill; fixture
state and evaluation evidence remain outside it. Dependency direction remains
references → templates → skills → commands; hooks remain standalone and silent on
success; template placeholders use {{PLACEHOLDER}}.

## Proof

Run identical disposable repositories with updated skill, old skill and no skill.
Inspect file states as well as reports. Bind results to the source revision and
skill digest; tokens/cost/native-host evidence remain unknown unless measured.
An acceptance evidence table maps the four F006 criteria to the evaluated cases.
This trial does not establish cross-session recovery or long-task performance.
