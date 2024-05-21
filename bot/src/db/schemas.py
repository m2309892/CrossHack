from enum import Enum
from pydantic import BaseModel


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


#class Mailing