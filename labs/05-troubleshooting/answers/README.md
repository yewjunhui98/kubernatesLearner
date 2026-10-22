# Answer keys (spoilers)

Try each scenario yourself first. Open these only to check.

| Scenario | Symptom | Root cause | Fix |
|----------|---------|------------|-----|
| A | CrashLoopBackOff | Container command exits 1 | Keep process running, e.g. `sleep 3600` |
| B | ImagePullBackOff / ErrImagePull | Bad image tag | Use a real tag, e.g. `nginx:1.27-alpine` |
| C | Service has no Endpoints | selector `app: website` ≠ Pods `app: web` | Set Service selector to `app: web` |
| D | Pod not Ready | readinessProbe path 404 | Probe `/` (or a real path nginx serves) |
| E | CreateContainerConfigError | ConfigMap key `MSG` missing | Use key `MESSAGE` or add `MSG` to CM |

Detailed patches: [a.md](a.md) … [e.md](e.md).
