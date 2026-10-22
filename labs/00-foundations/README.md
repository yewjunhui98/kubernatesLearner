# Module 0 — Foundations

**Goals:** explain the Podman/kind/kubectl stack; deploy demo-api; practice scale, rollouts, Jobs.

## Prerequisites

- Read [docs/HOW-THE-STACK-WORKS.md](../../docs/HOW-THE-STACK-WORKS.md)
- Host tools: `podman`, `kind`, `kubectl`

## Success criteria

- [ ] Name Layer 1/2/3 for `podman ps`, `kind get clusters`, and `kubectl get nodes`
- [ ] App responds on port-forward (`/` and `/healthz`)
- [ ] You can scale, restart after ConfigMap edit, and run a Job/CronJob

## Lab

Follow [COMMANDS.md](COMMANDS.md) from top to bottom.
