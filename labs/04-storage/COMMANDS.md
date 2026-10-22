# Module 4 — Commands (zsh)

```zsh
export KIND_EXPERIMENTAL_PROVIDER=podman
ROOT="$(pwd)"
NS=storage-lab
```

## 1) Install local-path provisioner

```zsh
kubectl apply -f "${ROOT}/labs/04-storage/manifests/local-path-provisioner.yaml"
kubectl -n local-path-storage rollout status deploy/local-path-provisioner --timeout=120s
kubectl get storageclass
```

## 2) emptyDir and hostPath

```zsh
kubectl apply -f "${ROOT}/labs/04-storage/manifests/00-namespace.yaml"
kubectl apply -f "${ROOT}/labs/04-storage/manifests/01-emptydir-hostpath.yaml"
kubectl exec -n "$NS" emptydir-demo -- cat /cache/note.txt
kubectl exec -n "$NS" hostpath-demo -- cat /data/note.txt
# Delete emptydir Pod and recreate — file is gone. hostPath persists on that node.
```

## 3) Dynamic PVC

```zsh
kubectl apply -f "${ROOT}/labs/04-storage/manifests/02-pvc-pod.yaml"
kubectl get pvc,pv -n "$NS"
kubectl wait --for=condition=Ready pod/pvc-writer -n "$NS" --timeout=120s
kubectl exec -n "$NS" pvc-writer -- cat /mnt/data/log.txt
kubectl describe pvc demo-pvc -n "$NS"
```

## 4) StatefulSet volumeClaimTemplates

```zsh
kubectl apply -f "${ROOT}/labs/04-storage/manifests/03-statefulset-pvc.yaml"
kubectl get sts,pods,pvc -n "$NS"
kubectl exec -n "$NS" db-0 -- cat /data/id.txt
kubectl exec -n "$NS" db-1 -- cat /data/id.txt
```

## 5) Reclaim / cleanup notes

```zsh
kubectl delete pod pvc-writer -n "$NS"
# PVC still exists; recreate writer Pod to see data survive Pod delete
kubectl apply -f "${ROOT}/labs/04-storage/manifests/02-pvc-pod.yaml"
kubectl wait --for=condition=Ready pod/pvc-writer -n "$NS" --timeout=120s
kubectl exec -n "$NS" pvc-writer -- cat /mnt/data/log.txt

# Full cleanup
kubectl delete ns storage-lab
# optional: kubectl delete -f .../local-path-provisioner.yaml
```
