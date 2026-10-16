https://github.com/ram133/agentdb/blob/main/agentdb.py
#!/usr/bin/env python3
"""
AgentDB: Lightweight Agent Context & Memory Database
GitHub: https://github.com/ram133/agentdb
"""

import os
import sys
import sqlite3
import json
from datetime import datetime

DB_FILE = "agentdb.sqlite"

def get_connection():
    """Establish a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema for agent state, memory, and logs."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def set_memory(key, value):
    """Store or update a key-value pair in agent memory."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO memory (key, value, updated_at) VALUES (?, ?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
        (key, json.dumps(value) if isinstance(value, (dict, list)) else value, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    print(f"Memory saved: {key}")

def get_memory(key):
    """Retrieve a value from agent memory by key."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM memory WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        val = row["value"]
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return val
    return None

def log_event(level, message):
    """Log an event to the agent database."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (level, message, created_at) VALUES (?, ?, ?)",
        (level.upper(), message, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def main():
    """CLI Entrypoint for AgentDB operations."""
    init_db()
    if len(sys.argv) < 2:
        print("Usage: python agentdb.py [init|set <key> <val>|get <key>|log <level> <msg>]")
        return
    
    command = sys.argv[1].lower()
    if command == "init":
        print("AgentDB initialized successfully.")
    elif command == "set" and len(sys.argv) >= 4:
        set_memory(sys.argv[2], sys.argv[3])
    elif command == "get" and len(sys.argv) >= 3:
        result = get_memory(sys.argv[2])
        print(result)
    elif command == "log" and len(sys.argv) >= 4:
        log_event(sys.argv[2], " ".join(sys.argv[3:]))
        print("Logged event.")
    else:
        print("Invalid command or missing arguments.")

if __name__ == "__main__":
    main()

