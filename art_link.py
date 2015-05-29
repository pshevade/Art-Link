# art_link.py

from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Art, Artist, Art_Artist, Tags, Art_Tags, Comments

engine = create_engine('sqlite:///art_link_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class Art_Display_Content():
    def __init__(self, art_id, art_link, art_title, rating, artist_name, created_by, last_updated_by,tag_list=[]):
        self.id = art_id
        self.art_link = art_link
        self.art_title = art_title
        self.artist_name = artist_name
        self.created_by = created_by
        self.last_updated_by = last_updated_by
        self.rating = rating
        self.tag_list = tag_list


@app.route('/')
@app.route('/art')
def artLinkPage():
    art_tags_freq_list = []
    art_tags_count = session.query(Art_Tags.tag_id, func.count(Art_Tags.tag_id)).group_by(Art_Tags.tag_id)
    print art_tags_count
    most_popular_tags_list = []

    for el in art_tags_count:
        #art_tags_freq_list.append(el)
        tag = session.query(Tags).filter_by(id=el[0]).one()
        most_popular_tags_list.append((tag.tag_name, el[1]))

    most_popular_tags_list.sort(key=lambda tup:tup[1])
    most_popular_tags_list.reverse()

    print most_popular_tags_list

    most_popular_tags_list = most_popular_tags_list[:10]

    # generate art_content, art name, art link, art artist name, tags created_by, last_updated_by
    art_display_content = []

    art = session.query(Art).all()

    art_info = session.query(Art.id, Art.link, Art.title, Art.ratings, Artist.name, User.user_name, User.user_name).\
                        filter(Art_Artist.art_id==Art.id).filter(Art_Artist.artist_id==Artist.id).\
                        filter(Art.created_by_id == User.id).filter(Art.last_updated_by_id == User.id).all()

    for e in art_info:
        print e
        tag_list=[]
        tags = session.query(Tags).filter(Art_Tags.art_id==e[0]).filter(Art_Tags.tag_id==Tags.id).all()
        for el in tags:
            tag_list.append(el.tag_name)
        print tag_list
        art_display_content.append(Art_Display_Content(e[0],e[1], e[2], e[3], e[4], e[5], e[6], tag_list=tag_list))

    # art_content = {}
    print "Display content:"
    print art_display_content[0].art_title


    return render_template('index.html', most_popular_tags_list=most_popular_tags_list, art_display_content=art_display_content)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
