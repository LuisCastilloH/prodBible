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
parallelFlag = 0
userLogged = 0

@bp.before_app_request
def before_request():
    global userLogged
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        userLogged = 1
    else:
        userLogged = 0
    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    global userLogged
    if current_user.is_authenticated:
        userLogged = 1
    else:
        userLogged = 0
    text2 = text.displayText()
    verses = text2[2]
    return render_template('index.html', title=_('Home'), 
            text=text2, verses=verses, userStatus=userLogged)

@bp.route('/version')
def version():
    versions2 = versions
    return render_template('index.html', title=_('Home'),
            text=None, verses=None, versions=versions2, userStatus=userLogged)

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
    # import pdb; pdb.set_trace()
    global parallelFlag
    if parallelFlag:
        parallelFlag = 0
        return render_template('index.html', title=_('Home'), 
                text=textVersion1, verses=verses, userStatus=userLogged)
    else:
        parallelFlag = 1
        secondText = deepcopy(text)
        secondText.changeVersion('reinaValera')
        textVersion2 = secondText.displayText(currentBook, int(currentChapter))
        verses2 = textVersion2[2]
        return render_template('index.html', title=_('Home'),text=textVersion1,
            text2=textVersion2, verses=verses, verses2=verses2, 
            parallel=parallelFlag, userStatus=userLogged)


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
                text=textVersion1, verses=verses, userStatus=userLogged)
    else:
        secondText = deepcopy(text)
        secondText.changeVersion('reinaValera')
        textVersion2 = secondText.displayText(book, int(chapter))
        verses2 = textVersion2[2]
        return render_template('index.html', title=_('Home'),text=textVersion1,
            text2=textVersion2, verses=verses, verses2=verses2, 
            parallel=parallelFlag, userStatus=userLogged)

@bp.route('/version/<version>')
def changeVersion(version):
    currentBook = text.getCurrentBook()
    currentChapter = text.getCurrentChapter()
    text.changeVersion(version)
    text2 = text.displayText(currentBook, int(currentChapter))
    verses = text2[2]
    global parallelFlag
    parallelFlag = 0
    return render_template('index.html', title=_('Home'),
            text=text2, verses=verses, userStatus=userLogged)

@bp.route('/bookmark/<bk>/<chp>/<vrs>')
@login_required
def bookmark(bk, chp, vrs):
    currVersion = text.getCurrentVersion()
    bookmark = Bookmark(book=bk, chapter=chp, verses=vrs, version=currVersion,
                        author=current_user)
    db.session.add(bookmark)
    db.session.commit()
    flash('Your bookmark is now saved!')
    text2 = text.displayText(bk, int(chp), int(vrs))
    verses2 = text2[2]
    return render_template('index.html', title=_('Home'),text=text2,
            verses=verses2, bookmark=1, vrs=int(vrs))

@bp.route('/listBookmarks')
@login_required
def listBookmarks():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    bookmarks = user.bookmarks.order_by(Bookmark.timestamp.desc())
    listBk = list()
    for bk in bookmarks:
        listBk.append((text.displayText(bk.book, int(bk.chapter), 
        int(bk.verses), version=bk.version), bk.version, int(bk.verses),
        bk.timestamp))
    return render_template('index.html', title=_('Home'), lsBk=listBk)

@bp.route('/user/<username>')
@login_required
def user(username):
    return render_template('index.html', title=_('Home'), 
        userName=current_user.username, userEmail=current_user.email)



