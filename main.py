from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI(title="FinTech Nova - Secure API Practice")

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

def get_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
    cursor.executemany("INSERT INTO users (username, role) VALUES (?, ?)",
        [("admin", "superadmin"), ("juan", "user"), ("maria", "user")])
    conn.commit()
    return conn

@app.get("/vulnerable/users/{username}")
def get_user_vulnerable(username: str):
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return {"query_ejecutada": query, "resultado": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/secure/users/{username}")
def get_user_secure(username: str):
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    return {"query_ejecutada": query, "resultado": result}
