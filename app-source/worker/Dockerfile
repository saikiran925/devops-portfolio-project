# ---------- Stage 1 : Builder ----------

FROM python:3.9-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install/deps --no-cache-dir -r requirements.txt

# ---------- Stage 2 : Runtime ----------

FROM python:3.9-slim

WORKDIR /app

# Copy installed dependencies

COPY --from=builder /install/deps /usr/local

# Copy application source

COPY . .

# Better logging behaviour in containers

ENV PYTHONUNBUFFERED=1

# (Optional but very good security practice)

RUN useradd -m appuser
USER appuser

CMD ["python", "worker.py"]
