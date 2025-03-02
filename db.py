import dataclasses
from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

user_project = Table('user_project', Base.metadata,
                     Column('user_id', Integer, ForeignKey('users.id')),
                     Column('project_id', Integer, ForeignKey('projects.id'))
                     )


@dataclasses.dataclass
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    role = Column(String)
    profile = relationship('Profile', backref='users', uselist=False)
    projects = relationship('Project', secondary=user_project, backref='users')


@dataclasses.dataclass
class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    bio = Column(String)
    phone = Column(String, unique=True)
    skill = Column(String)
    social_link = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)


@dataclasses.dataclass
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    tasks = relationship('Task', backref='projects')


@dataclasses.dataclass
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))


async def create_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.drop_all)
