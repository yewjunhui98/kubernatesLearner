# How Podman, kind, and kubectl work together

Required reading before any lab. Goal: you can name which layer each command touches.

## One-sentence mental model

**Podman runs containers. kind turns some of those containers into Kubernetes nodes. kubectl is your remote control for the Kubernetes API — it never needs to live inside Podman.**

## Three layers

```text
Layer 1 — Host CLIs (on your Mac)
  podman | kind | kubectl

Layer 2 — Podman machine (Linux VM) + kind node containers
  podman-lab-control-plane | podman-lab-worker | podman-lab-worker2

Layer 3 — Kubernetes inside those nodes
  kube-apiserver, Pods, Deployments, Services, ...
```

| Layer | Tools / things | Runs where | Job |
|-------|----------------|------------|-----|
| 1 | `podman`, `kind`, `kubectl` | Your Mac | You type commands here |
| 2 | Podman machine + kind **node** containers | Linux VM under Podman | Fake cluster “computers” |
| 3 | API server, Pods, Services, … | Inside those node containers | Real Kubernetes |

## Who talks to whom

- **You → `podman`:** start the machine, build images (`podman build`), list containers (`podman ps`).
- **You → `kind`:** create/delete the cluster, load images into nodes. With `KIND_EXPERIMENTAL_PROVIDER=podman`, kind calls the Podman API to create/start/stop node containers.
- **You → `kubectl`:** apply YAML, get Pods, scale Deployments. kubectl reads `~/.kube/config` (written by kind when the cluster is created) and speaks HTTPS to the API server. **Day-to-day kubectl does not go through kind.**

## Lifecycle of this lab

1. `podman machine start` — boot the Linux VM where containers can run (required on macOS).
2. `kind create cluster --config kind/cluster.yaml` — kind asks Podman to run 1 control-plane + 2 worker **containers**, installs Kubernetes inside them, writes kubeconfig.
3. `podman build -t demo-api:v1 ./app` — build an image in Podman’s store (not yet in the cluster).
4. `kind load docker-image demo-api:v1` — copy that image into the kind node containers so kubelet can run it. (Command name says “docker-image”; Podman is the backend when the env var is set.)
5. `kubectl apply -k ...` — kubectl → API server → schedule Pods onto worker nodes.
6. Compare views:
   - `podman ps` — container runtime view of the **nodes**
   - `kubectl get nodes` — Kubernetes view of those same nodes

## Common confusions

| Confusion | Clear answer |
|-----------|--------------|
| “Is kubectl a container?” | No. Host CLI. |
| “Is kind a container?” | No. Host CLI. It *creates* containers. |
| “Where is my cluster?” | Inside Podman: containers named like `podman-lab-control-plane`. |
| “Why both `podman ps` and `kubectl get nodes`?” | Runtime view vs Kubernetes view of the same nodes. |
| “Do I need Docker?” | No. Podman is kind’s provider here. |
| “Is Podman machine the same as a kind node?” | No. Machine = VM that hosts containers. Nodes = containers *inside* that VM. |

## Hands-on verify (after cluster create)

Run these and write one sentence for each output naming the layer:

```zsh
export KIND_EXPERIMENTAL_PROVIDER=podman

podman machine list
# Layer 2 (VM): is the Podman machine running?

podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
# Layer 2 (containers): kind node containers

kind get clusters
# Layer 1 inventory: clusters kind knows about

kubectl get nodes -o wide
# Layer 3: Kubernetes nodes (same machines as the containers above)

kubectl cluster-info
# Layer 3: API server endpoint kubectl is talking to
```

**Success criteria:** you can point at each command’s output and say Layer 1, 2, or 3.

## Host tools only

This project uses **Podman + kind + kubectl** on the host. Cluster add-ons are installed with `kubectl apply`, not new host installers. Docker, Helm CLI, and extra VMs are not required.
