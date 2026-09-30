# Kubernetes Podman Lab

This is a minimal Kubernetes learning project that runs locally with **Podman + kind** (no Docker needed).

## What you will learn

- Build a container image with Podman.
- Create a local Kubernetes cluster with kind using Podman runtime.
- Deploy an app with Deployment + Service + ConfigMap.
- Observe Pods, logs, probes, scaling, and rollouts.
- Run a one-off Job and a scheduled CronJob.

## Project structure

```text
k8s-podman-lab/
  app/
    Containerfile
    requirements.txt
    server.py
  kind/
    cluster.yaml
  k8s/
    00-namespace.yaml
    01-configmap.yaml
    02-deployment.yaml
    03-service.yaml
    04-job.yaml
    05-cronjob.yaml
    kustomization.yaml
  COMMANDS.md
  README.md
```

## Quick start

1. Follow `COMMANDS.md` from top to bottom.
2. Keep one terminal for `kubectl port-forward` and use another terminal for `curl`.
3. Change the ConfigMap value and restart the deployment to see live config behavior.

## Notes

- This lab is intentionally small so you can understand each resource quickly.
- You can delete and recreate the cluster repeatedly to practice.
