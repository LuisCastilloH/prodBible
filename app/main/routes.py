from datetime import datetime
from copy import deepcopy

from flask import g, current_app
from flask import jsonify
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language

from app import db
# from app.main.forms import EditProfileForm, PostForm
from app.models import Bible, User, Bookmark
from app.main import bp
from config import versions

text = Bible()
parallelFlag = False

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    text2 = text.displayText()
    verses = text2[2]
    return render_template('index.html', title=_('Home'), 
            text=text2, verses=verses)

@bp.route('/version')
def version():
    versions2 = versions
    return render_template('index.html', title=_('Home'),
            text=None, verses=None, versions=versions2)

@bp.route('/explore')
def explore():
    books = text.listOfBooks()
    return render_template('index.html', title=_('Home'), 
            text=None, verses=None, books=books)

@bp.route('/parallel')
def parallel():
    # display a parallel Bible version 
    # input = <chosen version>
    currentBook = text.getCurrentBook()
    currentChapter = text.getCurrentChapter()
    textVersion1 = text.displayText(currentBook, int(currentChapter))
    verses = textVersion1[2]
    global parallelFlag
    if parallelFlag:
        parallelFlag = False
        return render_template('index.html', title=_('Home'), 
                text=textVersion1, verses=verses)
    else:
        parallelFlag = True
        secondText = deepcopy(text)
        secondText.changeVersion('reinaValera')
        textVersion2 = secondText.displayText(currentBook, int(currentChapter))
        verses2 = textVersion2[2]
        return render_template('index.html', title=_('Home'),text=textVersion1,
            text2=textVersion2, verses=verses, verses2=verses2, 
            parallel=parallelFlag)


@bp.route('/explore/<book>')
def exploreBook(book):
    chapters = text.listOfChapters(book)
    return render_template('index.html', title=_('Home'), 
            text=None, verses=None, book=book, chapters=chapters)
 
@bp.route('/explore/<book>/<chapter>')
def exploreChapter(book, chapter):
    textVersion1 = text.displayText(book, int(chapter))
    verses = textVersion1[2]
    global parallelFlag
    if not parallelFlag:
        return render_template('index.html', title=_('Home'), 
                text=textVersion1, verses=verses)
    else:
        secondText = deepcopy(text)
        secondText.changeVersion('reinaValera')
        textVersion2 = secondText.displayText(book, int(chapter))
        verses2 = textVersion2[2]
        return render_template('index.html', title=_('Home'),text=textVersion1,
            text2=textVersion2, verses=verses, verses2=verses2, 
            parallel=parallelFlag)

@bp.route('/version/<version>')
def changeVersion(version):
    currentBook = text.getCurrentBook()
    currentChapter = text.getCurrentChapter()
    text.changeVersion(version)
    text2 = text.displayText(currentBook, int(currentChapter))
    verses = text2[2]
    global parallelFlag
    parallelFlag = False
    return render_template('index.html', title=_('Home'),
            text=text2, verses=verses)


@bp.route('/user/<username>')
@login_required
def user(username):
    return 'user'
    # user = User.query.filter_by(username=username).first_or_404()
    # page = request.args.get('page', 1, type=int)
    # posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        # page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('main.user', username=user.username, 
            # page=posts.next_num) if posts.has_next else None
    # prev_url = url_for('main.user', username=user.username, 
            # page=posts.prev_num) if posts.has_prev else None
    # return render_template('user.html', user=user, posts=posts.items,
            # next_url=next_url, prev_url=prev_url)

# @bp.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
    # form = EditProfileForm(current_user.username)
    # if form.validate_on_submit():
        # current_user.username = form.username.data
        # current_user.about_me = form.about_me.data
        # db.session.commit()
        # flash(_('Your changes have been saved.'))
        # return redirect(url_for('main.edit_profile'))
    # elif request.method == 'GET':
        # form.username.data = current_user.username
        # form.about_me.data = current_user.about_me
    # return render_template('edit_profile.html', title=_('Edit Profile'),
                            # form=form)

# @bp.route('/follow/<username>')
# @login_required
# def follow(username):
    # user = User.query.filter_by(username=username).first()
    # if user is None:
        # flash(_('User %(username)s not found.', username=username))
        # return redirect(url_for('main.index'))
    # if user == current_user:
        # flash(_('You cannot follow yourself!'))
        # return redirect(url_for('main.user', username=username))
    # current_user.follow(user)
    # db.session.commit()
    # flash('You are following {}!'.format(username))
    # return redirect(url_for('main.user', username=username))

# @bp.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
    # user = User.query.filter_by(username=username).first()
    # if user is None:
        # flash('User {} not found.'.format(username))
        # return redirect(url_for('main.index'))
    # if user == current_user:
        # flash('You cannot unfollow yourself!')
        # return redirect(url_for('main.user', username=username))
    # current_user.unfollow(user)
    # db.session.commit()
    # flash('You are not following {}.'.format(username))
    # return redirect(url_for('main.user', username=username))

# @bp.route('/translate', methods=['POST'])
# @login_required
# def translate_text():
    # return jsonify({'text': translate(request.form['text'],
                                      # request.form['source_language'],
                                      # request.form['dest_language'])})

