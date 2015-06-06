# routing.py

from session_setup import *
from helper import *

@app.route('/')
@app.route('/articles')
@app.route('/articles/')
def articlesLinkPage():
    """ Main page:
        Find all articles
        List the 10 most popular tags
        generate a list of display content (Article_Display_Content objects)
    """

    print("Passed parameters are {0} and {1}".format(request.args.get('isthisworking'), request.args.get('testing')))
    article_types_list = session.query(Article_Type).all()
    # Get the 10 most popular tags
    most_popular_tags_list = getMostPopularTags()
    # # generate art_content, art name, art link, art artist name, tags created_by, last_updated_by
    kwargs = {"article_id":None, "article_type_id":None, "tag_id":None}
    article_display_content = getArticleDisplayContent(**kwargs)
    return render_template('index.html',
                            most_popular_tags_list=most_popular_tags_list,
                            article_types_list = article_types_list,
                            article_display_content=article_display_content)



@app.route('/articles/<int:type_id>/<int:article_id>/')
def articleInformation(type_id, article_id):
    """ Display Article Information for one article
        Find the article
        Find its associated tags from the Article_Tags table
    """
    article = session.query(Article).filter_by(id = article_id).one()
    article_type = session.query(Article_Type).filter_by(id=type_id).one()
    tags = session.query(Tags).filter(Article_Tags.article_id==article_id).filter(Article_Tags.tag_id==Tags.id).all()
    tag_list = []
    # for t in tags:
    #     tag_list.append(t.tag_name)
    comments = session.query(Comments).filter_by(article_id=article.id).all()
    return render_template('article_info.html', article_type = article_type,
                            article = article, tag_list = tags, comments_list=comments)



@app.route('/articles/type/<int:type_id>/')
def articlesByType(type_id):
    """ Dispaly all articles for a given type
        Article Display Content list generated based on the article type
    """
    kwargs = {"article_id":None, "article_type_id":type_id, "tag_id":None}
    article_display_content = getArticleDisplayContent(**kwargs)
    article_type = session.query(Article_Type).filter_by(id=type_id).one()
    return render_template('articles_by_type.html',
                            article_type = article_type,
                            article_display_content=article_display_content)



@app.route('/articles/tags/<int:tag_id>')
def articlesByTag(tag_id):
    """ Display all articles for a given tag
        Article Display Content list generated based on the article tag
    """
    kwargs = {"article_id":None, "article_type_id":None, "tag_id":tag_id}
    article_display_content = getArticleDisplayContent(**kwargs)
    tag = session.query(Tags).filter_by(id = tag_id).one()
    return render_template('articles_by_tag.html', tag = tag,
                            article_display_content=article_display_content)



@app.route('/articles/new', methods=['GET', 'POST'])
def addNewArticle():
    """ Add a new article, create the tags if not exist, and create article/tag pairs """
    if request.method == 'POST':
        new_article = Article(link=request.form['link'],
                             title=request.form['title'],
                             upload_file=None, # file path to where the uploaded file is stored
                             article_type=createTypeIfNotExists(request.form['type']),
                             about=request.form['about'],
                             created_by = None,
                             last_updated_by = None)
        print("The new article's link is: {}".format(new_article.link))
        create_article = createArticleIfNotExists(new_article)
        print("The article is: {0}".format(create_article.id))
        print("The article tags are: {0}".format(request.form['tags']))
        articleTagPairs(create_article, request.form['tags'])
        return redirect(url_for('articlesLinkPage'))
    else:
        return render_template('new_article.html')


@app.route('/articles/<int:article_id>/comments/new', methods=['GET', 'POST'])
def addNewComment(article_id):
    """ Add a new article, create the tags if not exist, and create article/tag pairs """
    article_to_comment = session.query(Article).filter_by(id=article_id).first()
    if request.method == 'POST':
        print("Inside post")
        print("Article in question: {}".format(article_to_comment.title))
        new_comment = Comments(text=request.form['comment_text'],
                                user=None,
                                article=article_to_comment)
        print("The new comment is: {}".format(new_comment))
        session.add(new_comment)
        session.commit()
        print("committed to session")
        return redirect(url_for('articlesLinkPage', testing=0, isthisworking=0))
    else:
        return render_template('new_comment.html', article=article_to_comment)



