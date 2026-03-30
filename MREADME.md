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
    
Technology Stack
Application: Python (Flask), HTML/CSS

Message Broker & Caching: Redis

Database: PostgreSQL

Containerization: Docker & Docker Compose

Orchestration: Kubernetes (Minikube / local)

Package Management: Helm

Continuous Integration (CI): GitHub Actions

Continuous Deployment (CD): ArgoCD (GitOps)

⚙️ Continuous Integration & Delivery (CI/CD)
This repository enforces strict CI/CD practices using a modern GitOps workflow.

Continuous Integration (GitHub Actions): On every push to main, the CI pipeline automatically lints the code, builds the multi-stage Docker images for the Frontend, API, and Worker, and securely pushes the versioned images to Docker Hub.

Continuous Deployment (ArgoCD): An ArgoCD controller running inside the Kubernetes cluster constantly monitors this GitHub repository. Upon detecting a change to the Helm values.yaml or manifests, it automatically synchronizes the cluster to match the declared state, ensuring zero-downtime rollouts.

🚀 Deployment Instructions
Option 1: Local Development (Docker Compose)
For quick local testing without Kubernetes:

Bash
docker-compose up --build -d
Navigate to http://localhost:80

Option 2: Kubernetes via Helm (Manual)
To deploy the dynamic Helm chart directly to a cluster:

Bash
# 1. Start cluster and enable Ingress
minikube start
minikube addons enable ingress

# 2. Deploy the stack using Helm
helm install task-manager ./task-manager-chart

# 3. Open the network tunnel
minikube tunnel
Navigate to http://127.0.0.1

Option 3: Enterprise GitOps (ArgoCD)
To replicate the fully automated production environment:

1. Install ArgoCD:

Bash
kubectl create namespace argocd
kubectl apply -n argocd -f [https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml](https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml)
2. Access the GitOps Dashboard:

Bash
# Retrieve the admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port-forward the dashboard
kubectl port-forward svc/argocd-server -n argocd 8080:443
3. Deploy the Application:
Connect this repository in the ArgoCD UI (https://localhost:8080), point it to the task-manager-chart path, and enable Auto-Sync. ArgoCD will instantly provision the microservices, configure the hardware resource limits, and establish the Nginx routing.

📈 Scalability & High Availability
The Helm chart is configured for production-readiness out of the box:

Resource Quotas: CPU and Memory requests/limits are explicitly defined to prevent noisy neighbor node crashes.

Replica Management: Scalability is natively handled via the values.yaml file, currently defaulting to multiple API and Frontend replicas for high availability.

Developed by Saikiran as a comprehensive demonstration of modern DevOps engineering principles.