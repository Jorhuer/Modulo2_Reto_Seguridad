import asyncio
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import create_access_token, verify_token, authenticate_user
from db import init_db, get_last_for_device
from mqtt_client import run_mqtt, broadcaster

app = FastAPI(title="SmartCity MQTT API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    init_db()
    loop = asyncio.get_event_loop()
    loop.create_task(run_mqtt())

@app.post("/api/auth/login")
async def login(payload: dict):
    username = payload.get("username")
    password = payload.get("password")
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/iot/data/{device_id}")
async def get_device(device_id: str, token=Depends(verify_token)):
    return get_last_for_device(device_id)

@app.websocket("/ws/telemetry")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    await broadcaster.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except Exception:
        broadcaster.disconnect(ws)
