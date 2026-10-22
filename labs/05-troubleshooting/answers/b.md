# Scenario B — ImagePullBackOff

**Diagnose**

```zsh
kubectl describe pod -n trouble-lab -l app=bad-image | sed -n '/Events/,$p'
```

**Fix**

```zsh
kubectl -n trouble-lab set image deploy/bad-image app=nginx:1.27-alpine
```
