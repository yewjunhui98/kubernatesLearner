# Module 3 — Services & Networking (CKA 20%)

**Goals:** Service types, DNS, NetworkPolicy, Ingress, Gateway API basics.

## Important

- **Ingress** works on the default `kind/cluster.yaml` (ports 8081/8443 mapped).
- **NetworkPolicy** needs a policy-capable CNI. Use [`kind/cluster-netpol.yaml`](../../kind/cluster-netpol.yaml) + Calico (kubectl apply URL). Recreate the cluster for that section, then reload `demo-api:v1` if needed.

## Success criteria

- [ ] Explain ClusterIP vs NodePort and show EndpointSlices
- [ ] Resolve a Service DNS name from a debug Pod
- [ ] Enforce default-deny + allow NetworkPolicy
- [ ] Route HTTP via Ingress
- [ ] Apply Gateway API CRDs and a sample Gateway/HTTPRoute (controller via kubectl)

## Lab

Follow [COMMANDS.md](COMMANDS.md).
