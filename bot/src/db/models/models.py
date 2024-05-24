from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger

from .base import Base
from enum import Enum
from schemas import Position, Status, MailType


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True, index=True)
    tg_username: Mapped[str] = mapped_column(str, index=True, unique=True, primary_key=True)
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    name: Mapped[str] 
    position: Mapped[Position] 
    
    
class Lectures(Base):
    __tablename__ = 'lectures'
    
    lecture_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True)
    name: Mapped[str]
    feedback_url: Mapped[str]
    status: Mapped[Status]
    day: Mapped[datetime]
    
    tg_username: Mapped[str] = mapped_column(str, ForeignKey('users.id'))
    

class Mailing(Base):
    __tablename__ = 'mailings'
    
    mailing_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True)
    type: Mapped[MailType]
    text: Mapped[str]
    url: Mapped[str]
    date: Mapped[datetime]
    
    admin_name: Mapped[str] = mapped_column(str, ForeignKey('users.tg_username'))