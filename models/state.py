#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """
    State class
    Attributes:
        name: name of the state
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
