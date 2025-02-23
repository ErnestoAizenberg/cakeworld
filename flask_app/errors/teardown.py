from flask import g

from flask_app import app

@app.teardown_appcontext
def close_connection(exception=None):
    """Closes the database connection at the end of each request."""
    if 'db' in g:
        db = g.pop('db')
        db.close()