# CKA-aligned syllabus

Learning-first path mapped to the Certified Kubernetes Administrator (CKA) domains. Host toolchain: **Podman + kind + kubectl** only.

Read [docs/HOW-THE-STACK-WORKS.md](docs/HOW-THE-STACK-WORKS.md) before Module 0.

## Recommended order

**M0 → M2 → M4 → M3 → M1 → M5 → appendix-kubeadm (read-only)**

| Module | Folder | CKA domain | Weight |
|--------|--------|------------|--------|
| 0 Foundations | [labs/00-foundations](labs/00-foundations) | Prerequisites + kubectl fluency | — |
| 2 Workloads & Scheduling | [labs/02-workloads-scheduling](labs/02-workloads-scheduling) | Workloads & Scheduling | 15% |
| 4 Storage | [labs/04-storage](labs/04-storage) | Storage | 10% |
| 3 Services & Networking | [labs/03-services-networking](labs/03-services-networking) | Services & Networking | 20% |
| 1 Cluster Architecture | [labs/01-cluster-architecture](labs/01-cluster-architecture) | Cluster Architecture, Installation & Configuration | 25% |
| 5 Troubleshooting | [labs/05-troubleshooting](labs/05-troubleshooting) | Troubleshooting | 30% |
| Appendix | [labs/appendix-kubeadm](labs/appendix-kubeadm) | kubeadm / etcd / HA (theory) | part of 25% |

## Competency checklist

### Stack literacy (before CKA domains)

- [ ] Explain Podman vs kind vs kubectl (three layers)
- [ ] Interpret `podman ps` vs `kubectl get nodes`
- [ ] Build an image with Podman and load it into kind

### Cluster Architecture, Installation & Configuration (25%)

- [ ] Inspect control-plane static Pods and component logs on kind
- [ ] Manage RBAC (ServiceAccount, Role/ClusterRole, bindings)
- [ ] Use Kustomize overlays to install/configure components
- [ ] Describe CRI / CNI / CSI at a high level
- [ ] Apply a CRD and manage a custom resource
- [ ] (Theory) kubeadm init/join, upgrade, etcd snapshot/restore, HA — see appendix

### Workloads & Scheduling (15%)

- [ ] Deployments: rolling update and rollback
- [ ] ConfigMaps and Secrets (env + volume)
- [ ] DaemonSet and StatefulSet
- [ ] Requests/limits, LimitRange, ResourceQuota
- [ ] Scheduling: nodeSelector, affinity, taints/tolerations
- [ ] HPA with metrics-server
- [ ] Probes and self-healing primitives

### Services & Networking (20%)

- [ ] ClusterIP, NodePort, EndpointSlices
- [ ] CoreDNS debugging from an in-cluster Pod
- [ ] NetworkPolicy (default-deny + allow)
- [ ] Ingress controller + Ingress
- [ ] Gateway API basics

### Storage (10%)

- [ ] emptyDir / hostPath (demo)
- [ ] PV, PVC, access modes, reclaim policies
- [ ] StorageClass + dynamic provisioning (local-path)

### Troubleshooting (30%)

- [ ] Use a systematic method: events → describe → logs → exec → components → network
- [ ] Fix CrashLoopBackOff, ImagePullBackOff, probe failures
- [ ] Fix Service selector / DNS / NetworkPolicy issues
- [ ] Practice cordon/drain and read control-plane logs
- [ ] Complete Module 5 scenarios without the answer key

## Kind limits (honest)

Hands-on labs cover almost all object-level admin work. **kubeadm install/upgrade, etcd backup/restore, and HA bootstrap** are theory-only in [labs/appendix-kubeadm](labs/appendix-kubeadm) — they need real VMs, which this project deliberately does not require.

## CKA habits (use in every module)

```zsh
kubectl explain deployment.spec.strategy
kubectl create deployment demo --image=nginx --dry-run=client -o yaml
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
```
