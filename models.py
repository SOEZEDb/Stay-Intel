from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Intel(db.Model):
    __tablename__ = 'Stayintel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    link = db.Column(db.String)
    provisions = db.Column(db.String)
    rating = db.Column(db.Float)

    categories = db.relationship('Category', backref='intel', lazy='dynamic')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    intel_id = db.Column(db.Integer, db.ForeignKey('Stayintel.id'))
