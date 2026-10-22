# Appendix — kubeadm, etcd, HA (theory only)

CKA tests **kubeadm** cluster lifecycle. This project stays on **Podman + kind + kubectl** and does **not** require Multipass or extra VMs. Use this checklist to learn the competencies; practice them later on cloud VMs or a dedicated lab if you sit the exam.

## What kind already showed you

On kind, control-plane components run as **static Pods** (see Module 1). That is the same *idea* as kubeadm’s `/etc/kubernetes/manifests` model, but kind bootstraps nodes for you.

## Competencies to know (reading checklist)

### Prepare infrastructure

- [ ] Linux nodes with container runtime, unique hostname, time sync
- [ ] Open required ports (API 6443, etcd, kubelet, etc.)
- [ ] Swap off (classic kubeadm requirement on Linux nodes)

### Create and join with kubeadm

- [ ] `kubeadm init` produces a join command and admin kubeconfig
- [ ] Install a CNI after init (nodes stay NotReady until CNI exists)
- [ ] `kubeadm join` for workers (and extra control-plane nodes with `--control-plane`)

### Cluster lifecycle / upgrade

- [ ] Upgrade order: control plane first, then workers
- [ ] `kubeadm upgrade plan` → `kubeadm upgrade apply`
- [ ] Drain node → upgrade kubelet/kubectl packages → uncordon

### etcd backup and restore

- [ ] Snapshot: `etcdctl snapshot save` (with certs from `/etc/kubernetes/pki/etcd`)
- [ ] Restore: `etcdctl snapshot restore` then point etcd static Pod at restored data
- [ ] Know that etcd holds cluster state; bad restore = wrong cluster

### Highly available control plane

- [ ] Multiple control-plane nodes + stacked or external etcd
- [ ] Load balancer in front of API servers
- [ ] `kubeadm init --control-plane-endpoint`

## Exam tip

On the CKA exam you often get SSH to nodes and run kubeadm/etcdctl directly. kind is excellent for RBAC, workloads, networking objects, and storage — use VMs for muscle memory on kubeadm when you schedule the exam.

## Optional external practice (not part of this repo)

If you later want a disposable VM lab, use any Linux VMs you already have (cloud free tier, local hypervisor). Do **not** install extra tools for *this* project’s graded path.
