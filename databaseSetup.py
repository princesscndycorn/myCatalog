from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os
import sys

Base = declarative_base()

# This code was used from the Udacity Course Material.

class User(Base):
    '''
    This class will build the User database table.
    '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Categorys(Base):
    '''
    This class will build the Caregorys list.
    '''
    __tablename__ = 'categorys'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class CatItems(Base):
    '''
    This class will define the items under the
    categorys.
    '''
    __tablename__ = 'cat_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    categorys_id = Column(Integer, ForeignKey('categorys.id'))
    categorys = relationship(Categorys)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///waylandDatabase.db')
Base.metadata.create_all(engine)
