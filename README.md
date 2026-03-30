# Asynchronous Task Manager – DevOps Portfolio Project

This project demonstrates an event-driven microservices architecture where tasks are processed asynchronously using Redis, a background worker, and PostgreSQL.

## Project Structure

* `app-source/` – Application source code (API, Worker, Frontend)
* `k8s-manifests/` – Kubernetes deployment files

## Run Application Locally (Without Dockerizing Services)

See:

```
app-source/RUN-LOCALLY.md
```

## /////////////////

Markdown
# Asynchronous Task Manager – DevOps Portfolio Project

## 📌 Overview
This project demonstrates a complete, cloud-native DevOps workflow by building, containerizing, and deploying an event-driven microservices architecture. 

Users can submit tasks via a web UI. The API routes these tasks to a Redis message queue, where a background worker processes them asynchronously before saving the final state to a PostgreSQL database.

## 🏗️ Architecture Flow
`User` ➡️ `Ingress Controller` ➡️ `Frontend UI & Python API` ➡️ `Redis Queue` ➡️ `Worker` ➡️ `PostgreSQL`

## 🚀 Tech Stack
* **Backend:** Python (Flask)
* **Frontend:** HTML / Vanilla JavaScript
* **Message Broker:** Redis
* **Database:** PostgreSQL
* **Containerization:** Docker (Multi-stage builds)
* **Orchestration:** Kubernetes (Minikube / Amazon EKS)
* **Traffic Routing:** Nginx Ingress / AWS Application Load Balancer (ALB)
* **CI/CD:** GitHub Actions

---

## 🐳 Run Locally (Docker Compose)
To test the raw containers without Kubernetes orchestration, you can spin up the entire stack using Docker Compose:

docker compose up --build
Navigate to http://localhost:80 in your browser.

## ☸️ Kubernetes Deployment
The core infrastructure is fully decoupled and secured. All backend services (Database, Redis, Worker, API) communicate strictly over internal ClusterIP networks, with a single Ingress Controller managing external traffic.

1. Deploy the Cluster
Apply all declarative manifests from the root directory:

Bash
kubectl apply -f k8s-manifests/
2. Verify Services
Ensure all pods and the Ingress resource are running:

Bash
kubectl get pods
kubectl get ingress
🌐 Accessing the Application
This project is designed to be highly portable. The access method depends on whether you are running this in a local test environment or a production cloud environment.

## Environment A: Local Testing (Minikube)
When running on a local Minikube cluster, the project uses the Nginx Ingress Controller.

Enable the local Nginx Ingress addon:

Bash
minikube addons enable ingress
Open a network tunnel to expose the Ingress to your host machine:

Bash
minikube tunnel
Open your browser and navigate to: http://127.0.0.1

### Environment B: Production Cloud (AWS EKS)
When migrating to Amazon EKS, the core deployment manifests remain exactly the same. Only the Ingress resource needs to be updated to provision a cloud-native Load Balancer.

Ensure the AWS Load Balancer Controller is installed on your EKS cluster.

Update the k8s-manifests/ingress.yaml file to use the AWS ALB:

Change ingressClassName: nginx to ingressClassName: alb.

Add the required internet-facing annotations:
Add the required internet-facing annotations:

YAML
annotations:
  alb.ingress.kubernetes.io/scheme: internet-facing
  alb.ingress.kubernetes.io/target-type: ip
  

Apply the updated Ingress file. AWS will automatically provision a public Load Balancer URL to access the application.

(Note: Never use the rewrite-target annotation for this specific path-based routing setup, as it will strip the /api prefix required by the backend).

### 🔄 CI/CD Pipeline (GitHub Actions)
This project includes an automated Continuous Integration pipeline triggered on every push to the main branch.

Workflow Stages:

Lints and tests the application code.

Builds optimized multi-stage Docker images.

Authenticates and pushes versioned images to Docker Hub.

Required Repository Secrets:

DOCKER_USERNAME

DOCKER_PASSWORD

📌 DevOps Highlights
Advanced Traffic Management: Implemented path-based routing using Ingress Controllers.

Network Security: Strict internal ClusterIP isolation for databases and message brokers.

Container Optimization: Reduced image vulnerabilities and sizes using multi-stage Docker builds.

Observability: Configured readiness probes, health checks, and utilized kubectl for system debugging.

Environment Portability: Seamless transition from local Minikube to AWS EKS.

📈 Future Improvements
Implement Kubernetes ConfigMaps & Secrets for secure environment variable management.

Provision Persistent Volumes (PV/PVC) to prevent PostgreSQL data loss during pod restarts.

Introduce Horizontal Pod Autoscaling (HPA) to scale worker nodes based on Redis queue length.

Utilize Terraform (IaC) to automate the provisioning of the AWS EKS cluster.

Author: Saikiran


# 🚀 Enterprise Cloud-Native Task Management Platform

![Architecture: Microservices](https://img.shields.io/badge/Architecture-Microservices-blue)
![Orchestration: Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?logo=kubernetes&logoColor=white)
![Package Manager: Helm](https://img.shields.io/badge/Package_Manager-Helm-0F1689?logo=helm&logoColor=white)
![GitOps: ArgoCD](https://img.shields.io/badge/GitOps-ArgoCD-EF7B4D?logo=argo&logoColor=white)
![CI/CD: GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)

A fully automated, event-driven microservices application designed to showcase a complete, production-grade DevOps lifecycle. This project demonstrates expertise in containerization, Kubernetes orchestration, dynamic Helm templating, and pull-based GitOps continuous deployment.

---

## 🏗️ System Architecture

The application is fully decoupled, routed through an Nginx Ingress Controller, and utilizes an asynchronous message-passing architecture to process background tasks.

```mermaid
graph TD
    Client([👤 User Browser]) -->|HTTP/80| Ingress[🌐 Nginx Ingress Controller]
    
    subgraph Kubernetes Cluster [Kubernetes Cluster]
        Ingress -->|Routes to /| Frontend[🖥️ Frontend Pods <br> Python/Flask]
        Frontend -->|Internal DNS: 5000| API[⚙️ API Pods <br> Python/Flask]
        
        API -->|Queues Task| Redis[(🟥 Redis Broker)]
        Redis -->|Pulls Task| Worker[👷 Worker Pods <br> Python]
        
        Worker -->|Saves State| DB[(🐘 PostgreSQL Database)]
    end