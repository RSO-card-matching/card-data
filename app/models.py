# pylint: disable=no-name-in-module

from typing import Optional

from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String


Base = declarative_base()


class Card(BaseModel):
    id: int
    title: str
    series: str
    manufacturer: str
    serial_num: Optional[str] = None

class CardNew(BaseModel):
    title: str
    series: str
    manufacturer: str
    serial_num: Optional[str] = None

class CardUpdate(BaseModel):
    title: Optional[str] = None
    series: Optional[str] = None
    manufacturer: Optional[str] = None
    serial_num: Optional[str] = None

class NewCardID(BaseModel):
    id: int

class CardModel(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    series = Column(String, index = True)
    manufacturer = Column(String, index = True)
    serial_num = Column(String)
