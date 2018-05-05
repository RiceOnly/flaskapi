from app import app, db
from app.models import Doctor, Review


@app.shell_context_processor
def make_shell_context():
    """
    When flask shell is ran, these variables can be used without having to import them
    :return:
    """
    return {'db': db, 'Doctor': Doctor, 'Review': Review}

