#!/usr/bin/python3
"""This is the amenity class"""

import os
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """This is the class for Amenity
    Attributes:
        name: input name
    """
    if os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place",
                                       secondary="place_amenity",
                                       viewonly=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """instantiates a new amenity"""
        super().__init__(self, *args, **kwargs)
