from sqlalchemy import sql, Column, BigInteger, String, Integer, Boolean, DateTime, ForeignKey

from .base import BaseModel


class Reminder(BaseModel):
    __tablename__ = 'reminders'
    query: sql.Select
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.uid'))
    notify_time = Column(DateTime(timezone=True))