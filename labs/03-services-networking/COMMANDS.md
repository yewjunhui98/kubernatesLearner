# Module 3 — Commands (zsh)

```zsh
export KIND_EXPERIMENTAL_PROVIDER=podman
ROOT="$(pwd)"
NS=net-lab
```

## A) Services and DNS (default kind cluster is fine)

```zsh
kubectl apply -f "${ROOT}/labs/03-services-networking/manifests/00-namespace.yaml"
kubectl apply -f "${ROOT}/labs/03-services-networking/manifests/01-services.yaml"
kubectl get svc,endpointslices -n "$NS"
kubectl get pods -n "$NS" -o wide

# DNS from an in-cluster debug Pod
kubectl run dnscheck -n "$NS" --rm -it --restart=Never --image=busybox:1.36 -- \
  nslookup echo-clusterip.net-lab.svc.cluster.local

kubectl run curlcheck -n "$NS" --rm -it --restart=Never --image=busybox:1.36 -- \
  wget -qO- http://echo-clusterip.net-lab.svc.cluster.local/hostname
```

## B) Ingress (ingress-nginx for kind)

```zsh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.3/deploy/static/provider/kind/deploy.yaml
kubectl -n ingress-nginx rollout status deploy/ingress-nginx-controller --timeout=180s

kubectl apply -f "${ROOT}/labs/03-services-networking/manifests/03-ingress.yaml"
kubectl get ingress -n "$NS"

# Host port 8081 maps to node :80 (see kind/cluster.yaml)
curl -H "Host: echo.localtest.me" http://127.0.0.1:8081/
```

## C) Gateway API (CRDs + nginx gateway fabric via kubectl)

```zsh
# CRDs
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

# Experimental nginx Gateway controller for kind (kubectl only; no Helm)
kubectl apply -f https://github.com/nginxinc/nginx-gateway-fabric/releases/download/v1.5.0/crds.yaml
kubectl apply -f https://github.com/nginxinc/nginx-gateway-fabric/releases/download/v1.5.0/nginx-gateway.yaml

kubectl get gatewayclass
kubectl apply -f "${ROOT}/labs/03-services-networking/manifests/04-gateway.yaml"
kubectl get gateway,httproute -n "$NS"
```

If `gatewayClassName: nginx` is not ready, run `kubectl get gatewayclass -o yaml` and adjust the Gateway manifest to match an available class, or treat CRDs + object definitions as the learning goal for this lab.

## D) NetworkPolicy (recreate cluster with Calico)

```zsh
# Save work / note: this deletes the cluster
kind delete cluster --name podman-lab
kind create cluster --config "${ROOT}/kind/cluster-netpol.yaml"

# Install Calico CNI (pinned URL; needs network once)
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.2/manifests/calico.yaml
kubectl wait --for=condition=Ready nodes --all --timeout=180s

# Reload app image if you still need demo-api
podman build -t demo-api:v1 "${ROOT}/app"
kind load docker-image demo-api:v1 --name podman-lab

# Redeploy echo services + policies
kubectl apply -f "${ROOT}/labs/03-services-networking/manifests/00-namespace.yaml"
kubectl apply -f "${ROOT}/labs/03-services-networking/manifests/01-services.yaml"
kubectl apply -f "${ROOT}/labs/03-services-networking/manifests/02-networkpolicy.yaml"

kubectl wait --for=condition=Ready pod -l app=echo -n "$NS" --timeout=120s

# Allowed client should succeed
kubectl exec -n "$NS" client-allowed -- wget -qO- --timeout=3 http://echo-clusterip/hostname

# Denied client should time out / fail
kubectl exec -n "$NS" client-denied -- wget -qO- --timeout=3 http://echo-clusterip/hostname || echo "blocked as expected"
```

To return to the simpler CNI later:

```zsh
kind delete cluster --name podman-lab
kind create cluster --config "${ROOT}/kind/cluster.yaml"
```

## Cleanup

```zsh
kubectl delete ns net-lab
```
