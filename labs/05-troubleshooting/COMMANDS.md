# Module 5 — Commands (zsh)

```zsh
export KIND_EXPERIMENTAL_PROVIDER=podman
ROOT="$(pwd)"
NS=trouble-lab
```

## 1) Warm-up: method on a healthy workload

```zsh
kubectl get ns podman-lab 2>/dev/null || echo "redeploy Module 0 if missing"
kubectl get events -n podman-lab --sort-by=.lastTimestamp | tail -20
kubectl describe deploy demo-api -n podman-lab | sed -n '/Events/,$p'
kubectl logs -n podman-lab deploy/demo-api --tail=30
```

## 2) Node ops: cordon and drain

```zsh
WORKER=$(kubectl get nodes -o name | grep worker | head -1 | cut -d/ -f2)
kubectl cordon "$WORKER"
kubectl drain "$WORKER" --ignore-daemonsets --delete-emptydir-data --force
kubectl get nodes
kubectl get pods -A -o wide | head -40

kubectl uncordon "$WORKER"
kubectl get nodes
```

## 3) Control-plane logs (kind)

```zsh
CP=$(podman ps --format '{{.Names}}' | grep control-plane | head -1)
podman exec "$CP" ls /var/log/containers 2>/dev/null | head
kubectl logs -n kube-system "$(kubectl get pods -n kube-system -o name | grep kube-apiserver | head -1)" --tail=50
```

## 4) Scenarios (break / fix)

Apply each broken manifest, diagnose, fix. Answers are in `answers/` — use only after you try.

```zsh
kubectl create ns "$NS" --dry-run=client -o yaml | kubectl apply -f -

# Scenario A — CrashLoopBackOff
kubectl apply -f "${ROOT}/labs/05-troubleshooting/scenarios/a-crashloop.yaml"
# fix, then:
kubectl get pods -n "$NS"

# Scenario B — ImagePullBackOff
kubectl apply -f "${ROOT}/labs/05-troubleshooting/scenarios/b-imagepull.yaml"

# Scenario C — Service selector mismatch
kubectl apply -f "${ROOT}/labs/05-troubleshooting/scenarios/c-service-selector.yaml"

# Scenario D — Probe failure
kubectl apply -f "${ROOT}/labs/05-troubleshooting/scenarios/d-bad-probe.yaml"

# Scenario E — Wrong ConfigMap key
kubectl apply -f "${ROOT}/labs/05-troubleshooting/scenarios/e-bad-configmap.yaml"
```

## 5) Cleanup

```zsh
kubectl delete ns trouble-lab
```
