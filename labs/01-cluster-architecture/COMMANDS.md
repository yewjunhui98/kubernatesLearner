# Module 1 — Commands (zsh)

```zsh
export KIND_EXPERIMENTAL_PROVIDER=podman
ROOT="$(pwd)"
```

## 1) Control-plane anatomy (Layer 3 inside the control-plane node)

```zsh
kubectl get nodes -o wide
kubectl get pods -n kube-system -o wide

# Static Pods typically named kube-apiserver-*, etcd-*, kube-scheduler-*, kube-controller-manager-*
kubectl get pods -n kube-system | grep -E 'apiserver|etcd|scheduler|controller-manager'

kubectl logs -n kube-system -l component=kube-apiserver --tail=30 2>/dev/null || \
  kubectl logs -n kube-system "$(kubectl get pods -n kube-system -o name | grep kube-apiserver | head -1)" --tail=30

# Optional: peek at static Pod manifests inside the kind node container
CONTROL_PLANE=$(podman ps --format '{{.Names}}' | grep control-plane | head -1)
podman exec "$CONTROL_PLANE" ls /etc/kubernetes/manifests
```

## 2) Extension interfaces (observe)

```zsh
# CRI: runtime on nodes (containerd inside kind nodes)
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.containerRuntimeVersion}{"\n"}{end}'

# CNI: Pod network add-ons in kube-system (kindnet or calico)
kubectl get ds,deploy -n kube-system

# CSI: StorageClasses / CSIDrivers if present
kubectl get storageclass
kubectl get csidrivers 2>/dev/null || echo "no CSIDriver objects yet"
```

## 3) RBAC least privilege

```zsh
kubectl apply -f "${ROOT}/labs/01-cluster-architecture/manifests/rbac/sa-role.yaml"
kubectl wait --for=condition=Ready pod/reader-pod -n rbac-lab --timeout=120s

# Should succeed
kubectl exec -n rbac-lab reader-pod -- kubectl get pods -n rbac-lab

# Should fail (no permission to list secrets)
kubectl exec -n rbac-lab reader-pod -- kubectl get secrets -n rbac-lab || echo "denied as expected"

kubectl auth can-i get pods -n rbac-lab --as=system:serviceaccount:rbac-lab:app-reader
kubectl auth can-i get secrets -n rbac-lab --as=system:serviceaccount:rbac-lab:app-reader
```

## 4) Kustomize overlay (no Helm)

```zsh
kubectl apply -k "${ROOT}/labs/01-cluster-architecture/manifests/overlays/staging"
kubectl get deploy -n rbac-lab -l env=staging
kubectl get pods -n rbac-lab -l env=staging
```

## 5) CRD + custom resource

```zsh
kubectl apply -f "${ROOT}/labs/01-cluster-architecture/manifests/crd/widget-crd.yaml"
kubectl get crd widgets.demo.cka.local
kubectl apply -f "${ROOT}/labs/01-cluster-architecture/manifests/crd/widget-sample.yaml"
kubectl get widgets -n rbac-lab
kubectl get wd blue-box -n rbac-lab -o yaml
```

## 6) Cleanup

```zsh
kubectl delete ns rbac-lab
kubectl delete crd widgets.demo.cka.local
```

Next: read [../appendix-kubeadm/README.md](../appendix-kubeadm/README.md) for kubeadm/etcd/HA theory.
