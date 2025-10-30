# app/main.py

from fastapi import FastAPI, Query, Body, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.core import create_jwt

app = FastAPI(title="FreeFire JWT API", version="1.0.0")


class TokenRequest(BaseModel):
    uid: str
    password: str


@app.get("/")
async def root():
    return {
        "message": "JWT API running. Use POST /api/token with JSON { uid, password } or GET /api/token?uid=...&password=...",
    }


# GET with query parameters (convenience)
@app.get("/api/token")
async def get_token(uid: str = Query(...), password: str = Query(...)):
    try:
        result = await create_jwt(uid, password)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# POST JSON (preferred)
@app.post("/api/token")
async def post_token(payload: TokenRequest = Body(...)):
    try:
        result = await create_jwt(payload.uid, payload.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
