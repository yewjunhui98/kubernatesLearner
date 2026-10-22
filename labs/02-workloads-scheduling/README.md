# Module 2 — Workloads & Scheduling (CKA 15%)

**Goals:** Secrets, DaemonSet, StatefulSet, resources/quotas, scheduling controls, rollouts, HPA.

Assumes Module 0 cluster exists (`podman-lab`) and `demo-api:v1` is loaded.

## Success criteria

- [ ] Mount a Secret as env and as a volume
- [ ] Run a DaemonSet (one Pod per node) and a StatefulSet with stable identity
- [ ] Apply LimitRange / ResourceQuota and see admission effects
- [ ] Place a Pod with nodeSelector / taint+toleration
- [ ] Perform rollout undo; see HPA react after metrics-server is up

## Lab

Follow [COMMANDS.md](COMMANDS.md).
