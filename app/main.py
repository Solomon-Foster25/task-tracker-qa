from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
import psycopg
import os
from psycopg.rows import dict_row
from psycopg import errors

app = FastAPI()

# host port you mapped in docker-compose (5432 if you took my suggestion, 8080 if you kept yours)
DB_CONN = os.environ.get(
    "DATABASE_URL",
    "host=localhost port=5432 dbname=taskdb user=Admin password=password123",
)

@app.get("/health")
def health():
    with psycopg.connect(DB_CONN) as conn:       # open a connection to the container
        with conn.cursor() as cur:               # a cursor runs SQL
            cur.execute("SELECT 1")              # trivial query — just proves the DB answers
            cur.fetchone()
    return {"status": "ok", "database": "connected"}

# create a user

class UserCreate(BaseModel):
    username: str
    email: str
    
@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    try:
        with psycopg.connect(DB_CONN) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, email) "
                    "VALUES (%s, %s) RETURNING id, created_at",
                    (user.username, user.email),
                )
                new_id, created_at = cur.fetchone()
    except errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="username or email already exists")
    return {"id": new_id, "username": user.username, "email": user.email, "created_at": created_at}

# Create a task

class TaskCreate(BaseModel): 
    title: str
    body: str | None = None
    user_id: int
    status: str = "todo"

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    try:
        with psycopg.connect(DB_CONN) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, body, user_id, status) "
                    "VALUES (%s, %s, %s, %s) RETURNING id, created_at",
                    (task.title, task.body, task.user_id, task.status),
                )
                new_id, created_at = cur.fetchone()
    except errors.ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="user_id not found")
    return {"id": new_id, "title": task.title, "body":task.body, "user_id": task.user_id, "status": task.status, "created_at": created_at}

# get a task by ID

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with psycopg.connect(DB_CONN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, body, user_id, status, created_at "
                "FROM tasks WHERE id = %s",
                (task_id,),
            )
            row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": row[0], "title": row[1], "body": row[2],
        "user_id": row[3], "status": row[4], "created_at": row[5],
    }


# list all tasks

@app.get("/tasks")
def list_task():
    with psycopg.connect(DB_CONN,  row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM tasks"
            )
            row = cur.fetchall()
    return row

# update a task status

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task_status: str):
    with psycopg.connect(DB_CONN) as conn: 
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET status = %s WHERE id = %s "
                "RETURNING id, title, status, created_at",
                (task_status, task_id),
            )
            row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="ID not found")
    return {"id": row[0], "title": row[1], "status": row[2], "created_at": row[3]}

# delete a task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with psycopg.connect(DB_CONN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM tasks "
                "WHERE id = %s "
                "RETURNING id",
                (task_id,),
            )
            deleted = cur.fetchone()
            if deleted is None:
                raise HTTPException(status_code=404, detail="Task not found")
