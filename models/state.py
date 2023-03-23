#!/usr/bin/python3
"""This is the state class"""

from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    if os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade="all, delete", backref='state')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """instantiates a new state"""
        super().__init__(self, *args, **kwargs)

    @property
    def cities(self):
        """return list of cities"""
        if os.getenv('HBNB_TYPE_STORAGE', '') != 'db':
            all_cities = models.storage.all("City")
            city_list = []
            for cityid in all_cities:
                if all_cities[cityid].state_id == self.id:
                    city_list.append(all_cities[cityid])
            return city_list
