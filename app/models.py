from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    DateTime
)

from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger , unique=True , nullable=False)
    name = Column(String(length=128) , nullable=False)
    contact = Column(String(length=25))
    

    created_at = Column(DateTime , default=datetime.now)
    updated_at = Column(DateTime , onupdate=datetime.now)