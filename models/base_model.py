#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Instantiates a new model
        Args:
            args:
            kwargs: BaseModel constructor arguments
        Attributes:
            id: uniquely generated object identifier
            created_at: date and time of object creation
            updated_at: date and time of object update
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                setattr(self, key, value)
        else:
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = type(self).__name__
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Converts instance into dict format"""
        dictionary = dict(self.__dict__)
        if '_sa_instance_state' in dictionary:
            dictionary.pop('_sa_instance_state')
        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Deletes the current instance from storage"""
        from models import storage
        storage.delete(self)
