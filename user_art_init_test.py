from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Art, Artist, Art_Artist, Art_Tags, Tags

engine = create_engine('sqlite:///art_link_database.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

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

art1 = Art( link="http://www.google.com",
            title = "test_art",
            upload_file = "", # file path to where the uploaded file is stored
            created_by = primary_user,
            last_updated_by = primary_user)

session.add(art1)
session.commit()

artist1 = Artist(name="Google")

session.add(artist1)
session.commit()

art_artist_pair1 = Art_Artist(art=art1, artist=artist1)

session.add(art_artist_pair1)
session.commit()

art2 = Art( link="http://www.Udacity.com",
            title = "test_art_two",
            upload_file = "", # file path to where the uploaded file is stored
            created_by = secondary_user,
            last_updated_by = secondary_user)

session.add(art2)
session.commit()

art_artist_pair2 = Art_Artist(art=art2, artist=artist1)
session.add(art_artist_pair2)
session.commit()

tag1 = Tags(tag_name ="name1")
session.add(tag1)
session.commit()

tag2 = Tags(tag_name ="name2")
session.add(tag2)
session.commit()

tag3 = Tags(tag_name ="name3")
session.add(tag3)
session.commit()

tag4 = Tags(tag_name ="name4")
session.add(tag4)
session.commit()

tag5 = Tags(tag_name ="name5")
session.add(tag5)
session.commit()

tag6 = Tags(tag_name ="name6")
session.add(tag6)
session.commit()

tag7 = Tags(tag_name ="name7")
session.add(tag7)
session.commit()

art_tag1 = Art_Tags(art=art1, tag=tag1)
session.add(art_tag1)
session.commit()

art_tag2 = Art_Tags(art=art1, tag=tag2)
session.add(art_tag2)
session.commit()

art_tag3 = Art_Tags(art=art1, tag=tag4)
session.add(art_tag3)
session.commit()

art_tag4 = Art_Tags(art=art1, tag=tag7)
session.add(art_tag4)
session.commit()

art_tag5 = Art_Tags(art=art2, tag=tag1)
session.add(art_tag5)
session.commit()

art_tag6 = Art_Tags(art=art2, tag=tag2)
session.add(art_tag6)
session.commit()

art_tag7 = Art_Tags(art=art2, tag=tag3)
session.add(art_tag7)
session.commit()

art_tag8 = Art_Tags(art=art2, tag=tag5)
session.add(art_tag8)
session.commit()

art_tag9 = Art_Tags(art=art2, tag=tag6)
session.add(art_tag9)
session.commit()

art_tag10 = Art_Tags(art=art2, tag=tag4)
session.add(art_tag10)
session.commit()

