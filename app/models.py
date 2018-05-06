from datetime import datetime
from hashlib import md5
from json import loads
from time import time
from re import sub
from os import path

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from flask import current_app

from app import db
from app import login
from config import versions

def loadJSONBible(version):
    temp = dict()
    bookNames = list()
    filePath = path.abspath(''.join((version, '.json')))
    with open(filePath, 'rb') as f:
        data = f.read().decode('UTF-8')
    # cleaning of json string
    data = sub('^[^\[]*', '', data)
    jsonData = loads(data)
    for book in jsonData:
        temp[book['name']] = book
        bookNames.append(book['name'])
    return temp, bookNames

class Bible(object):
    """Main class, displays the Bible and other functionalities"""
    def __init__(self, version=versions['kings'], book='Genesis', chapter=1):
        self.version = version
        self.text, self.bookNames = loadJSONBible(self.version)
        self.book = book
        self.chapter = chapter
        self.verse = None

    def changeVersion(self, version):
        self.version = versions[version]
        self.text, self.bookNames = loadJSONBible(self.version)

    def displayText(self, book='Genesis', chapter=1, verse=None, version=None):
        self.book = book
        self.chapter = chapter
        if version:
            text, bookNames = loadJSONBible(version)
        else:
            text = self.text
            bookNames = self.bookNames
        if verse:
            self.verse = verse
            return (self.book, self.chapter,
                text[self.book]['chapters'][self.chapter-1][self.verse-1])
        return (self.book, self.chapter,
                text[self.book]['chapters'][self.chapter-1])

    def getCurrentBook(self):
        return self.book

    def getCurrentChapter(self):
        return self.chapter

    def getCurrentVerse(self):
        return self.verse

    def getCurrentVersion(self):
        return self.version

    def listOfBooks(self):
        return self.bookNames

    def listOfChapters(self, book):
        return len(self.text[book]['chapters'])

    def listOfVersions(self):
        return versions

    def searchKeywords(self, keywords):
        # implement a function of searching
        pass

    def displayVersesList(self):
        # possible function to show results of searchKeywords function
        pass
        
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bookmarks = db.relationship('Bookmark', backref='author', lazy='dynamic')
    lastBookViewed = db.Column(db.String(64))
    lastChapterViewed = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_bookmarks(self):
        bookmarks = Bookmark.query.filter_by(user_id=self.id)
        return bookmarks.order_by(Bookmark.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in },
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                    algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(64))
    chapter = db.Column(db.String(64))
    verses = db.Column(db.String(64))
    version = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Bookmark {} {}:{}>'.format(self.book, self.chapter,
                                            self.verses)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
