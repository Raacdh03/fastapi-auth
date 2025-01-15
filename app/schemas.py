from datetime import timedelta
from pydantic import BaseModel
from typing import Optional
from config import Config

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

# class EncryptRequest(BaseModel):
#     data: str

# class DecryptRequest(BaseModel):
#     hashed_data: str
#     original_data: str

class SettingJWT(BaseModel):
    authjwt_secret_key: str = Config.SECRET_KEY
    authjwt_algorithm: str = "RS256"
    authjwt_public_key: str = Config.JWT_PUBLIC_KEY
    authjwt_private_key: str = Config.JWT_PRIVATE_KEY
    authjwt_access_token_expires: int = timedelta(minutes=15)
    authjwt_refresh_token_expires: int = timedelta(days=30)
    authjwt_token_location: set = {"headers"}
    # authjwt_cookie_secure: bool = True
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_samesite: str = 'lax'

class EncryptRequest(BaseModel):
    data: str

class DecryptRequest(BaseModel):
    encrypted_data: str
