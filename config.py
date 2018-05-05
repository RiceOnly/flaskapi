class Config():
    """
    Hold the configurations used by flask
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
