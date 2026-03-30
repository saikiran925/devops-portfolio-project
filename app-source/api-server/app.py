import os
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to Redis & Postgres
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5433'), # <-- We explicitly added the port here
        database=os.getenv('DB_NAME', 'taskdb'),
        user=os.getenv('DB_USER', 'myuser'),
        password=os.getenv('DB_PASS', 'mypassword')
    )


# Create table on startup
with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                task_name VARCHAR(255) NOT NULL,
                status VARCHAR(50) NOT NULL
            )
        """)
    conn.commit()

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM tasks ORDER BY id DESC")
            tasks = cur.fetchall()
    return jsonify(tasks)

@app.route('/api/task', methods=['POST'])
def create_task():
    data = request.json
    task_name = data.get('task')
    
    if not task_name:
        return jsonify({"error": "Task name required"}), 400
        
    # 1. Save to Database as 'Queued'
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tasks (task_name, status) VALUES (%s, %s) RETURNING id", (task_name, 'Queued'))
            task_id = cur.fetchone()[0]
        conn.commit()

    # 2. Push the ID and Name to Redis
    cache.lpush('task_queue', f"{task_id}|{task_name}")
    
    return jsonify({"status": "Task saved and queued!", "task": task_name}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# ==========================================
# INTENTIONAL SABOTAGE TO TEST CI PIPELINE
# ==========================================
def break_the_pipeline()
    print(this_variable_does_not_exist)
    return "This will never run"