from fastapi import FastAPI, Request
import sqlite3
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import status

app = FastAPI()

def create_logs_table():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user TEXT,
        action TEXT
    )
    """)
    conn.commit()
    conn.close()

create_logs_table()

@app.post("/log/")
async def log_action(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON"}, status_code=status.HTTP_400_BAD_REQUEST)
    user = data.get("user")
    action = data.get("action")
    if not user or not action:
        return JSONResponse(content={"error": "'user' and 'action' fields are required"}, status_code=status.HTTP_400_BAD_REQUEST)
    timestamp = datetime.now().isoformat()
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (timestamp, user, action) VALUES (?, ?, ?)",
                   (timestamp, user, action))
    conn.commit()
    conn.close()
    return {"status": "ok"} 