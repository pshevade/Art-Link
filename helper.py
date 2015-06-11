# article_link_page helper functions
from session_setup import *
from urlparse import urlparse

class Article_Display_Content():
    """ This class combines the relevant article information to display
        to the front end. We must find the article, its type, and the tags
        associated with it from the database to build an object of this class.
    """
    def __init__(self, article, article_type, tags):
        self.article = article
        self.article_type = article_type
        self.tags = tags

    @property
    def serialize(self):
        return {
                'Article'   : self.article.serialize,
                'Article_Type': self.article_type.name,
                'Tags'      : [tag.serialize for tag in self.tags],
        }


def createTagIfNotExists(name):
    """ Create the tag as specified by the name, only if it doesn't already exist
        in the Tags table.
        returns: the tag object of either the existing tag or the newly created tag
    """
    # Check if tag exists in the Tags table
    tag_exists = session.query(Tags).filter_by(tag_name=name).first()
    if tag_exists:
        flash('This article tag exists')
        return tag_exists
    else:
        # Create a new tag as per the name attribute
        newTag = Tags(tag_name=name)
        session.add(newTag)
        session.commit()
        print(newTag.tag_name)
        return newTag


def createTypeIfNotExists(name):
    """ Create the article type as specified by the name, only if it doesn't
        already exist in the Article_Type table.
        returns: the article_type object of either the existing tag or the newly created type
    """
    # Check if article type exists in the Article_Type table
    type_exists = session.query(Article_Type).filter_by(name=name).first()
    if type_exists:
        flash('This article type exists')
        return type_exists
    else:
        # Create a new article type per the name attribute
        newType = Article_Type(name=name)
        session.add(newType)
        session.commit()
        return newType


def createArticleIfNotExists(new_article):
    """ Create a new article as specified by the new article attribute, only if
        it's link doesn't exist in the Article table.
        returns: the article object
    """
    # Check if article type exists in the Article_Type table
    print("In createArticleIfNotExists")
    #print("Article link scheme: {}".format(new_article.scheme))
    new_article = parseArticleURL(new_article)
    print("Article link scheme post parse: {}".format(new_article.url_scheme))
    print("The article searchable link: {}".format(new_article.searchable_link))
    article_exists = session.query(Article).filter_by(searchable_link=new_article.searchable_link).first()
    #print("The article_exists object has a link: {0}".format(article_exists.link))
    print("The new_article object has a link: {0}".format(new_article.link))
    if article_exists:
        print("The article exists")
        print("The article exists: {0}, {1}".format(article_exists.title, article_exists.id))
        #flash('This article exists!')
        return article_exists
    else:
        print("The article doesn't exist")
        session.add(new_article)
        session.commit()
        return new_article


def parseArticleURL(article):
    print("The article link before any parsing, raw is: {}".format(article.link))
    link_url_obj = urlparse(article.link)
    if link_url_obj.scheme is '':
        article.link + 'http://'+article.link
        link_url_obj = urlparse(article.link)
        print("ParseArticleURL - updated the link - the link scheme is: {}".format(link_url_obj.scheme))
    else:
        print("ParseArticleURL - the link scheme is: {}".format(link_url_obj.scheme))


    article.url_scheme = link_url_obj.scheme
    article.url_netloc = link_url_obj.netloc
    article.url_path = link_url_obj.path
    article.url_params = link_url_obj.params
    article.url_query = link_url_obj.query
    article.url_fragment = link_url_obj.fragment
    article.url_hostname = link_url_obj.hostname
    article.url_port = link_url_obj.port
    article.searchable_link = link_url_obj.geturl()[len(link_url_obj.scheme)+3 : ]

    return article



def articleTagPairs(article, tags):
    """ Create the article,tag pairs for a given article and tags
        The tags attribute is a string of tags, comma separated
        This function calls the createTagIfNotExists to create the tag object for
        each of the tags in the 'tags' string and then calls the
        createArticleTagPairs with the tag object and the article
    """
    # Create a list of tags by splitting the tags string attribute
    print("Article id in articleTagPairs: {0}".format(article.id))
    tag_list = tags.split(',')
    for tag_name in tag_list:
        tag_obj=createTagIfNotExists(tag_name)
        createArticleTagPairs(tag_obj, article)


def createArticleTagPairs(tag, article):
    """ Create the article,tag pairs in the Article_Tags table
        and commit to the database """
    new_article_tag_pair = Article_Tags(article=article, tag=tag)
    session.add(new_article_tag_pair)
    session.commit()


