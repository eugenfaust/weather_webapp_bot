from sqlalchemy import sql, Column, BigInteger, String, Integer, Boolean, DateTime

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    query: sql.Select
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    status = Column(Boolean, default=True)
    uid = Column(BigInteger, unique=True)
    admin = Column(Boolean, default=False)
    last_action = Column(DateTime(timezone=True))
    username = Column(String(50))
    full_name = Column(String(100))
    location = Column(String(50))
    city_name = Column(String(50))
    created = Column(DateTime(timezone=True))
    ref_id = Column(Integer, default=0)