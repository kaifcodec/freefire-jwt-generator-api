# app/core.py

import json
from typing import Tuple, Dict, Any

import httpx
from Crypto.Cipher import AES
from google.protobuf import json_format, message

from app.settings import settings
from ff_proto import freefire_pb2


def pkcs7_pad(b: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(b) % block_size)
    return b + bytes([pad_len]) * pad_len


def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pkcs7_pad(plaintext, 16))


def json_to_proto(json_data: Dict[str, Any], proto_message: message.Message) -> bytes:
    json_format.ParseDict(json_data, proto_message)
    return proto_message.SerializeToString()


async def get_access_token(client: httpx.AsyncClient, uid: str, password: str) -> Tuple[str, str]:
    payload = (
        f"uid={httpx.QueryParams({'uid': uid})['uid']}"
        f"&password={httpx.QueryParams({'password': password})['password']}"
        f"&response_type=token&client_type=2&client_secret={settings.CLIENT_SECRET_PAYLOAD}"
    )
    headers = {
        "User-Agent": settings.USER_AGENT,
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive",
    }
    r = await client.post(settings.OAUTH_URL, content=payload, headers=headers, timeout=settings.TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return data.get("access_token", "0"), data.get("open_id", "0")


async def create_jwt(uid: str, password: str) -> Dict[str, str]:
    async with httpx.AsyncClient(http2=False) as client:
        access_token, open_id = await get_access_token(client, uid, password)
        if access_token == "0":
            raise RuntimeError("Failed to obtain access token.")

        login_req = {
            "open_id": open_id,
            "open_id_type": "4",
            "login_token": access_token,
            "orign_platform_type": "4",
        }

        req_msg = freefire_pb2.LoginReq()
        encoded = json_to_proto(login_req, req_msg)
        encrypted_payload = aes_cbc_encrypt(settings.MAIN_KEY, settings.MAIN_IV, encoded)

        headers = {
            "User-Agent": settings.USER_AGENT,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/octet-stream",
            "Expect": "100-continue",
            "X-Unity-Version": settings.X_UNITY_VERSION,
            "X-GA": "v1 1",
            "ReleaseVersion": settings.RELEASE_VERSION,
        }

        r = await client.post(
            settings.MAJOR_LOGIN_URL,
            content=encrypted_payload,
            headers=headers,
            timeout=settings.TIMEOUT,
        )
        r.raise_for_status()

        # Direct protobuf decode of response bytes (mirroring your Python)
        res_msg = freefire_pb2.LoginRes()
        res_msg.ParseFromString(r.content)

        # Build response
        token = res_msg.token if res_msg.token else "0"
        lock_region = res_msg.lock_region if res_msg.lock_region else ""
        server_url = res_msg.server_url if res_msg.server_url else ""

        if token == "0" or len(token) == 0:
            raise RuntimeError("Failed to obtain JWT.")

        return {
            "token": token,
            "lockRegion": lock_region,
            "serverUrl": server_url,
        }
