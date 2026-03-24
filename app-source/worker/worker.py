import os
import time
import redis
import psycopg2

cache = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5433'), # <-- Added the port here too
        database=os.getenv('DB_NAME', 'taskdb'),
        user=os.getenv('DB_USER', 'myuser'),
        password=os.getenv('DB_PASS', 'mypassword')
    )

print("Worker started. Listening for tasks...")

while True:
    # Pull from queue
    _, message = cache.brpop('task_queue')
    
    # Message looks like "15|Learn Kubernetes"
    task_id, task_name = message.decode('utf-8').split('|', 1)
    
    print(f"[{time.strftime('%X')}] Processing Task {task_id}: {task_name}")
    time.sleep(3) # Simulate heavy work
    
    # Update Database to 'Completed'
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE tasks SET status = %s WHERE id = %s", ('Completed', task_id))
        conn.commit()
        
    print(f"[{time.strftime('%X')}] Successfully completed Task {task_id}")