# Module 2 — Commands (zsh)

```zsh
export KIND_EXPERIMENTAL_PROVIDER=podman
ROOT="$(pwd)"   # repo root
NS=workloads-lab
```

## 1) Install metrics-server (for HPA later)

```zsh
kubectl apply -f "${ROOT}/labs/02-workloads-scheduling/manifests/metrics-server.yaml"
kubectl -n kube-system rollout status deploy/metrics-server --timeout=120s
# Wait ~30s then:
kubectl top nodes
kubectl top pods -A | head
```

## 2) Apply core workloads

```zsh
kubectl apply -k "${ROOT}/labs/02-workloads-scheduling/manifests"
kubectl get all -n "$NS"
kubectl get secret demo-secret -n "$NS" -o yaml | head -30
kubectl logs -n "$NS" deploy/secret-demo --tail=20
kubectl exec -n "$NS" deploy/secret-demo -- cat /secrets/config.json
```

## 3) DaemonSet and StatefulSet

```zsh
kubectl get ds node-agent -n "$NS" -o wide
kubectl get pods -n "$NS" -l app=node-agent -o wide
# Expect one agent Pod per Ready node

kubectl get sts web -n "$NS"
kubectl get pods -n "$NS" -l app=web -o wide
kubectl get svc web-headless -n "$NS"
```

## 4) Quotas

```zsh
kubectl describe limitrange defaults -n "$NS"
kubectl describe resourcequota compute-quota -n "$NS"
```

## 5) Scheduling: nodeSelector, taint, toleration, affinity

```zsh
# Place prefer-worker on worker via nodeSelector
kubectl apply -f "${ROOT}/labs/02-workloads-scheduling/manifests/06-scheduling.yaml"
kubectl get pod prefer-worker -n "$NS" -o wide

# Taint worker2, then tolerating Pod should still schedule there
kubectl taint nodes podman-lab-worker2 spot=true:NoSchedule
kubectl get pod tolerates-spot -n "$NS" -o wide
kubectl describe pod tolerates-spot -n "$NS" | grep -A5 Events

# Cleanup taint when done with this section
kubectl taint nodes podman-lab-worker2 spot=true:NoSchedule-
```

## 6) Rollout / rollback on demo-api (Module 0 app)

```zsh
kubectl rollout history deploy/demo-api -n podman-lab
kubectl set image deploy/demo-api api=demo-api:v1 -n podman-lab
kubectl rollout undo deploy/demo-api -n podman-lab
kubectl rollout status deploy/demo-api -n podman-lab
```

## 7) HPA

```zsh
kubectl apply -f "${ROOT}/labs/02-workloads-scheduling/manifests/07-hpa-target.yaml"
kubectl get hpa -n "$NS" -w
# Ctrl+C after you see TARGETS populated (may take a minute)
kubectl describe hpa cpu-load -n "$NS"
```

## 8) Cleanup module namespace (optional)

```zsh
kubectl delete ns workloads-lab
# leave metrics-server if later modules need kubectl top
```
