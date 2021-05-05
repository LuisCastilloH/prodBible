# @author Luis Castillo

'''
Configuration file for Flask application
2018-2021
'''

from app        import create_app
from app        import db
from app.models import User
from app.models import Bookmark
# from app import cli

app = create_app()
# cli.register(app)

@app.shell_context_processor
def make_shell_context():
    '''
    Shell context.
    '''
    return {'db': db, 'User': User, 'Bookmark': Bookmark}
