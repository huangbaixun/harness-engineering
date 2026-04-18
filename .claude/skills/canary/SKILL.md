# harness:canary — Pre-Deployment Canary Planning

> Generate a structured deployment runbook with risk-based canary stages, rollback triggers, and observability checklists.
> Core principle: The gap between "code verified" and "safely in production" is where most incidents originate. A structured runbook closes that gap.

## When to Use

Under any of the following circumstances, execute this workflow **before deploying to production**:

| Circumstance | Example |
|------|------|
| Feature passed harness:verify, ready to ship | "Let's deploy this to production" |
| Preparing a release with database migrations | "We have schema changes, need a deploy plan" |
| Deploying to a new environment or region | "Rolling out to EU region" |
| Any change touching auth, payments, or core data paths | "The auth rewrite is ready to go live" |
| Team wants a deployment checklist | "Write a deploy runbook", "How should we roll this out" |

Decision rule: **If the change affects production users or infrastructure, a canary plan is recommended. If it involves database migrations, auth, or payment paths, it is mandatory.**

## Canary Planning Workflow

### Step 1: Gather Change Context

Collect information from three sources:

**1a. Git diff analysis**
```bash
# Compare against the deployment base (main or last release tag)
git diff main...HEAD --stat
git diff main...HEAD --name-only
git log main...HEAD --oneline
```

Extract:
- Total files changed, lines added/removed
- Which directories and modules are affected
- Whether migrations, config files, or environment variables changed

**1b. Constraint check (if features.json exists)**
```bash
cat docs/features.json
```

Identify which features are being deployed and their constraint types:
- `rigid` constraints (acceptance_criteria, forbidden_patterns) — these map to mandatory verification steps in the runbook
- `dependencies` — confirm all are satisfied before deployment

**1c. Architecture impact (if docs/architecture.md exists)**
```bash
cat docs/architecture.md
```

Identify which layers/services are affected and their downstream consumers.

### Step 2: Risk Assessment

Score the deployment across five dimensions. Each dimension adds to the total risk score:

| Dimension | Condition | Score |
|-----------|-----------|-------|
| **Data** | Database schema migration (ALTER TABLE, new index, column change) | +3 |
| **Data** | Data backfill or bulk update | +2 |
| **Auth/Security** | Changes to authentication, authorization, or encryption | +3 |
| **Payment/Financial** | Changes to payment processing, billing, or financial calculations | +3 |
| **Blast radius** | Changes span 3+ services or modules | +2 |
| **Blast radius** | Changes span 10+ files | +1 |
| **Novelty** | New service, new external dependency, or new infrastructure component | +2 |
| **Novelty** | First deployment to this environment/region | +2 |
| **Reversibility** | Includes irreversible migration (DROP COLUMN, data format change) | +3 |
| **Reversibility** | Feature flag not available for quick disable | +1 |

**Risk level mapping:**

| Total Score | Level | Canary Strategy |
|-------------|-------|-----------------|
| 0-2 | **Low** | 2-stage: 50% -> 100% |
| 3-5 | **Medium** | 3-stage: 10% -> 50% -> 100% |
| 6-8 | **High** | 4-stage: 1% -> 10% -> 50% -> 100% |
| 9+ | **Critical** | 5-stage: 1% -> 5% -> 25% -> 50% -> 100% |

### Step 3: Generate Runbook

Output the runbook to `deploy/runbook-<feature-or-release-name>.md` using the following structure:

