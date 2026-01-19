
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

# Create connection pool (ONCE)
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

def get_connection():
    """Get connection from pool"""
    return db_pool.getconn()

def release_connection(conn):
    """Return connection back to pool"""
    db_pool.putconn(conn)

