import sqlite3
import os
import shutil

DB_NAME = "database.db"
# Vercel-specific: Use /tmp for writable database
if os.environ.get('VERCEL'):
    DB_PATH = os.path.join('/tmp', DB_NAME)
else:
    DB_PATH = DB_NAME

def get_db():
    # If on Vercel and db doesn't exist in /tmp, copy it from project root
    if os.environ.get('VERCEL'):
        if not os.path.exists(DB_PATH):
            # Original DB in project root
            original_db = os.path.join(os.getcwd(), DB_NAME)
            if os.path.exists(original_db):
                shutil.copy2(original_db, DB_PATH)
            else:
                # If no original DB, we let create_tables make a new one in /tmp
                pass
    
    return sqlite3.connect(DB_PATH)

def create_tables():
    db = get_db()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS wardrobe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        formality TEXT,
        season TEXT,
        color TEXT,
        image TEXT,
        worn_count INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        event_type TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        mobile TEXT,
        password TEXT
    )
    """)

    db.commit()
    db.close()
