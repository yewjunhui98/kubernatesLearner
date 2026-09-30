# Kubernetes on Podman: command list

> Run in PowerShell unless noted.  
> This lab uses `kind` with Podman as the container runtime.

## 1) Prerequisites check

```powershell
podman --version
kind --version
kubectl version --client
```

## 2) Start Podman machine (Windows/macOS)

```powershell
podman machine init
podman machine start
podman info
```

If `podman machine init` says the machine already exists, skip it.

## 3) Create a Kubernetes cluster backed by Podman

```powershell
$env:KIND_EXPERIMENTAL_PROVIDER="podman"
kind create cluster --config .\kind\cluster.yaml
kubectl cluster-info
kubectl get nodes -o wide
```

## 4) Build your app image with Podman

```powershell
podman build -t demo-api:v1 .\app
podman images
```

## 5) Load the image into kind nodes

```powershell
$env:KIND_EXPERIMENTAL_PROVIDER="podman"
kind load docker-image demo-api:v1 --name podman-lab
```

## 6) Deploy core Kubernetes objects

```powershell
kubectl apply -k .\k8s
kubectl get ns
kubectl get all -n podman-lab
kubectl get pods -n podman-lab -w
```

## 7) Access your app with port-forward

```powershell
kubectl port-forward -n podman-lab svc/demo-api 8080:80
```

Open another terminal:

```powershell
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/healthz
```

## 8) Learn core kubectl operations

```powershell
kubectl get deploy,pods,svc -n podman-lab
kubectl describe deploy demo-api -n podman-lab
kubectl logs -n podman-lab deploy/demo-api --tail=50
kubectl exec -it -n podman-lab deploy/demo-api -- /bin/sh
```

## 9) Scale and rollout practice

```powershell
kubectl scale deploy/demo-api --replicas=4 -n podman-lab
kubectl get pods -n podman-lab
kubectl rollout status deploy/demo-api -n podman-lab

kubectl set image deploy/demo-api api=demo-api:v1 -n podman-lab
kubectl rollout history deploy/demo-api -n podman-lab
```

## 10) ConfigMap update practice

```powershell
kubectl edit configmap demo-api-config -n podman-lab
kubectl rollout restart deploy/demo-api -n podman-lab
kubectl logs -n podman-lab deploy/demo-api --tail=20
```

## 11) Batch workloads: Job and CronJob

```powershell
kubectl apply -f .\k8s\04-job.yaml
kubectl get jobs -n podman-lab
kubectl logs job/pi-once -n podman-lab

kubectl apply -f .\k8s\05-cronjob.yaml
kubectl get cronjobs -n podman-lab
kubectl get jobs -n podman-lab --watch
```

## 12) Cleanup

```powershell
kubectl delete ns podman-lab
$env:KIND_EXPERIMENTAL_PROVIDER="podman"
kind delete cluster --name podman-lab
podman machine stop
```
