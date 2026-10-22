# Scenario A — CrashLoopBackOff

**Diagnose**

```zsh
kubectl get pods -n trouble-lab
kubectl describe pod -n trouble-lab -l app=crashy
kubectl logs -n trouble-lab -l app=crashy --previous
```

**Fix:** change command to stay alive:

```zsh
kubectl -n trouble-lab set command deploy/crashy -- /bin/sh -c -- 'sleep 3600'
# or edit the Deployment YAML command and re-apply
```
