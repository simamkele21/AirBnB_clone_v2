#!/usr/bin/python3
"""
New engine DBStrorage, transition from FileStorage
"""

import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, MetaData
from models import base_model, amenity, city, place, review, state, user
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.user import User
from models.state import State
from models.review import Review
from models.city import City
from models.amenity import Amenity
from models.place import Place, PlaceAmenity
from models.engine.file_storage import FileStorage


class DBStorage:
    """docstring
    """

    DNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    __engine = None
    __session = None

    def __init__(self):
        """drop all tables if the environment variable
        HBNB_ENV is equal to test"""

        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
                        f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                        pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        retuns a dictionary like FileStorage of __object
        """
        objects = {}
        classes = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for c in classes:
                query = self.__session.query(eval(c)).all()
                for obj in query:
                    key = '{}.{}'.format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """add the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session (self.__session)
        """
        self.__session.commit()

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)
        (WARNING: all classes who inherit from Base must be imported
        before calling Base.metadata.create_all(engine))
        create the current database session (self.__session)
        from the engine (self.__engine)
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """
        if obj is None:
            return
        self.__session.delete(obj)

    def close(self):
        self.__session.remove()
