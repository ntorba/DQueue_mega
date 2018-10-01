from app import app, db
from app.models import User, Party, Song

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User': User, 'Party': Party, 'Song':Song}
