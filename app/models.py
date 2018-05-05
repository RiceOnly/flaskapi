from app import db


class Doctor(db.Model):
    """
    Doctor Model that sqlAlchemy links to the table found in database
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<Doctors Name {}>'.format(self.name)


class Review(db.Model):
    """
    Review Model that sqlAlchemy links to the table found in database
    """
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    description = db.Column(db.String(140))

    def __repr__(self):
        return '<Review Description {}>'.format(self.description)
