from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger
from create_db import Base
from enum import Enum
from schemas import Position, Status, MailType


class Users(Base):
    __tablename__ = 'users'

    tg_user_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True)
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    position: Mapped[Position] 
    name: Mapped[str] 
    
    
class Lectures(Base):
    __tablename__ = 'lectures'
    
    lecture_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True)
    name: Mapped[str]
    feedback_url: Mapped[str]
    status: Mapped[Status]
    date: Mapped[datetime]
    
    owner_id: Mapped[str] = mapped_column(str, ForeignKey('users.id'))
    

class Mailing(Base):
    __tablename__ = 'mailings'
    
    mailing_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True)
    type: Mapped[MailType]
    text: Mapped[str]
    url: Mapped[str]
    
    admin_id: Mapped[str] = mapped_column(str, ForeignKey('users.id'))