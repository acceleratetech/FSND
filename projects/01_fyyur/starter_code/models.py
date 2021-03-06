from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, nullable=False, autoincrement="auto", primary_key=True)
  start_time = db.Column(db.DateTime(timezone=True), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
  venue = db.relationship('Venue', backref='shows')
  artist = db.relationship('Artist', backref='shows')

class Venue(db.Model):
  __tablename__ = 'venue'

  id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
  name = db.Column(db.String, nullable=False, unique=True)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String()), nullable=False)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean, nullable=False, default=True)
  seeking_description = db.Column(db.String())

# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
  name = db.Column(db.String, nullable=False, unique=True)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String()), nullable=False)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, nullable=False, default=True)
  seeking_description = db.Column(db.String())

# TODO: implement any missing fields, as a database migration using Flask-Migrate
