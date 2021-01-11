#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
from models import db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

# TODO: connect to a local postgresql database
# DONE: connected to local database "fyyur" specified in the config file

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  #print(f"Parser value is {value}")
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.state, Venue.city).all()
  for place in places:
    data.append({
      'city': place.city,
      'state': place.state,
      'venues': [{
        'id': venue.id,
        'name': venue.name,
      } for venue in venues if (
        venue.city == place.city and venue.state == place.state
      )]
    })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term')
  #print(f"Venues search request: {search_term}")
  search = db.session.query(Venue).filter(Venue.name.ilike("%"+search_term+"%")).all()
  #print(f"Venue search: {search}")
  data = []
  for item in search:
    num_upcoming_shows = db.session.query(Show).join(Venue, Show.venue_id==Venue.id).filter(Show.start_time>datetime.now()).count()
    temp = {
      "id": item.id,
      "name": item.name,
      "num_upcoming_shows": num_upcoming_shows
    }
    data.append(temp)

  response = {
    "count": len(search),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  past_shows = db.session.query(Artist, Show).join(Show).join(Venue)\
    .filter(
      Show.venue_id == venue_id,
      Show.artist_id == Artist.id,
      Show.start_time < datetime.now()
    ).all()

  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue)\
  .filter(
    Show.venue_id == venue_id,
    Show.artist_id == Artist.id,
    Show.start_time > datetime.now()
  ).all()

  past_shows_count = len(past_shows)
  upcoming_shows_count = len(upcoming_shows)

  venue_detail = db.session.query(Venue).filter(Venue.id==venue_id).first_or_404()

  venue_data = {
    "id": venue_detail.id,
    "name": venue_detail.name,
    "genres": venue_detail.genres,
    "address": venue_detail.address,
    "city": venue_detail.city,
    "state": venue_detail.state,
    "phone": venue_detail.phone,
    "website": venue_detail.website,
    "facebook_link": venue_detail.facebook_link,
    "seeking_talent": venue_detail.seeking_talent,
    "seeking_description": venue_detail.seeking_description,
    "image_link": venue_detail.image_link,
    "past_shows": [{
      'artist_id': artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
      } for artist, show in past_shows],
    "upcoming_shows": [{
        'artist_id': artist.id,
        'artist_name': artist.name,
        'artist_image_link': artist.image_link,
        'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
      } for artist, show in upcoming_shows],
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count
  }
  
  return render_template('pages/show_venue.html', venue=venue_data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form, meta={'csrf': False})

  if form.validate_on_submit():
    try:
      venue = Venue()
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully listed!')
    except ValueError as e:
      print(e)
      flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    message = []
    for field, errors in form.errors.items():
      message.append(field + ':, '.join(errors))
    flash(f'Errors: {message}')
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artists_all = db.session.query(Artist).order_by(Artist.id).all()
  #print(f"artists_all: {artists_all}")
  data = []
  for artist in artists_all:
    artist_data = {
      "id": artist.id,
      "name": artist.name
    }
    data.append(artist_data)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term')
  search = db.session.query(Artist).filter(Artist.name.ilike("%"+search_term+"%")).all()
  data = []

  for item in search:
    num_upcoming_shows = db.session.query(Show).join(Artist, Show.venue_id==Artist.id).filter(Show.start_time>datetime.now()).count()
    temp = {
      "id": item.id,
      "name": item.name,
      "num_upcoming_shows": num_upcoming_shows
    }
    data.append(temp)

  response = {
    "count": len(search),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  past_shows = db.session.query(Venue, Show).join(Show).join(Artist)\
    .filter(
      Show.venue_id == Venue.id,
      Show.artist_id == artist_id,
      Show.start_time < datetime.now()
    ).all()

  upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist)\
  .filter(
    Show.venue_id == Venue.id,
    Show.artist_id == artist_id,
    Show.start_time > datetime.now()
  ).all()

  past_shows_count = len(past_shows)
  upcoming_shows_count = len(upcoming_shows)

  artist_detail = db.session.query(Artist).filter(Artist.id==artist_id).first_or_404()

  artist_data = {
    "id": artist_detail.id,
    "name": artist_detail.name,
    "genres": artist_detail.genres,
    "city": artist_detail.city,
    "state": artist_detail.state,
    "phone": artist_detail.phone,
    "website": artist_detail.website,
    "facebook_link": artist_detail.facebook_link,
    "seeking_talent": artist_detail.seeking_venue,
    "seeking_description": artist_detail.seeking_description,
    "image_link": artist_detail.image_link,
    "past_shows": [{
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
      } for venue, show in past_shows],
    "upcoming_shows": [{
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
      } for venue, show in upcoming_shows],
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count
  }

  return render_template('pages/show_artist.html', artist=artist_data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form, meta={'csrf': False})

  if form.validate_on_submit():
    try:
      artist = Artist()
      form.populate_obj(artist)
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + artist.name + ' was successfully listed!')
    except ValueError as e:
      print(e)
      flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    message = []
    for field, errors in form.errors.items():
      message.append(field + ':, '.join(errors))
    flash(f'Errors: {message}')
  
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  show_data = db.session.query(Show).join(Venue, Show.venue_id==Venue.id).join(Artist, Show.artist_id==Artist.id).all()
  data = []
  for show in show_data:
    temp = {
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist.id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
    }
    data.append(temp)
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form, meta={'csrf': False})

  if form.validate_on_submit():
    try:
      show = Show()
      form.populate_obj(show)
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except ValueError as e:
      print(e)
      flash('An error occurred. Show could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    message = []
    for field, errors in form.errors.items():
      message.append(field + ':, '.join(errors))
    flash(f'Errors: {message}')
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
  return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
