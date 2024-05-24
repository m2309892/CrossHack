from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from models.models import *
import db.models.models as model
import db.schemas as schema
#import src.schemas.general_schemas as schema
from .db import Basic


async def create_object(session: AsyncSession, table_obj: Basic, data: list[BaseModel], responce_model: BaseModel | None = None):
    new_obj_list = []

    for sub_data in data:
        new_obj = table_obj(**sub_data.model_dump())
        session.add(new_obj)
        await session.flush()
        new_obj_list.append(new_obj)

    await session.commit()

    if responce_model:
        new_obj_list = [responce_model.model_validate(obj, from_attributes=True) for obj in new_obj_list]

    return new_obj_list


async def get_obj_list(session: AsyncSession, table_obj: Basic, responce_model: BaseModel | None = None, id_list: list[int] | None = None):
    expr = select(table_obj)

    if id_list:
        expr = expr.where(table_obj.id.in_(id_list))

    obj_list = await session.execute(expr)
    obj_list = obj_list.scalars().all()

    if responce_model:
        obj_list = [responce_model.model_validate(obj, from_attributes=True) for obj in obj_list]

    return obj_list


async def get_obj_list_by_join(session: AsyncSession, table_obj: Basic, join_table_obj: Basic, join_id_name: str, condition_id_name: str, condition_id, responce_model: BaseModel | None = None):
    obj_list = await session.execute(
        select(
            table_obj
        ).join(
            join_table_obj,
            join_table_obj.id == table_obj.__get_attr__(join_id_name)
        ).where(
            join_table_obj.__get_attr__(condition_id_name) == condition_id
        )
    )
    obj_list = obj_list.scalars().all()

    if responce_model:
        obj_list = [responce_model.model_validate(obj, from_attributes=True) for obj in obj_list]

    return obj_list


async def get_obj_by_id(session: AsyncSession, table_obj: Basic, obj_id: int, responce_model: BaseModel | None = None):
    obj_res = await session.execute(
        select(
            table_obj
        ).where(
            table_obj.id == obj_id
        )
    )
    obj_res = obj_res.scalar_one_or_none()
    
    if responce_model:
        obj_res = responce_model.model_validate(obj_res, from_attributes=True)
        
    if obj_res is None:
        return []
    return obj_res


async def update_obj_by_id(session: AsyncSession, table_obj: Basic, obj_id: int, data: BaseModel):
    obj_res = await session.execute(
        select(
            table_obj
        ).where(
            table_obj.id == obj_id
        )
    )
    obj_res = obj_res.scalar_one_or_none()


async def check_id_by_model(session: AsyncSession, table_obj: Basic, check_id: int):
    check = await session.execute(
        select(
            table_obj.id
        ).where(
            table_obj.id == check_id
        )
    )
    check = check.scalar_one_or_none()


async def check_id_set_by_model(session: AsyncSession, table_obj: Basic, check_id_set: set[int]):
    model_id_list = await session.execute(
        select(
            table_obj.id
        ).where(
            table_obj.id.in_(check_id_set)
        )
    )
    model_id_list = model_id_list.scalars().all()
    model_id_list = set(model_id_list)
    
    
    
#SPECIFIC DB PROC
async def get_lecture_list_by_user_id(session: AsyncSession, user_id: int): #get запрос для "мои лекции" и для отчетности
    lecture_list = await session.execute(
        select(
            Lectures
        ).where(
            Lectures.user_id == user_id
        )
    )
    lecture_list = lecture_list.scalars().all()

    lecture_list = [schema.LectionGet.model_validate(section, from_attributes=True) for section in lecture_list]
    return lecture_list


async def get_lection_list_by_date(session: AsyncSession, date: datetime): #get запрос для "дайджест"
    lecture_list = await session.execute(
        select(
            Lectures
        ).where(
            Lectures.day == date or (abs(Lectures.day - date) <= '30:00:00') #тут нужно понять, как проверить, попадает ли лекция в квартал
        )
    )
    lecture_list = lecture_list.scalars().all()

    lecture_list = [schema.LectionGet.model_validate(section, from_attributes=True) for section in lecture_list]
    return lecture_list

