from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    _id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    username = Column("username", String(50), nullable=False)
    email = Column("email", String(100), unique=True, nullable=False)
    password = Column("password", String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())  
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 