def getMostPopularTags():
    """ Parse through all tags and find the top ten most popular
        (most frequently used) tags
        returns: list of Tags objects
    """
    # Get the tags for all articles by the count -> pair them as (tag_id, count)
    article_tags_count = session.query(Article_Tags.tag_id, func.count(Article_Tags.tag_id)).group_by(Article_Tags.tag_id)
    tags_list = []

    # for each (tag_id,count) pair, find the tag corresponding to that tag_id
    for el in article_tags_count:
        tag = session.query(Tags).filter_by(id=el[0]).first()
        # create a (tag,count) pair
        tags_list.append((tag, el[1]))

    # sort the list of (tag,count) pairs by the count
    tags_list.sort(key=lambda tup:tup[1])
    # reverse list to get the most frequently appearing tags first
    tags_list.reverse()
    # unzip the list of tuples (tag,count) to only get the tags
    most_popular_tags_list = zip(*tags_list[:10])[0]

    # Return a list of Tags objects
    return most_popular_tags_list


def getArticleDisplayContent(article_id=None, article_type_id=None, tag_id=None):
    """ This function creates a list of the Article_Display_Content objects,
        to display to the front end.
        The list of the articles/type/tags is composed based on either a particular
        article, type, or tag (front end filtering) or for ALL articles
        return: list of Article_Display_Content objects
    """
    article_display_content = []
    # Retrieve articles based on the passed parameter
    if article_id:
        articles = session.query(Article).filter_by(id = article_id).one()
    elif article_type_id:
        articles = session.query(Article).filter_by(article_type_id = article_type_id).all()
    elif tag_id:
        articles = session.query(Article).filter(Article_Tags.tag_id == tag_id).filter(Article_Tags.article_id == Article.id).all()
    else:
        articles = session.query(Article).all()
    # For each article, find the article type object and the tags list
    for article in articles:
        article_type = session.query(Article_Type).filter_by(id=article.article_type_id).one()
        tags = session.query(Tags).filter(Article_Tags.article_id==article.id).filter(Article_Tags.tag_id==Tags.id).all()
        article_display_content.append(Article_Display_Content(article, article_type, tags))
    return article_display_content


# def getArticleDisplayContentJSON(article_id=None, article_type_id=None, tag_id=None):
#     """ This function creates a list of the Article_Display_Content objects,
#         to display to the front end.
#         The list of the articles/type/tags is composed based on either a particular
#         article, type, or tag (front end filtering) or for ALL articles
#         return: list of Article_Display_Content objects
#     """
#     article_display_content = []
#     # Retrieve articles based on the passed parameter
#     if article_id:
#         articles = session.query(Article).filter_by(id = article_id).one()
#     elif article_type_id:
#         articles = session.query(Article).filter_by(article_type_id = article_type_id).all()
#     elif tag_id:
#         articles = session.query(Article).filter(Article_Tags.tag_id == tag_id).filter(Article_Tags.article_id == Article.id).all()
#     else:
#         articles = session.query(Article).all()
#     # For each article, find the article type object and the tags list
#     for article in articles:
#         article_type = session.query(Article_Type).filter_by(id=article.article_type_id).one()
#         tags = session.query(Tags).filter(Article_Tags.article_id==article.id).filter(Article_Tags.tag_id==Tags.id).all()
#         article_display_content.append(Article_Display_Content(article, article_type, tags))
#     return jsonify(article_display_content_json = [content.serialize for content in article_display_content])
   


def deleteArticleTagPairs(article_id, tag_id):
    """ Delete article,tag pairs
        Search by either article_id or tag_id
    """
    if article_id:
        article_tags = session.query(Article_Tags).filter(Article_Tags.article_id==article_id).all()
    elif tag_id:
        article_tags = session.query(Article_Tags).filter(Article_Tags.tag_id==tag_id).all()
    else:
        article_tags = None
    # delete all article/tag pairs
    for pair in article_tags:
        session.delete(pair)
        session.commit()


def deleteArticleFromDB(delete_article):
    kwargs = {"article_id":delete_article.id, "tag_id":None}
    deleteArticleTagPairs(**kwargs)
    session.delete(delete_article)
    session.commit()


# def parseLink(raw_link):
#     if raw_link.rfind('http://') == 0:
#         link = raw_link[len('http://'):]
#     elif raw_link.rfind('https://')== 0:
#         link = raw_link[len('https://'):]
#     return link
