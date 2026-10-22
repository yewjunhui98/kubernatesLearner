# Scenario C — Service selector mismatch

**Diagnose**

```zsh
kubectl get pods -n trouble-lab -l app=web --show-labels
kubectl get endpoints web -n trouble-lab
kubectl get svc web -n trouble-lab -o yaml | grep -A2 selector
```

**Fix:** patch selector to `app: web`

```zsh
kubectl -n trouble-lab patch svc web -p '{"spec":{"selector":{"app":"web"}}}'
kubectl get endpoints web -n trouble-lab
```
