from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class Position(str, Enum):
    INTERN = 'Стажер'
    ADMIN = 'Админ'
    EMPLOYEE = 'Сотрудник'
    
class Status(str, Enum):
    CREATED = 'Создана'
    CHANGED = 'Изменена'
    APPROVED = 'Одобрена'
    COMPLETED = 'Завершена'

class MailType(str, Enum):
    ORGANIZATORS = 'Организаторы'
    SPEAKERS = 'Спикеры'

#for model MAILING
class MailingCreate(BaseModel):
    type: MailType
    text: str
    url: str
    date: datetime
    admin_name: str
    
class MailingData(MailingCreate):
    id: int
    
#for model LECTURES
class LectureCreate(BaseModel):
    name: str
    feedback_url: str
    status: Status
    day: datetime
    tg_username: str
    
class LectureData(LectureCreate):
    id: int
    
#for model USERS
class UserCreate(BaseModel):
    tg_username: str
    tg_chat_id: int
    name: str
    position: Position
    
class UserDate(UserCreate):
    user_id: int