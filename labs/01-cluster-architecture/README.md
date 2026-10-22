# Module 1 — Cluster Architecture, Installation & Configuration (CKA 25%)

**Goals:** control-plane anatomy on kind, RBAC, Kustomize overlays, extension interfaces, CRDs.

**Note:** kubeadm install/upgrade/etcd/HA are theory-only — see [../appendix-kubeadm](../appendix-kubeadm). This lab does not use Helm CLI; components are installed with kubectl/Kustomize (exam may still use Helm).

## Success criteria

- [ ] List control-plane static Pods and read an apiserver/etcd-related log path
- [ ] Create a least-privilege Role + RoleBinding for a ServiceAccount
- [ ] Apply a Kustomize overlay that changes replicas/labels
- [ ] Apply a CRD and create a custom resource
- [ ] Name CRI / CNI / CSI in one sentence each

## Lab

Follow [COMMANDS.md](COMMANDS.md).
