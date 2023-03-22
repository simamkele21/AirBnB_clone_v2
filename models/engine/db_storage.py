#!/usr/bin/python3
"""
New engine DBStrorage, transition from FileStorage
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """Defines a class DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        user = os.environ.get('HBNB_MYSQL_USER')
        pwd = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        db = os.environ.get('HBNB_MYSQL_DB')
        env = os.environ.get('HBNB_ENV')

        self.__engine = create_engine(
                        f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                        pool_pre_ping=True)
        
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        retuns a dictionary like FileStorage of __object"""
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
        """add object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reloads the storage"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """closes current session"""
        self.__session.close()
