from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from schemas import *
from services import *

appRoute = APIRouter()
safezone = Safezone()

@appRoute.get("/generate-iv")
def get_iv():
    iv = safezone.generate_iv()  
    return {"iv": iv.hex()}

@appRoute.get("/generate-key")
def get_encryption_key():
    key = safezone.generate_encryption_key()  
    return {"key": key.hex()}

@appRoute.post("/encrypt")
def encrypt_data(request: EncryptRequest):
    try:
        encrypted_data = safezone.encrypt_with_aes_cbc(request.data)
        print(type(encrypted_data))
        return {"encrypted_data": encrypted_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@appRoute.post("/decrypt")
def decrypt_data(request: DecryptRequest):
    try:
        decrypted_data = safezone.decrypt_with_aes_cbc(request.encrypted_data)
        return {"decrypted_data": decrypted_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))






pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@appRoute.post("/encrypt")
def encrypt_data(request: EncryptRequest):
    hashed_data = pwd_context.hash(request.data)
    return {"hashed_data": hashed_data}

@appRoute.post("/decrypt")
def decrypt_data(request: DecryptRequest):
    is_valid = pwd_context.verify(request.original_data, request.hashed_data)
    if is_valid:
        return {"status": "success", "message": "Data matches the hash"}
    else:
        raise HTTPException(status_code=400, detail="Invalid data")
