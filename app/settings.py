# app/settings.py

import base64
from pydantic import BaseModel

class Settings(BaseModel):
    MAIN_KEY_B64: str = "WWcmdGMlREV1aDYlWmNeOA=="
    MAIN_IV_B64: str = "Nm95WkRyMjJFM3ljaGpNJQ=="
    RELEASE_VERSION: str = "OB50"
    USER_AGENT: str = "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)"
    CLIENT_SECRET_PAYLOAD: str = (
        "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3&client_id=100067"
    )
    OAUTH_URL: str = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    MAJOR_LOGIN_URL: str = "https://loginbp.ggblueshark.com/MajorLogin"
    X_UNITY_VERSION: str = "2018.4.11f1"
    TIMEOUT: float = 15.0

    @property
    def MAIN_KEY(self) -> bytes:
        return base64.b64decode(self.MAIN_KEY_B64)

    @property
    def MAIN_IV(self) -> bytes:
        return base64.b64decode(self.MAIN_IV_B64)

settings = Settings()
