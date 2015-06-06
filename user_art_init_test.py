# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from urlparse import urlparse
from session_setup import *
from helper import *
# from database_setup import Base, User, Article_Type, Article, Article_Tags, Tags, Comments

# engine = create_engine('sqlite:///article_link_database.db')

# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)

# session = DBSession()

primary_user = User(user_name="foo",
                    user_image="foo.jpg",
                    user_email="foo@foobaifoo.com",
                    is_admin=True)

session.add(primary_user)
session.commit()

secondary_user = User(user_name="bar",
                    user_image="bar.jpg",
                    user_email="bar@barbar.com",
                    is_admin=False)

session.add(secondary_user)
session.commit()

type_academic = Article_Type(name='academic')
session.add(type_academic)
session.commit()

type_blog = Article_Type(name='blog')
session.add(type_blog)
session.commit()

type_news = Article_Type(name='news')
session.add(type_news)
session.commit()

type_opinion = Article_Type(name='opinion')
session.add(type_opinion)
session.commit()

type_tutorial = Article_Type(name='tutorial')
session.add(type_tutorial)
session.commit()


type_portrait = Article_Type(name='portrait')
session.add(type_portrait)
session.commit()

full_link="http://www.copterlabs.com/blog/json-what-it-is-how-it-works-how-to-use-it/"
full_link_url_obj = urlparse(full_link)
art1 = Article( link=full_link,
            # url_scheme = full_link_url_obj.scheme,
            # url_netloc = full_link_url_obj.netloc,
            # url_path = full_link_url_obj.path,
            # url_params = full_link_url_obj.params,
            # url_query = full_link_url_obj.query,
            # url_fragment = full_link_url_obj.fragment,
            # url_hostname = full_link_url_obj.hostname,
            # url_port = full_link_url_obj.port,
            title = "JSON: What it is, How it works, and how to use it",
            upload_file = "", # file path to where the uploaded file is stored
            article_type=type_opinion,
            about="An article on how json works",
            created_by = primary_user,
            last_updated_by = primary_user)

art1 = createArticleIfNotExists(art1)

# session.add(art1)
# session.commit()

comment1 = Comments(text="What a great article", user=primary_user, article=art1)
session.add(comment1)
session.commit()

full_link="http://bost.ocks.org/mike/treemap/"
full_link_url_obj = urlparse(full_link)
art2 = Article(link=full_link,
            # url_scheme = full_link_url_obj.scheme,
            # url_netloc = full_link_url_obj.netloc,
            # url_path = full_link_url_obj.path,
            # url_params = full_link_url_obj.params,
            # url_query = full_link_url_obj.query,
            # url_fragment = full_link_url_obj.fragment,
            # url_hostname = full_link_url_obj.hostname,
            # url_port = full_link_url_obj.port,
            title = "Zoomable Treemap",
            upload_file = "", # file path to where the uploaded file is stored
            article_type=type_tutorial,
            about="Cool data representation using javascript and D3js",
            created_by = secondary_user,
            last_updated_by = secondary_user)

# session.add(art2)
# session.commit()

art2 = createArticleIfNotExists(art2)


tag1 = Tags(tag_name ="javascript")
session.add(tag1)
session.commit()

tag2 = Tags(tag_name ="json")
session.add(tag2)
session.commit()

tag3 = Tags(tag_name ="programming")
session.add(tag3)
session.commit()

tag4 = Tags(tag_name ="d3js")
session.add(tag4)
session.commit()

tag5 = Tags(tag_name ="web development")
session.add(tag5)
session.commit()

tag6 = Tags(tag_name ="visualization")
session.add(tag6)
session.commit()

tag7 = Tags(tag_name ="treemap")
session.add(tag7)
session.commit()

art_tag1 = Article_Tags(article=art1, tag=tag1)
session.add(art_tag1)
session.commit()

art_tag2 = Article_Tags(article=art1, tag=tag2)
session.add(art_tag2)
session.commit()

art_tag3 = Article_Tags(article=art1, tag=tag3)
session.add(art_tag3)
session.commit()

art_tag4 = Article_Tags(article=art1, tag=tag5)
session.add(art_tag4)
session.commit()

art_tag5 = Article_Tags(article=art2, tag=tag1)
session.add(art_tag5)
session.commit()

art_tag6 = Article_Tags(article=art2, tag=tag2)
session.add(art_tag6)
session.commit()

art_tag7 = Article_Tags(article=art2, tag=tag3)
session.add(art_tag7)
session.commit()

art_tag8 = Article_Tags(article=art2, tag=tag4)
session.add(art_tag8)
session.commit()

art_tag9 = Article_Tags(article=art2, tag=tag5)
session.add(art_tag9)
session.commit()

art_tag10 = Article_Tags(article=art2, tag=tag6)
session.add(art_tag10)
session.commit()

art_tag11 = Article_Tags(article=art2, tag=tag7)
session.add(art_tag11)
session.commit()

