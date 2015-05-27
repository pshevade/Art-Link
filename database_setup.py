import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False)
    user_image = Column(String(250))
    user_email = Column(String(100))
    is_admin = Column(Boolean, default=False)


class Art(Base):
    __tablename__ = 'art'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    artist_name = Column(String(100), nullable=False)
    ratings = Column(Integer)
    link = Column(String(250))
    upload_file = Column(String(100)) # file path to where the uploaded file is stored
    art_type = Column(String(50))
    created_by_id = Column(Integer, ForeignKey('user.id'))
    last_updated_by_id = Column(Integer, ForeignKey('user.id'))
    created_by = relationship(User, foreign_keys='Art.created_by_id')
    last_updated_by = relationship(User, foreign_keys='Art.last_updated_by_id')


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String(100), nullable=True)


class Art_Tags(Base):
    __tablename__ = 'art_tags'

    art_id = Column(Integer, ForeignKey('art.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    art = relationship(Art, foreign_keys='Art_Tags.art_id')
    tag = relationship(Tags, foreign_keys='Art_Tags.tag_id')


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    art_id = Column(Integer, ForeignKey('art.id'))
    art = relationship(Art)





engine = create_engine('sqlite:///art_link_database.db')

Base.metadata.create_all(engine)
