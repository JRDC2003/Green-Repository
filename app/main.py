from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app import db
from app import models
import asyncio
import httpx


app = FastAPI(title="Green Repository API")


@app.on_event("startup")
def startup_event():
    db.init_db()


@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/devices/register", status_code=201)
async def register_device(dev: models.DeviceIn):
    db.register_device(dev.name, dev.ip)
    return {"status": "registered"}


@app.get("/devices", response_model=list[models.DeviceOut])
async def list_devices():
    devices = db.get_all_devices()
    return devices


async def ping_one(ip: str) -> bool:
    url = f"http://{ip}/ping"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get(url)
            return r.status_code == 200
    except Exception:
        return False


@app.post("/devices/ping")
async def ping_devices():
    devices = db.get_all_devices()
    if not devices:
        return {"checked": 0}

    async def ping_and_update(device):
        ok = await ping_one(device["ip"])
        db.update_device_status(device["id"], ok)
        return {"id": device["id"], "ip": device["ip"], "online": ok}

    tasks = [ping_and_update(d) for d in devices]
    results = await asyncio.gather(*tasks)
    return {"checked": len(results), "results": results}

