#!/usr/bin/python3
"""Database storage engine using SQLAlchemy with a mysql+mysqldb database
connection.
"""

import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
name2class = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance."""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.
            format(os.getenv('HBNB_MYSQL_USER'),
                   os.getenv('HBNB_MYSQL_PWD'),
                   os.getenv('HBNB_MYSQL_HOST'),
                   os.getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)
        
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session."""
        from models import classes_dict
        
        objects = {}
        if cls:
            query = self.__session.query(classes_dict[cls])
            for obj in query.all():
                key = "{}.{}".format(cls, obj.id)
                objects[key] = obj
        else:
            for cls in classes_dict.values():
                query = self.__session.query(cls)
                for obj in query.all():
                    key = "{}.{}".format(cls.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and create a new session."""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) == str and cls in name2class:
            cls = name2class[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in name2class.values():
                total += self.__session.query(cls).count()
        return total
