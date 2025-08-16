Sumanth9040660
# RollDice App - Kubernetes Deployment

This project demonstrates deploying a simple Node.js app (`RollDice`) to Kubernetes using a Docker container and YAML manifest.

---

## Tech Stack

- Node.js 18 (Alpine)
- Docker
- Kubernetes (kubectl, minikube/Docker Desktop)
- YAML manifests (Deployment + Service)

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/SumanthReddyKConestoga/Monitoringloggingtask4.git


## Repository layout

```
ansible/
  group_vars/all.yml
  inventory.ini
  templates/override-values.yaml.j2
  up.yml
  down.yml
k8s/
  rolldice/
    namespace.yaml
    deployment.yaml
    service.yaml
rolldice-app/
  app.py
  Dockerfile
  requirements.txt
up.yaml
down.yml
rolldice.yaml
```

---

## Prerequisites

* Docker (Desktop on Windows/macOS; engine on Linux)
* Kubernetes CLI: `kubectl`
* A cluster (Minikube / Docker Desktop / k3s / real k8s)
* Python 3.10+ (only needed for local run or Ansible)
* **Optional:** Ansible 2.15+ and `helm` (if using the playbooks)

---

## 1) Local build & run (Docker)

```bash
# From repo root
docker build -t rolldice:local ./rolldice-app
docker run -p 5000:5000 --name rolldice rolldice:local
```

Open: `http://localhost:5000`

Useful one-liners:

```bash
docker logs -f rolldice
docker rm -f rolldice
```

---

## 2) Kubernetes deployment (manifests)

### Minikube quick start

```bash
minikube start
kubectl get nodes
```

### Apply manifests

```bash
# Namespace + app
kubectl apply -f k8s/rolldice/namespace.yaml
kubectl apply -f k8s/rolldice/deployment.yaml
kubectl apply -f k8s/rolldice/service.yaml

# Wait until the deployment is ready
kubectl rollout status -n rolldice deploy/rolldice
kubectl get all -n rolldice
```

### Access the service

* If `service.yaml` is **NodePort**:

  ```bash
  minikube service -n rolldice rolldice
  ```
* Or port-forward:

  ```bash
  kubectl -n rolldice port-forward svc/rolldice 8080:80
  # Then open http://localhost:8080
  ```

---

## 3) Orchestration with **Ansible** (optional)

Update the variables to match your environment:

* `ansible/group_vars/all.yml` — common vars (namespace, image, ports, etc.)
* `ansible/inventory.ini` — targets (for local: `127.0.0.1 ansible_connection=local`)

Run:

```bash
# Bring up (provision namespace, apply manifests/values, etc.)
ansible-playbook -i ansible/inventory.ini ansible/up.yml

# Tear down
ansible-playbook -i ansible/inventory.ini ansible/down.yml
```

> If your playbooks template Helm/K8s values via `templates/override-values.yaml.j2`, ensure `helm` is installed and your `all.yml` contains the expected keys.

---

## 4) Image management (when using a private registry)

Tag and push to your registry, then reference it in `k8s/rolldice/deployment.yaml` (or your Ansible vars):

```bash
# Example: Docker Hub
docker tag rolldice:local your-dockerhub-username/rolldice:1.0.0
docker push your-dockerhub-username/rolldice:1.0.0
# Update the Deployment image: your-dockerhub-username/rolldice:1.0.0
kubectl -n rolldice set image deploy/rolldice rolldice=your-dockerhub-username/rolldice:1.0.0
```

---

## 5) Validation & Ops

```bash
# Health
kubectl get pods -n rolldice
kubectl describe pod -n rolldice -l app=rolldice
kubectl logs -f -n rolldice -l app=rolldice

# Service discovery
kubectl get svc -n rolldice
kubectl get endpoints -n rolldice rolldice
```

---

## 6) Troubleshooting

* **ImagePullBackOff / ErrImagePull**
  Image name/tag in `deployment.yaml` doesn’t exist or registry needs auth.

  ```bash
  kubectl -n rolldice describe pod <pod>
  docker login
  docker push <correct-image>
  kubectl -n rolldice set image deploy/rolldice rolldice=<correct-image>
  ```

* **Service not reachable**
  Use port-forward to validate the Pod first:

  ```bash
  kubectl -n rolldice port-forward deploy/rolldice 8080:5000
  curl http://localhost:8080
  ```

* **Windows path issues**
  Prefer forward slashes in `kubectl apply -f` paths or run from repo root.

* **Large binaries in Git**
  Keep tools like `minikube*` out via `.gitignore`. Don’t commit >100MB files.

---

## 7) Clean up

```bash
kubectl delete ns rolldice
# or:
kubectl delete -f k8s/rolldice/service.yaml
kubectl delete -f k8s/rolldice/deployment.yaml
kubectl delete -f k8s/rolldice/namespace.yaml
```

---

## Tech Stack

* **App:** Python (Flask-style minimal service)
* **Container:** Docker
* **Orchestration:** Kubernetes (manifests), optional **Ansible** automation
* **Templating:** Jinja2 for values (via Ansible templates)

---

## Maintainer

**Sumanth Reddy K** — [@SumanthReddyKConestoga](https://github.com/SumanthReddyKConestoga)

---
