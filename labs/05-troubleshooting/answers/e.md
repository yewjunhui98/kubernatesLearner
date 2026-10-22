# Scenario E — Wrong ConfigMap key

**Diagnose**

```zsh
kubectl get pods -n trouble-lab -l app=cfg-miss
kubectl describe pod -n trouble-lab -l app=cfg-miss | sed -n '/Events/,$p'
kubectl get cm app-config -n trouble-lab -o yaml
```

**Fix:** point env at key `MESSAGE`

```zsh
kubectl -n trouble-lab set env deploy/cfg-miss --from=configmap/app-config --keys=MESSAGE
# If the bad key remains, edit the Deployment and remove the broken env entry, or:
kubectl -n trouble-lab patch deploy cfg-miss --type='json' -p='[
  {"op":"replace","path":"/spec/template/spec/containers/0/env/0/valueFrom/configMapKeyRef/key","value":"MESSAGE"}
]'
```
