import os
import sys
from urlparse import urlparse


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
    Class: Article_Type
    Users can add as many tags as they want.
"""
class Article_Type(Base):
    __tablename__ = 'article_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


"""
    Class: Article
    This class contains all the information for the Article object.
    User will be able to create/modify/delete Article, but either posting a link
    or by uploading a file.
"""
class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    link = Column(String(250), nullable=False)
    url_scheme = Column(String(8), default=None)
    url_netloc = Column(String(250), default=None)
    url_path = Column(String(250), default=None)
    url_params = Column(String(250), default=None)
    url_query = Column(String(250), default=None)
    url_fragment = Column(String(250), default=None)
    url_hostname = Column(String(250), default=None)
    url_port = Column(String(5), default=None)
    searchable_link = Column(String(250), nullable=False)
    title= Column(String(250), nullable=False)
    upload_file = Column(String(100)) # file path to where the uploaded file is stored
    article_type_id = Column(Integer, ForeignKey('article_type.id'))
    article_type = relationship(Article_Type, foreign_keys='Article.article_type_id')
    ratings = Column(Integer, default=0)
    about = Column(String(500))
    created_by_id = Column(Integer, ForeignKey('user.id'))
    last_updated_by_id = Column(Integer, ForeignKey('user.id'))
    created_by = relationship(User, foreign_keys='Article.created_by_id')
    last_updated_by = relationship(User, foreign_keys='Article.last_updated_by_id')


    @property
    def serialize(self):
        return {
            "link"      : self.link,
            "title"     : self.title,
            "ratings"   : self.ratings,
            "about"     : self.about,
            "created_by": self.created_by.user_name,
            "last_updated_by" : self.last_updated_by.user_name
        }



"""
    Class: Tags
    Users can add as many tags as they want.
"""
class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String(100), nullable=True)

    @property
    def serialize(self):
        return {
            "tag_name"      : self.tag_name,
        }





"""
    Class: Article_Tags
    Normalization table for the two classes - Article, and Tags.
    Each art can have multiple tags, each tag can be applied to multiple article
"""
class Article_Tags(Base):
    __tablename__ = 'article_tags'

    article_id = Column(Integer, ForeignKey('article.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    article = relationship(Article, foreign_keys='Article_Tags.article_id')
    tag = relationship(Tags, foreign_keys='Article_Tags.tag_id')
    __table_args__ = (PrimaryKeyConstraint(article_id, tag_id),)


    @property
    def serialize(self):
        return {
            # "article_id"         : self.article_id,
            # "tag_id"             : self.tag_id,
            "article_title"      : self.article.title,
            "tag_name"           : self.tag.tag_name,
        }

"""
    Class: Comments
    Comments need to refer to the user who made the comment and the art regarding which it is
"""
class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, foreign_keys='Comments.user_id')
    article_id = Column(Integer, ForeignKey('article.id'))
    article = relationship(Article, foreign_keys='Comments.article_id')

    @property
    def serialize(self):
        return {
            "text"      : self.text,
            "comment_by": self.user.user_name
        }




engine = create_engine('sqlite:///article_link_database.db')

Base.metadata.create_all(engine)


#"""
#     Class: Artist
#     This class containts information pertinant to an artist.
#     We will use a separate normalization table since we will have multiple artists,
#     who worked on multiple art (including joint collaboration)
# """
# class Artist(Base):
#     __tablename__ = 'artist'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)


# """
#     Class: Art_Artist
#     Normalization table for the two classes - Art, and Artist.
#     Multiple artists can work on an art, and each artist can have multiple art forms
# """
# class Art_Artist(Base):
#     __tablename__ = 'art_artist'

#     art_id = Column(Integer, ForeignKey('art.id'))
#     artist_id = Column(Integer, ForeignKey('artist.id'))
#     art = relationship(Art, foreign_keys='Art_Artist.art_id')
#     artist = relationship(Artist, foreign_keys='Art_Artist.artist_id')
#     __table_args__ = (PrimaryKeyConstraint(art_id, artist_id),)
