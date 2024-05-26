import random

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.services.db import async_session
from src.db.schemas import *
import src.db.services.general_db as db
import src.db.models.models as models

#сделать дергание по айдишнику (добавляется после чека на принадлежность)
#check admin

#добавление объекта лекция
async def create_lecture(lecture_data: LectureCreate):
    async with async_session() as session:
        new_lecture = await db.create_object(session, models.Lectures, lecture_data)
        return new_lecture
    

#добавление объекта опрос
async def create_mailing(mailing_data: MailingCreate):
    async with async_session() as session:
        new_mailing = await db.create_object(session, models.Mailing, mailing_data)
        return new_mailing


#проверка юзера на принадлежность к компании
async def check_user(user_tg: str):
    async with async_session() as session:
        ans = await db.check_user_by_tg(session, user_tg)
        if ans is None:
           return False
        else:
           return True
       
       
async def check_admin(user_tg: str):
    async with async_session() as session:
        ans = await db.check_admin_by_tg_username(session, user_tg)
        if ans is None:
           return False
        else:
           return True
    
    
async def get_user_by_tg(user_tg: str):
    async with async_session() as session:
        ans = await db.check_user_by_tg(session, user_tg)
        return ans
    

#получение лекций сотрудника по его тг
async def get_lectures_by_tg(user_tg: str):
    async with async_session() as session:
        lectures = await db.get_lecture_list_by_tg_username(session, user_tg)
        return lectures


#получение списка лекций на  текущий квартал (дайджест)
async def get_digest():
    today = datetime.today()
    async with async_session() as session:
        digest = await db.get_lection_list_by_date(session, today)
        return digest


#обновление объекта лекция
async def update_lecture(lection_id: int, new_data: LecturesUpdate):
    async with async_session() as session:
       await db.update_obj_by_id(session, models.Lectures, lection_id, new_data)


#обновление объекта юзер
async def update_user(user_tg: str, new_data: LecturesUpdate):
    async with async_session() as session:
        await db.update_user_by_tg(session, user_tg, new_data)


#обновление объекта опрос
async def update_mailing(mailing_id: int, new_data: MailingUpdate):
    async with async_session() as session:
        await db.update_obj_by_id(session, models.Mailing, mailing_id, new_data)
    

async def get_mailing_filter(type_data: MailType | MailType = None, status_data: StatusMailing| StatusMailing = None):
    async with async_session() as session:
        await db.get_mailing_by_status_and_type(session, type_data, status_data)
        
        
async def get_all_lectures(status_data: StatusLecture):
    async with async_session() as session:
        await db.get_lecture_by_status_and_date(session, status_data)
    
    
'''async def get_all_admins_filter(limit: int = 1000, offset: int = 0, filter_data: UserFilterData | None = None):
    async with db.async_session() as session:
        return await db.get_object(
            models.Users,
            session,
            UserData,
            limit,
            offset,
            filter_data=filter_data
        )
        

async def get_all_mailings_filter(limit: int = 1000, offset: int = 0, filter_data: MailingFilterData | None = None):
    async with db.async_session() as session:
        return await db.get_object(
            models.Mailing,
            session,
            MailingData,
            limit,
            offset,
            filter_data=filter_data
        )
        
        
async def get_all_lectures(limit: int = 1000, offset: int = 0, filter_data: LectureFilterData | None = None):
    async with db.async_session() as session:
        return await db.get_object(
            models.Lectures,
            session,
            LectureData,
            limit,
            offset,
            filter_data=filter_data
        )'''