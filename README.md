# FreeFire JWT API 🎮

* For any question, write an email to: kaifcodec@gmail.com
---
A **FastAPI** service that generates a game **JSON Web Token (JWT)** by reproducing the official mobile client flow.  
This process involves using the OAuth guest grant, protobuf serialization (via own `ff_proto/freefire_pb2.py`), and **AES-128-CBC** payload encryption.

The API supports both **POST JSON** and **GET query parameters** and is designed for easy deployment.

---

## ✨ Features
* **FastAPI Endpoints**: `POST /api/token` (preferred) and `GET /api/token` for quick testing and integration.  
* **Protobuf Integration**: Uses generated `ff_proto/freefire_pb2.py` module directly.  
* **Portable Start**: Simple, portable start script **`run.sh`** to use on any host (Render, Railway, Fly.io, VPS, etc.).

---

## 📁 Directory Structure
```text
app/main.py              # FastAPI routes and service bootstrap
app/core.py              # OAuth logic, protobuf encoding/decoding, AES encryption
app/settings.py          # Configuration (keys, IV, headers, URLs)
ff_proto/freefire_pb2.py # Generated protobuf module
requirements.txt         # Pinned dependencies
run.sh                   # Uvicorn startup script
```

---

## 🛠️ Requirements
```text
Python 3.11+ recommended

fastapi==0.115.0
uvicorn[standard]==0.30.6
httpx==0.27.2
protobuf==6.30.0
pycryptodome==3.20.0
pydantic==2.9.2
```
---

## ⚙️ Installation
1. **Clone repository**:
   ```bash
   git clone https://github.com/kaifcodec/freefire-jwt-generator-api.git && cd freefire-jwt-generator-api
   ```
2. **Create virtualenv and install dependencies**:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
---

### run.sh (Reference) or Start command for backend: `./run.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
export PYTHONUNBUFFERED=1
uvicorn app.main:app --host 0.0.0.0 --port 3000 --workers 1
```

---

## 🚀 API Usage

### GET (Quick Testing)
```bash
curl "http://localhost:3000/api/token?uid=4104181280&password=6485A0BBC486BFE8CF065F14D45F9CDAB5BE5D7F2A5998A6A7CABB295BA5F31A"
```

### POST (Preferred)
```bash
curl -X POST http://localhost:3000/api/token 
  -H "Content-Type: application/json" 
  -d '{"uid":"4104181280","password":"6485A0BBC486BFE8CF065F14D45F9CDAB5BE5D7F2A5998A6A7CABB295BA5F31A"}'
  ```

### ✅ Successful Response Example
```json
{
  "token": "<JWT>",
  "lockRegion": "IND",
  "serverUrl": "https://..."
}
```

---

## ⚙️ Configuration
Edit `app/settings.py`:
* Modify keys/IVs: `MAIN_KEY_B64`, `MAIN_IV_B64`  
* Update version/headers: `RELEASE_VERSION`, `USER_AGENT`  
* Change URLs if endpoints are updated: `OAUTH_URL`, `MAJOR_LOGIN_URL`  
* Environment Overrides: `PORT` and `WORKERS` are consumed by `run.sh`.

---

## 📝 Notes
* **Protobuf Compatibility**: `freefire_pb2.py` must match the server schema of the current client version. Update this file whenever the game app version changes.  
* **Latency**: Primarily determined by external OAuth/MajorLogin calls. Host your service near the game servers for lower RTT.  
* **Security**: Always prefer using the **POST** endpoint for submitting credentials in production.

---

## 📜 License and Credits
Preserve original notices from your `get_jwt.py` according to your chosen license terms.

<p align="center">
  <img src="https://visitor-badge.laobi.icu/badge?page_id=kaifcodec.freefire-jwt-generator-api&style=for-the-badge&color=0078ff" alt="Repo Views">
</p>
