# Kubernetes Deployment Guide

This directory contains Kubernetes manifests for deploying the asynchronous task manager system.

---

## 📦 Resources

* api-deployment.yaml
* api-service.yaml
* worker-deployment.yaml
* postgres-deployment.yaml
* postgres-service.yaml
* redis-deployment.yaml
* redis-service.yaml

---

## 🚀 Deploy All Components

```bash
kubectl apply -f .
```

---

## 🔍 Verify Deployment

```bash
kubectl get pods
kubectl get svc
```

---

## 🌐 Access API

### Port Forward (Recommended)

```bash
kubectl port-forward service/api-service 8000:5000
```

Open:

```text
http://localhost:8000
```

---

## 🧪 Debugging Commands

### Describe Pod

```bash
kubectl describe pod <pod-name>
```

### View Logs

```bash
kubectl logs <pod-name>
```

### Access Container

```bash
kubectl exec -it <pod-name> -- sh
```

---

## ⚠️ Notes

* Kubernetes uses **Service names as DNS**

  * postgres
  * redis

* API depends on:

  * PostgreSQL
  * Redis

---
### ☁️ Cloud Deployment (AWS EKS) Note
These manifests are currently configured for local execution using Minikube and the Nginx Ingress Controller. 

To deploy this architecture to a managed cloud provider like Amazon EKS, simply update the `ingress.yaml` file to provision a cloud load balancer:
1. Change `ingressClassName: nginx` to your cloud provider's controller (e.g., `alb`).
2. Add the required Load Balancer annotations (e.g., `alb.ingress.kubernetes.io/scheme: internet-facing`).
