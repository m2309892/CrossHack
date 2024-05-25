import random

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.schemas import *
import src.db.services.general_db as db
import src.db.models.models as models


#добавление объекта лекция
async def create_lecture(session: AsyncSession, lecture_data: LectureCreate):
    new_lecture = await db.create_object(session, models.Lectures, lecture_data)
    return new_lecture


#добавление объекта опрос
async def create_mailing(session: AsyncSession, mailing_data: MailingCreate):
    new_mailing = await db.create_object(session, models.Mailing, mailing_data)
    return new_mailing


#проверка юзера на принадлежность к компании
async def check_user(session: AsyncSession, user_tg: str):
    ans = await db.check_user_by_tg(session, user_tg)
    return ans


#получение лекций сотрудника по его тг
async def get_lectures_by_tg(session: AsyncSession, user_tg: str):
    lectures = await db.get_lecture_list_by_tg_username(session, user_tg)
    return lectures


#получение списка лекций на  текущий квартал (дайджест)
async def get_digest(session: AsyncSession):
    today = datetime.today()
    digest = await db.get_lection_list_by_date(session, today)
    return digest


#обновление объекта лекция
async def update_lecture(session: AsyncSession, lection_id: int, new_data: LecturesUpdate):
    await db.update_obj_by_id(session, models.Lectures, lection_id, new_data)


#обновление объекта юзер
async def update_user(session: AsyncSession, user_tg: str, new_data: LecturesUpdate):
    await db.update_user_by_tg(session, user_tg, new_data)


#обновление объекта опрос
async def update_mailing(session: AsyncSession, mailing_id: int, new_data: MailingUpdate):
    await db.update_obj_by_id(session, models.Mailing, mailing_id, new_data)
    
