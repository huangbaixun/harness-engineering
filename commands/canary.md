---
description: Generate a canary deployment runbook with risk assessment, staged rollout plan, rollback triggers, and observability checklists. Outputs to deploy/ directory.
---

# /harness:canary — Canary Deployment Runbook Generator

> Goal: Before any production deployment, generate a risk-scored runbook with staged canary rollout, quantitative rollback triggers, and observability checklists — so the team deploys with confidence instead of hope.

## Usage

```
/harness:canary                     # Auto-detect changes from git diff main...HEAD
/harness:canary feature-name        # Generate runbook for a specific feature
/harness:canary --platform k8s      # Include Kubernetes-specific commands
```

## What It Does

1. **Analyzes the change** — reads git diff, features.json constraints, and architecture.md to understand what's being deployed
2. **Scores risk** — evaluates 5 dimensions (Data, Auth/Security, Payment, Blast radius, Novelty, Reversibility) to produce a quantitative risk score
3. **Generates staged canary plan** — maps risk level to a canary strategy (2-5 stages with traffic percentages and observation windows)
4. **Defines rollback triggers** — sets quantitative thresholds (error rate, latency) that trigger automatic rollback
5. **Outputs runbook** — writes `deploy/runbook-<name>.md` with pre-deploy checklist, canary stages, rollback plan, observability checklist, and post-deploy verification

## When to Use

- After harness:verify passes and before deploying to production
- When preparing a release that includes database migrations
- When deploying changes to auth, payments, or core data paths
- When rolling out to a new environment or region
- Any time you want a structured deployment plan instead of ad-hoc steps

## Output

```
deploy/
  runbook-<feature-or-release-name>.md
```

The runbook is a planning document — it does not execute any deployment commands. The deploying engineer follows it step by step.
