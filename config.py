# @author Luis Castillo

'''
Configuration file for Flask application
2018-2021
'''

import os
from os.path    import abspath
from os.path    import join
from dotenv     import load_dotenv

basedir = abspath(os.path.dirname(__file__))
load_dotenv(join(basedir, '.env'))

versions = {'kings': 'kjv',
            'reinaValera': 'rvr'}

class Config():
    '''
    Environment variables. Prepared for online hosting or dev hosting
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        ('postgres://{}:{}@{}:{}/{}').format('postgres', 'barney', 'localhost',
        '5432', 'app')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['luis.castillo.h@outlook.com']
    POSTS_PER_PAGE = 25
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
