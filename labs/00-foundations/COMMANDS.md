# Module 0 — Commands (zsh)

Run from the **repository root** unless noted.

```zsh
export KIND_EXPERIMENTAL_PROVIDER=podman
ROOT="$(pwd)"   # should be the repo root containing app/, kind/, labs/
```

## 1) Prerequisites

```zsh
podman --version
kind --version
kubectl version --client
```

## 2) Start Podman machine (macOS)

```zsh
podman machine start
podman info
```

If the machine does not exist yet: `podman machine init` then `podman machine start`.

## 3) Create the kind cluster

```zsh
kind create cluster --config "${ROOT}/kind/cluster.yaml"
```

## 4) See the three layers (do this before deploying)

```zsh
podman machine list
# Layer 2 — VM

podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
# Layer 2 — kind node containers

kind get clusters
# Layer 1 — kind inventory

kubectl get nodes -o wide
kubectl cluster-info
# Layer 3 — Kubernetes view / API endpoint
```

Write one sentence per command: which layer?

## 5) Build and load the app image

```zsh
podman build -t demo-api:v1 "${ROOT}/app"
podman images | head
kind load docker-image demo-api:v1 --name podman-lab
```

## 6) Deploy core objects

```zsh
kubectl apply -k "${ROOT}/labs/00-foundations/manifests"
kubectl get ns
kubectl get all -n podman-lab
kubectl get pods -n podman-lab -w
# Ctrl+C when Ready
```

## 7) Access with port-forward

Terminal A:

```zsh
kubectl port-forward -n podman-lab svc/demo-api 8080:80
```

Terminal B:

```zsh
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/healthz
```

## 8) Core kubectl + CKA habits

```zsh
kubectl get deploy,pods,svc -n podman-lab
kubectl describe deploy demo-api -n podman-lab
kubectl logs -n podman-lab deploy/demo-api --tail=50
kubectl exec -it -n podman-lab deploy/demo-api -- /bin/sh
# inside: exit

kubectl explain deployment.spec.replicas
kubectl get pods -n podman-lab -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
kubectl create deployment scratch --image=nginx --dry-run=client -o yaml | head -20
```

## 9) Scale and rollout

```zsh
kubectl scale deploy/demo-api --replicas=4 -n podman-lab
kubectl rollout status deploy/demo-api -n podman-lab
kubectl set image deploy/demo-api api=demo-api:v1 -n podman-lab
kubectl rollout history deploy/demo-api -n podman-lab
```

## 10) ConfigMap change

```zsh
kubectl edit configmap demo-api-config -n podman-lab
# change POD_NOTE, save
kubectl rollout restart deploy/demo-api -n podman-lab
kubectl logs -n podman-lab deploy/demo-api --tail=20
```

## 11) Job and CronJob

```zsh
kubectl apply -f "${ROOT}/labs/00-foundations/manifests/04-job.yaml"
kubectl get jobs -n podman-lab
kubectl logs job/pi-once -n podman-lab

kubectl apply -f "${ROOT}/labs/00-foundations/manifests/05-cronjob.yaml"
kubectl get cronjobs -n podman-lab
kubectl get jobs -n podman-lab
```

## 12) Cleanup (optional)

```zsh
kubectl delete ns podman-lab
kind delete cluster --name podman-lab
podman machine stop
```

Keep the cluster if you are continuing to Module 2.
