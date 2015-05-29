import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, PrimaryKeyConstraint
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

"""
    Class: Art
    This class contains all the information for the Art object.
    User will be able to create/modify/delete Art, but either posting a link
    or by uploading a file.
"""
class Art(Base):
    __tablename__ = 'art'

    id = Column(Integer, primary_key=True)
    link = Column(String(250))
    upload_file = Column(String(100)) # file path to where the uploaded file is stored
    title = Column(String(100), nullable=False)
    ratings = Column(Integer)
    created_by_id = Column(Integer, ForeignKey('user.id'))
    last_updated_by_id = Column(Integer, ForeignKey('user.id'))
    created_by = relationship(User, foreign_keys='Art.created_by_id')
    last_updated_by = relationship(User, foreign_keys='Art.last_updated_by_id')


"""
    Class: Artist
    This class containts information pertinant to an artist.
    We will use a separate normalization table since we will have multiple artists,
    who worked on multiple art (including joint collaboration)
"""
class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


"""
    Class: Art_Artist
    Normalization table for the two classes - Art, and Artist.
    Multiple artists can work on an art, and each artist can have multiple art forms
"""
class Art_Artist(Base):
    __tablename__ = 'art_artist'

    art_id = Column(Integer, ForeignKey('art.id'))
    artist_id = Column(Integer, ForeignKey('artist.id'))
    art = relationship(Art, foreign_keys='Art_Artist.art_id')
    artist = relationship(Artist, foreign_keys='Art_Artist.artist_id')
    __table_args__ = (PrimaryKeyConstraint(art_id, artist_id),)

"""
    Class: Tags
    Users can add as many tags as they want.
"""
class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String(100), nullable=True)


"""
    Class: Art_Tags
    Normalization table for the two classes - Art, and Tags.
    Each art can have multiple tags, each tag can be applied to multiple art
"""
class Art_Tags(Base):
    __tablename__ = 'art_tags'

    art_id = Column(Integer, ForeignKey('art.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    art = relationship(Art, foreign_keys='Art_Tags.art_id')
    tag = relationship(Tags, foreign_keys='Art_Tags.tag_id')
    __table_args__ = (PrimaryKeyConstraint(art_id, tag_id),)

"""
    Class: Comments
    Comments need to refer to the user who made the comment and the art regarding which it is
"""
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
