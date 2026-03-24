# Asynchronous Task Manager

This project demonstrates an event-driven microservices architecture for processing background tasks asynchronously.

When a task is submitted through the API, it is pushed to a Redis message queue. A background worker consumes the task from the queue, processes it, and stores the final state in a PostgreSQL database.

The frontend provides a simple UI to submit and track tasks.

---

## Architecture Components

* **API Server** – Accepts incoming tasks and publishes them to Redis
* **Worker Service** – Listens to Redis queue and processes tasks
* **Redis** – Message broker for asynchronous communication
* **PostgreSQL** – Persistent storage for task status
* **Frontend** – Static UI to submit and view tasks

---

## Prerequisites

* Python **3.9+**
* Docker
* pip

---

## Running the Application Locally

This setup requires **three terminals**.

---

### Step 1 – Start Supporting Services (Redis & PostgreSQL)

Run temporary containers for Redis and PostgreSQL.

```bash
# Start Redis
docker run --name temp-redis -p 6379:6379 -d redis:alpine

# Start PostgreSQL (mapped to port 5433 to avoid conflicts)
docker run --name temp-postgres \
-e POSTGRES_USER=myuser \
-e POSTGRES_PASSWORD=mypassword \
-e POSTGRES_DB=taskdb \
-p 5433:5432 \
-d postgres:alpine
```

---

### Step 2 – Start the API Server

Open a new terminal:

```bash
cd app-source/api-server
pip install -r requirements.txt
```

#### Linux / Mac

```bash
export DB_PORT=5433
python app.py
```

#### Windows (Git Bash)

```bash
export DB_PORT=5433
python app.py
```

#### Windows (Command Prompt)

```bash
set DB_PORT=5433
python app.py
```

---

### Step 3 – Start the Worker Service

Open another terminal:

```bash
cd app-source/worker
pip install -r requirements.txt
```

#### Linux / Mac

```bash
export DB_PORT=5433
python worker.py
```

#### Windows (Command Prompt)

```bash
set DB_PORT=5433
python worker.py
```

---

### Step 4 – Open the Frontend

Navigate to:

```
app-source/frontend/
```

Open `index.html` in your browser.

You can now submit tasks and observe asynchronous processing via Redis and the background worker.

---

## Stopping the Supporting Containers

```bash
docker stop temp-redis temp-postgres
docker rm temp-redis temp-postgres
```
