from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger

from .base import Base
from enum import Enum
from schemas import Position, Status_lecture, Status_user, MailType

# модель пользователя
class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True, index=True)
    tg_username: Mapped[str] = mapped_column(str, index=True, unique=True, primary_key=True)
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    user_name: Mapped[str] 
    position: Mapped[Position]
    #status: Mapped[Status_user]
    
# модель лекции (для отбора по результатам опроса и для уведомлений)
class Lectures(Base):
    __tablename__ = 'lectures'

    lecture_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True)

    # данные из гугл формы для принятия заявок
    lecture_name: Mapped[str]
    lecture_description: Mapped[str]
    location: Mapped[str]
    date: Mapped[datetime]
    duration: Mapped[str]
    additional_info: Mapped[str]
    tg_username: Mapped[str] = mapped_column(str, ForeignKey('users.id'))

    # статус заявки (лекции)
    status: Mapped[Status_lecture]

# модель для увдемлений: о приёме заявок, о лекциях
class Mailing(Base):
    __tablename__ = 'mailings'
    
    mailing_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True)
    type: Mapped[MailType]
    text: Mapped[str]
    feedback_url: Mapped[str]
    conference_url: Mapped[str]
    lecture_meterials_url: Mapped[str]
    date: Mapped[datetime]
    
    admin_name: Mapped[str] = mapped_column(str, ForeignKey('users.tg_username'))


