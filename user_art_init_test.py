from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Art, User, Base

engine = create_engine('sqlite:///art_link_database.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

primary_user = User(user_name="admin",
                    user_image="admin.jpg",
                    user_email="pshevade@gmail.com",
                    is_admin=True)

session.add(primary_user)
session.commit()

secondary_user = User(user_name="foo",
                    user_image="foo.jpg",
                    user_email="foo@foobaifoo.com",
                    is_admin=False)

session.add(secondary_user)
session.commit()

art1 = Art( title = "test_art",
            artist_name = "prasanna",
            ratings = 5,
            link = "http://www.google.com",
            upload_file = "", # file path to where the uploaded file is stored
            art_type = "post-modern",
            created_by = primary_user,
            last_updated_by = primary_user)

session.add(art1)
session.commit()

