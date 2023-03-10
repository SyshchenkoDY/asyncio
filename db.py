from sqlalchemy import Column as c, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base


PG_DSN = f'postgresql+asyncpg://app:secret@127.0.0.1:5431/app'
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Person(Base):
    __tablename__ = 'person'

    id = c(Integer, primary_key=True, autoincrement=True)
    pers_id = c(Integer, nullable=False)
    birth_year = c(String(10))
    films = c(String)
    gender = c(String)
    hair_color = c(String)
    height = c(String)
    homeworld = c(String)
    mass = c(String)
    name = c(String)
    species = c(String)
    starships = c(String)
    vehicles = c(String)




