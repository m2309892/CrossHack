from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger

from .base import Base
from enum import Enum
from schemas import Position, StatusLecture, MailType, StatusMailing


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

    # данные из гугл формы для принятия заявок
    lecture_name: Mapped[str]
    lecture_description: Mapped[str]
    location: Mapped[str]
    date: Mapped[datetime]
    duration: Mapped[str]
    additional_info: Mapped[str] | None
    tg_username: Mapped[str] = mapped_column(str, ForeignKey('users.tg_username'))

    # статус заявки (лекции)
    status: Mapped[StatusLecture]
    

class Mailing(Base):
    __tablename__ = 'mailings'
    
    mailing_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True)
    type: Mapped[MailType]
    text: Mapped[str]
    feedback_url: Mapped[str] | None
    conference_url: Mapped[str] | None
    lecture_meterials_url: Mapped[str] | None
    servey_url: Mapped[str] | None
    date: Mapped[datetime]
    status: Mapped[StatusMailing]
    
    admin_name: Mapped[str] = mapped_column(str, ForeignKey('users.tg_username'))