# Module 5 — Troubleshooting (CKA 30%)

**Goals:** a repeatable debug method; fix broken apps, Services, and node/ops issues.

## Method (memorize)

1. **Events** — `kubectl get events --sort-by=.lastTimestamp`
2. **Describe** — Pod / Deployment / Service / Node
3. **Logs** — current + `--previous` for crashes
4. **Exec** — only if the container runs
5. **Components** — kube-system Pods, static Pod logs on control-plane
6. **Network path** — DNS → Service → Endpoints → NetworkPolicy

## Success criteria

- [ ] Fix all scenarios in `scenarios/` without opening `answers/` first
- [ ] Practice cordon/drain and recover
- [ ] Read a control-plane component log from the kind node

## Lab

Follow [COMMANDS.md](COMMANDS.md), then work scenarios.
