from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database connection details
DB_USER = 'admin123'
DB_PASSWORD = 'p0ssw0rd'
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'hakaton_db'

# Create SQLAlchemy engine
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)

# Base class for declarative models
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    tg_username = Column(String(255), unique=True, nullable=False)
    tg_chat_id = Column(BigInteger)
    name = Column(String(255))
    position = Column(String(50))

class Lecture(Base):
    __tablename__ = 'lectures'
    lecture_id = Column(BigInteger, primary_key=True)
    lecture_name = Column(String(255))
    lecture_description = Column(Text)
    location = Column(String(255))
    date = Column(DateTime)
    duration = Column(String(50))
    additional_info = Column(Text)
    tg_username = Column(String(255), ForeignKey('users.tg_username'))
    feedback_url = Column(String(255))
    conference_url = Column(String(255))
    lecture_materials_url = Column(String(255))
    status = Column(String(50))
    time_in_sheet = Column(DateTime)

class Mailing(Base):
    __tablename__ = 'mailings'
    mailing_id = Column(BigInteger, primary_key=True)
    type = Column(String(50))
    text = Column(Text)
    survey_url = Column(String(255))
    date = Column(DateTime)
    status = Column(String(50))
    admin_name = Column(String(255), ForeignKey('users.tg_username'))

Session = sessionmaker(bind=engine)