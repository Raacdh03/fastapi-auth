import base64
import secrets
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from sqlalchemy.orm import Session
from sqlalchemy import asc
from models import User
from schemas import *
from sqlalchemy.exc import IntegrityError

class HttpResponse:
    def success(self, data):
        return {"status": "success", "data": data}
    
    def not_found(self, message="Content tidak ditemukan"):
        return {"status": "error", "message": message}

    def error(self, message="An error occurred"):
        return {"status": "error", "message": message}
    
class ServiceContent:

    def __init__(self):
        self.response =  HttpResponse()

    async def getall(self, db):
        # contents = db.query(Content).all()
        contents = db.query(User).order_by(asc(User._id)).all()

        if contents:
            return self.response.success(contents)
        else:
            return self.response.not_found(message="Content tidak ditemukan")
        
    async def get_by_id(self, db, user_id: int):
        # Query untuk mendapatkan konten berdasarkan ID
        content = db.query(User).filter(User._id == user_id).first()

        if content:
            return self.response.success(content)
        else:
            return self.response.not_found(message=f"Content dengan ID {user_id} tidak ditemukan")

    async def create_user(self, db: Session, user_data: UserCreate):
        # Membuat objek Content baru dengan data yang diterima
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,  
        )

        try:
            db.add(new_user)
            db.commit()  # Simpan ke database
            db.refresh(new_user)  # Memperbarui objek baru dengan data yang tersimpan di database
            return self.response.success(new_user)
        except IntegrityError:
            db.rollback()  
            return self.response.error(message="Email sudah digunakan")
        except Exception as e:
            db.rollback()
            return self.response.error(message=str(e))
        
    async def update_user(self, db: Session, user_id: int, user_data: UserUpdate):
        # Cari konten berdasarkan ID
        content = db.query(User).filter(User._id == user_id).first()

        if content:
            # Update field yang diberikan
            if user_data.username:
                content.username = user_data.username
            if user_data.email:
                content.email = user_data.email
            if user_data.password:
                content.password = user_data.password  

            db.commit()
            db.refresh(content)  
            return self.response.success(content)
        else:
            return self.response.not_found(message=f"Content dengan ID {user_id} tidak ditemukan")
        
    async def delete(self, user_id: int, db):
        user_to_delete = db.query(User).filter(User._id == user_id).first()
        
        if user_to_delete:
            db.delete(user_to_delete)
            db.commit()
            return self.response.success({"message": f"User dengan ID {user_id} berhasil dihapus"})
        else:
            return self.response.not_found(message=f"User dengan ID {user_id} tidak ditemukan")

class Safezone:
    def __init__(self):
        self.client_id = Config.CLIENT_ID
        self.key = Config.ENCRYPTION_KEY
        self.iv = Config.IV

    def generate_client_credential(self):
        client_id = secrets.token_hex(16)
        secret_key = secrets.token_hex(32)

        return client_id, secret_key
    
    def generate_encryption_key(self):
        return os.urandom(32)
    
    def generate_iv(self):
        return os.urandom(16)
    
    def encrypt_with_aes_cbc(self, data: str) -> bytes:
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()

        cipher = Cipher(
            algorithms.AES(bytes.fromhex(self.key)),
            modes.CBC(bytes.fromhex(self.iv)),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_with_aes_cbc(self, encrypted_data):
        cipher = Cipher(
            algorithms.AES(bytes.fromhex(self.key)),
            modes.CBC(bytes.fromhex(self.iv)),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(base64.b64decode(encrypted_data)) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return data.decode()
