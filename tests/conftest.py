import os
os.environ["DATABASE_URL"] = "host=localhost port=5432 dbname=taskdb_test user=Admin password=password123"

import psycopg
import pytest

from fastapi.testclient import TestClient
from app.main import app

DB_CONN = os.environ["DATABASE_URL"]

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_tables():
    with psycopg.connect(DB_CONN) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE users, tasks, comments RESTART IDENTITY CASCADE;")
        conn.commit()
    yield