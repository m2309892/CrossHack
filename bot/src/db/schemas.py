from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class Position(str, Enum):
    INTERN = 'Стажер'
    ADMIN = 'Админ'
    EMPLOYEE = 'Сотрудник'
    FIRED = 'Уволен'
    
class StatusLecture(str, Enum):
    CREATED = 'Создана'
    CHANGED = 'Изменена'
    APPROVED = 'Одобрена'
    COMPLETED = 'Завершена'

class StatusMailing(str, Enum):
    ACTIVE = 'Активен'
    INACTIVE = 'Неактивен'
    
class MailType(str, Enum):
    CROSSTALKS = 'CrossTalks'
    LECTURE = 'Лекция'

#for model MAILING
class MailingCreate(BaseModel):
    type: MailType
    text: str
    url: str
    date: datetime
    admin_name: str
    status: StatusMailing
    
class MailingData(MailingCreate):
    id: int
    
class MailingUpdate(BaseModel):
    type: MailType | None
    text: str | None
    url: str | None
    date: datetime | None
    
class MailingFilterData(BaseModel):
    date: datetime | None
    status: StatusMailing | None
    type: MailType | None
    
#for model LECTURES
class LectureCreate(BaseModel):
    name: str
    feedback_url: str
    status: StatusLecture
    day: datetime
    tg_username: str
    
class LectureData(LectureCreate):
    id: int
    
class LecturesUpdate(BaseModel):
    status: StatusLecture
    
class LectureFilterData(BaseModel):
    id: int | None
    day: datetime | None
    status: StatusLecture | None
    
#for model USERS
class UserCreate(BaseModel):
    tg_username: str
    tg_chat_id: int
    name: str
    position: Position
    
class UserData(UserCreate):
    user_id: int
    
class UserUpdate(BaseModel):
    position: Position | None
    tg_username: str | None
    
class UserFilterData(BaseModel):
    tg_username: str | None
    position: Position | None