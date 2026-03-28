import os
import time
import redis
import psycopg2

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "taskdb")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASS = os.getenv("DB_PASS", "mypassword")


def wait_for_redis():
    while True:
        try:
            r = redis.Redis(host=REDIS_HOST, port=6379)
            r.ping()
            print("Connected to Redis")
            return r
        except Exception:
            print("Waiting for Redis...")
            time.sleep(2)


def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            print("Connected to PostgreSQL")
            return conn
        except Exception:
            print("Waiting for PostgreSQL...")
            time.sleep(2)


cache = wait_for_redis()

print("Worker started. Listening for tasks...")

while True:
    _, message = cache.brpop("task_queue")

    task_id, task_name = message.decode("utf-8").split("|", 1)

    print(f"[{time.strftime('%X')}] Processing Task {task_id}: {task_name}")
    time.sleep(3)

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE tasks SET status = %s WHERE id = %s",
            ("Completed", task_id),
        )
        conn.commit()
    conn.close()

    print(f"[{time.strftime('%X')}] Successfully completed Task {task_id}")