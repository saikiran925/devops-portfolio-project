# ---------- Stage 1 : Builder ----------
FROM python:3.9-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install/deps --no-cache-dir -r requirements.txt


# ---------- Stage 2 : Runtime ----------
FROM python:3.9-slim

WORKDIR /app

# Install curl for container healthcheck
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy installed dependencies
COPY --from=builder /install/deps /usr/local

# Copy application source
COPY . .

# Better logging in containers
ENV PYTHONUNBUFFERED=1

# Run container as non-root user (security best practice)
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]