@app.route('/articles/type/new', methods=['GET', 'POST'])
def addNewArticleType():
    """ Add new article type - only available to admin """
    if request.method == 'POST':
        createTypeIfNotExists(request.form['name'])
        return redirect(url_for('articlesLinkPage'))
    else:
        return render_template('new_article_type.html')



@app.route('/articles/tag/new', methods=['GET', 'POST'])
def addNewArticleTag():
    """ Add new article tag - only available to admin """
    if request.method == 'POST':
        createTagIfNotExists(request.form['name'])
        return redirect(url_for('articlesLinkPage'))
    else:
        return render_template('new_article_tag.html')



@app.route('/articles/<int:article_id>/edit', methods=['GET','POST'])
def editArticle(article_id):
    """ Edit article - update article information. """
    editArticle = session.query(Article).filter_by(id=article_id).one()
    if request.method == 'POST':
        # Update the article information as per the edit form
        # Update the 'title' if user has changed it
        if len(request.form['title']) > 0:
            editArticle.title = request.form['title']
        # Update the 'about' section if the user has changed it
        if len(request.form['about']) > 0:
            editArticle.about = request.form['about']
        # Update the 'last updated by' to the user who just edited the entry
        editArticle.last_updated_by = None
        session.add(editArticle)
        session.commit()
        # Update the tags if changed
        if len(request.form['tags']) > 0:
            # find all tags associated with the Article ie the article/tag pairs
            kwargs = {"article_id":article_id, "tag_id":None}
            deleteArticleTagPairs(**kwargs)
            # create article/tag pairs as per specified in the edit form
            articleTagPairs(article=editArticle,tags=request.form['tags'])
        return redirect(url_for('articlesLinkPage'))
    else:
        return render_template('edit_article.html', article = editArticle)



@app.route('/articles/type/<int:article_type_id>/delete', methods=['GET', 'POST'])
def deleteArticleType(article_type_id):
    delete_article_type = session.query(Article_Type).filter_by(id=article_type_id).first()
    if request.method == 'POST':
        articles = session.query(Article).filter_by(article_type_id=article_type_id).all()
        for art in articles:
            deleteArticleFromDB(art)
        session.delete(delete_article_type)
        session.commit()
        return redirect(url_for('articlesLinkPage'))
    else:
        return render_template('delete_article_type.html', article_type = delete_article_type)



@app.route('/articles/tag/<int:tag_id>/delete', methods=['GET', 'POST'])
def deleteArticleTag(tag_id):
    delete_article_tag = session.query(Tags).filter_by(id=tag_id).first()
    if request.method == 'POST':
        kwargs = {"article_id":None, "tag_id":tag_id}
        deleteArticleTagPairs(**kwargs)
        session.delete(delete_article_tag)
        session.commit()
        return redirect(url_for('articlesLinkPage'))
    else:
        return render_template('delete_tag.html', tag = delete_article_tag)


@app.route('/articles/<int:article_id>/delete', methods=['GET','POST'])
def deleteArticle(article_id):
    """ Delete article - remove the article/tag pairs, but we don't delete the tags """
    delete_article = session.query(Article).filter_by(id=article_id).one()
    if request.method == 'POST':
        deleteArticleFromDB(delete_article)
        return redirect(url_for('articlesLinkPage'))
    else:
        return render_template('delete_article.html', article = delete_article)


@app.route('/articles/api/json')
def articlesAPIJSON():
    articles = session.query(Article).all()
    return jsonify(ArticlesList = [article.serialize for article in articles])


@app.route('/articles/<int:article_id>/api/json')
def articlesByIDAPIJSON(article_id):
    articles = session.query(Article).filter_by(id = article_id).all()
    return jsonify(ArticlesList = [article.serialize for article in articles])


@app.route('/articles/tags/api/json')
def articleTagPairsAPIJSON():
    article_tag_pairs = session.query(Article_Tags).all()
    return jsonify(ArticlesTagsAllList = [article_tag.serialize for article_tag in article_tag_pairs])


@app.route('/articles/<int:article_id>/tags/api/json')
def articleTagPairByIDAPIJSON(article_id):
    article_tag_pairs = session.query(Article_Tags).filter_by(id = article_id).all()
    return jsonify(ArticlesTagsList = [article_tag.serialize for article_tag in article_tag_pairs])


@app.route('/articles/<int:article_id>/comments/api/json')
def articleCommentsByIDAPIJSON(article_id):
    comments = session.query(Comments).filter_by(article_id = article_id).all()
    return jsonify(CommentsForArticle= [comment.serialize for comment in comments])
