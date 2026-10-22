# Scenario D — Probe failure

**Diagnose**

```zsh
kubectl get pods -n trouble-lab -l app=probe-fail
kubectl describe pod -n trouble-lab -l app=probe-fail | grep -i -A5 'Readiness\|Warning'
```

**Fix:** readiness path `/`

```zsh
kubectl -n trouble-lab patch deploy probe-fail --type='json' -p='[
  {"op":"replace","path":"/spec/template/spec/containers/0/readinessProbe/httpGet/path","value":"/"}
]'
```