```markdown
# Deployment Runbook: [Feature/Release Name]

> Generated: [DATE]
> Risk level: [Low/Medium/High/Critical] (score: N)
> Author: harness:canary

## 1. Pre-Deploy Checklist

- [ ] All CI checks passing on the deployment branch
- [ ] harness:verify completed (4-layer check passed)
- [ ] Environment variables confirmed for target environment
  - [ ] [List any new env vars introduced in this change]
- [ ] Database migration reviewed and tested against staging data
  - [ ] Migration is backward-compatible (old code can run against new schema)
  - [ ] Rollback migration exists and has been tested
- [ ] Feature flags configured (if applicable)
  - [ ] [List flags and their initial state]
- [ ] On-call engineer identified and available: _______________
- [ ] Rollback procedure reviewed by deploying engineer

## 2. Risk Assessment

| Dimension | Finding | Score |
|-----------|---------|-------|
| Data | [specific finding] | +N |
| Auth/Security | [specific finding] | +N |
| ... | ... | ... |
| **Total** | | **N** |

Risk level: [Level] — [one-line justification]

## 3. Canary Stages

### Stage 1: [X]% traffic
- **Duration**: [observation window]
- **Deploy command**: [platform-specific or manual steps]
- **Monitor**:
  - [ ] Error rate < [threshold]% (baseline: [current]%)
  - [ ] p99 latency < [threshold]ms (baseline: [current]ms)
  - [ ] No new error types in logs
- **Proceed criteria**: All monitors green for full duration
- **Rollback trigger**: Any monitor breached -> immediate rollback

### Stage 2: [Y]% traffic
[same structure]

### Stage N: 100% traffic (full rollout)
- **Duration**: 30 min observation after full rollout
- **Monitor**: Same as above + business metrics
  - [ ] [Business-specific metric] within normal range
- **Stabilization**: Keep previous version available for 24h after full rollout

## 4. Rollback Plan

**Automated rollback triggers** (any ONE triggers immediate rollback):
- Error rate exceeds [X]% (2x baseline)
- p99 latency exceeds [X]ms (3x baseline)
- Any 5xx spike > [N] errors/minute
- [Feature-specific condition]

**Rollback procedure**:
1. [Platform-specific rollback command or manual steps]
2. Verify rollback: confirm previous version is serving traffic
3. Notify team in [channel]: "Rollback executed for [feature], investigating"
4. Create incident ticket if rollback was triggered by monitor breach

**Database rollback** (if applicable):
- [ ] Rollback migration: [migration name/path]
- [ ] Data backfill reversal: [procedure or N/A]
- ⚠️ If migration is irreversible, document the forward-fix strategy instead

## 5. Observability Checklist

Dashboards to watch during deployment:
- [ ] [Primary dashboard URL/name] — overall service health
- [ ] [Database dashboard] — query latency, connection pool, slow queries
- [ ] [Business metrics dashboard] — conversion, signup, core flows

Alerts that should be active:
- [ ] [Alert name] — [what it monitors]
- [ ] [Alert name] — [what it monitors]

Log queries to have ready:
- [ ] `[query for new error types]`
- [ ] `[query for the specific feature's log lines]`

## 6. Post-Deploy Verification

After reaching 100% and observation window passes:
- [ ] Smoke test: [list key user flows to manually verify]
- [ ] Verify rigid constraints from features.json are met in production
- [ ] Confirm monitoring baselines have stabilized at new normal
- [ ] Update deployment log / changelog
- [ ] Notify stakeholders: "[Feature] successfully deployed to production"
- [ ] Schedule: remove feature flag after [N] days (if applicable)
```

### Step 4: Platform-Specific Appendix

If the user specifies a deployment platform, append a platform-specific section.

**Generic (no platform specified)**:
- Use placeholder commands: `[deploy command]`, `[rollback command]`
- Focus on the process and decision framework

**Kubernetes**:
```markdown
## Appendix: Kubernetes Commands

### Canary deployment
```bash
# Stage 1: Deploy canary with reduced replicas
kubectl set image deployment/<app> <container>=<image>:<tag> -n <namespace>
kubectl scale deployment/<app>-canary --replicas=1 -n <namespace>

# Monitor canary pods
kubectl get pods -l app=<app>,track=canary -n <namespace> -w
kubectl logs -l app=<app>,track=canary -n <namespace> --tail=100 -f
```

### Traffic splitting (Istio/Linkerd)
```bash
# Adjust canary weight (example: Istio VirtualService)
kubectl patch virtualservice <app> -n <namespace> --type merge -p '
spec:
  http:
  - route:
    - destination:
        host: <app>
        subset: stable
      weight: 90
    - destination:
        host: <app>
        subset: canary
      weight: 10
'
```

### Rollback
```bash
kubectl rollout undo deployment/<app> -n <namespace>
kubectl rollout status deployment/<app> -n <namespace>
```

### Health checks
```bash
kubectl get events -n <namespace> --sort-by=.lastTimestamp | tail -20
kubectl top pods -l app=<app> -n <namespace>
```
```

### Step 5: Human Confirmation Gate

**After generating the runbook, present a summary and wait for user confirmation.**

```
Deployment runbook generated: deploy/runbook-<name>.md

Risk: [Level] (score: N)
  - [Top risk factor]
  - [Second risk factor if applicable]

Canary strategy: [N]-stage ([percentages])
Estimated total deployment time: [sum of observation windows]

Key items requiring your input:
  - [ ] On-call engineer name
  - [ ] Dashboard URLs (if not auto-detected)
  - [ ] Platform-specific deploy commands (if generic)

Review the runbook and confirm before proceeding with deployment.
```

Do not initiate any deployment. The runbook is a planning artifact, not an execution trigger.

## Integration with Harness Workflow

| Upstream | This Skill | Downstream |
|----------|-----------|------------|
| harness:verify (code quality confirmed) | **harness:canary** (deploy plan) | Manual deployment execution |
| harness:plan (rigid constraints) | Risk assessment uses rigid constraints | harness:archive (post-deploy cleanup) |

## Runbook Quality Checklist

A good runbook satisfies:
- [ ] Risk score is computed with explicit reasoning for each dimension
- [ ] Canary stages match the risk level (not over- or under-cautious)
- [ ] Every stage has quantitative monitor thresholds, not vague "check if things look ok"
- [ ] Rollback triggers are automated conditions, not "team decides"
- [ ] Rollback procedure is specific enough to execute under pressure (no ambiguity)
- [ ] Observability section references real dashboards/alerts (or marks them as TBD for user to fill)
- [ ] Post-deploy verification covers both technical health and business metrics
- [ ] Feature-specific risks are called out (not just generic checklist items)

## Anti-pattern Reminders

| Anti-pattern | Reason | Correct approach |
|--------|------|---------|
| Skipping canary for "small changes" | Small changes cause a disproportionate share of incidents | Risk-score the change; even Low risk gets a 2-stage canary |
| Observation windows < 10 minutes | Latent issues (memory leaks, connection pool exhaustion) take time to surface | Minimum 15 min per stage, 30 min for High/Critical |
| "We can always rollback" without testing | Rollback procedures that haven't been tested often fail when needed | Rollback migration must be tested on staging before deploy |
| Deploying on Friday afternoon | Reduced team availability for incident response | Prefer early-week deployments; flag Friday deploys as +1 risk |
| No feature flag for new user-facing features | No way to disable without full rollback | Recommend feature flags for any user-visible change |
