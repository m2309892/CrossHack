import random

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.schemas import *
import src.db.services.general_db as db
import src.db.models.models as models


async def create_lecture(session: AsyncSession, lecture_data: LectureCreate):
    new_lecture = await db.create_object(session, models.Lectures, lecture_data)
    return new_lecture


async def check_user(session: AsyncSession, user_tg: str):
    ans = await db.check_user_by_tg(session, user_tg)
    return ans


async def create_mailing(session: AsyncSession, mailing_data: MailingCreate):
    new_mailing = await db.create_object(session, models.Mailing, mailing_data)
    return new_mailing


async def get_lectures_by_tg(session: AsyncSession, user_tg: str):
    lectures = await db.get_lecture_list_by_tg_username(session, user_tg)
    return lectures


async def get_digest(session: AsyncSession):
    today = datetime.today()
    digest = await db.get_lection_list_by_date(session, today)
    return digest


async def update_lecture(session: AsyncSession, lection_id: int, new_data: )





async def get_section_list(session: AsyncSession, id_list: list[int] | None = None):
    section_list = await db.get_obj_list(session, models.Sections, SectionGet, id_list)
    return section_list


async def get_section_list_by_user_id(session: AsyncSession, user_id: int):
    section_list = await db.get_section_list_by_user_id(session, user_id)
    return section_list


async def get_section_by_id(session: AsyncSession, section_id: int):
    section = await db.get_obj_by_id(session, models.Sections, section_id, SectionGet)
    return section


async def update_section_by_id(session: AsyncSession, section_id: int, section_new_data: SectionCreate):
    await db.update_obj_by_id(session, models.Sections, section_id, section_new_data)


async def add_weather_note_to_section(session: AsyncSession, section_id: int, weather_note: WeatherCreate):
    new_weather_note = await db.add_weather_note_to_section(session, section_id, weather_note)
    return new_weather_note


async def add_collection_plant(session: AsyncSession, section_id: int, plant_data_list: list[PlantCreate]):
    new_plant_section = await db.add_collection_plant(session, section_id, plant_data_list)
    return new_plant_section


async def get_collection_plant_list(session: AsyncSession, section_id: int):
    collection_plant_list = await db.get_collection_plant_list(session, section_id)
    return collection_plant_list


async def get_collection_plant_by_id(session: AsyncSession, collection_plant_id: int):
    collection_plant = await db.get_obj_by_id(session, models.SectionPlant, collection_plant_id, PlantGet)
    return collection_plant


async def upadate_collection_plant(session: AsyncSession, collection_plant_id: int, plant_new_data: PlantCreate):
    await db.update_obj_by_id(session, models.SectionPlant, collection_plant_id, plant_new_data)


async def get_hint_to_collection_plant(session: AsyncSession, section_id: int, collection_plant_id: int):
    plant_data = await db.get_collection_plant_list(session, section_id)
    plant_data = [plant for plant in plant_data if plant.id == collection_plant_id]

    hint = await db.get_hint_to_collection_plant(session, collection_plant_id)
    return hint


async def get_plant_list(session: AsyncSession, id_list: list[int] | None = None):
    plant_list = await db.get_plant_list(session, id_list)
    return plant_list


async def create_plant(session: AsyncSession, plant_data_list: list[GeneralPlantCreate]):
    new_plant = await db.create_plant(session, plant_data_list)
    return new_plant


