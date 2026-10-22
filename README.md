# Kubernetes Podman Lab (CKA-aligned)

Local Kubernetes learning path using **Podman + kind + kubectl** only (no Docker, Helm CLI, or extra VMs).

## How the stack works (read first)

**Podman** runs containers. **kind** turns some of those containers into Kubernetes nodes. **kubectl** talks to the Kubernetes API from your Mac.

Full explainer: [docs/HOW-THE-STACK-WORKS.md](docs/HOW-THE-STACK-WORKS.md)

## Prerequisites (host only)

```zsh
podman --version
kind --version
kubectl version --client
```

Start the Podman machine on macOS if needed:

```zsh
podman machine start
podman info
```

## Syllabus

Follow [SYLLABUS.md](SYLLABUS.md). Recommended order:

**M0 → M2 → M4 → M3 → M1 → M5 → appendix-kubeadm**

| Module | CKA focus |
|--------|-----------|
| [00 Foundations](labs/00-foundations) | Stack literacy, deploy, scale, Jobs |
| [02 Workloads & Scheduling](labs/02-workloads-scheduling) | 15% — Secrets, DS/STS, scheduling, HPA |
| [04 Storage](labs/04-storage) | 10% — PV/PVC/StorageClass |
| [03 Services & Networking](labs/03-services-networking) | 20% — Services, DNS, NetworkPolicy, Ingress, Gateway |
| [01 Cluster Architecture](labs/01-cluster-architecture) | 25% — control plane, RBAC, Kustomize, CRDs |
| [05 Troubleshooting](labs/05-troubleshooting) | 30% — break/fix drills |
| [Appendix kubeadm](labs/appendix-kubeadm) | Theory: kubeadm / etcd / HA |

Command index: [COMMANDS.md](COMMANDS.md)

## Project layout

```text
app/                  # demo-api (Flask)
kind/                 # kind cluster config
docs/                 # stack explainer
labs/                 # modular CKA labs
SYLLABUS.md
COMMANDS.md
README.md
```

## Quick start (Module 0)

```zsh
export KIND_EXPERIMENTAL_PROVIDER=podman
cd "$(dirname "$0")"   # repo root, if needed

# See labs/00-foundations/COMMANDS.md for the full path
```

## Notes

- Cluster add-ons are installed with `kubectl apply` (manifests in each lab or pinned URLs).
- kind cannot fully simulate kubeadm upgrade / etcd restore / HA — covered as reading in the appendix.
- Delete and recreate the cluster often; that practice is intentional.
