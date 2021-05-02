#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import render_template, request, flash, redirect, url_for
from fyyur import app, db
from fyyur.forms import *
from fyyur.models import Artist, Venue, Show


#----------------------------------------------------------------------------#
# Routes
#----------------------------------------------------------------------------#

#  View Venues
#  -----------------------------------
@app.route('/venues')
def venues():
    # [DONE] TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    cities_and_states = Venue.query.distinct(Venue.city, Venue.state)\
        .with_entities(Venue.city, Venue.state)\
        .all()

    data = []

    for cas in cities_and_states:
        venues_in_cas = Venue.query.filter_by(
            city=cas.city, state=cas.state).all()
        data.append({
            "city": cas.city,
            "state": cas.state,
            "venues": [venue.serialize_venue_with_upcoming_shows for venue in venues_in_cas]
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # [DONE] TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    venues = Venue.query.filter(Venue.name.ilike(
        f"%{request.form.get('search_term')}%")).all()
    response = {
        "count": len(venues),
        "data": [venue.serialize_venue_with_upcoming_shows for venue in venues]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # [DONE] TODO: replace with real venue data from the venues table, using venue_id

    venue = Venue.query.filter_by(id=venue_id).first()

    all_shows = Show.query.with_entities(Show.artist_id, Show.start_time, Artist.image_link.label("artist_image_link"), Artist.name.label("artist_name"))\
        .filter(Show.venue_id == venue.id)\
        .join(Artist, Artist.id == Show.artist_id)\
        .all()

    past_shows = []
    upcoming_shows = []

    for show in all_shows:
        if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') < datetime.now():
            past_shows.append({
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": show.start_time,
            })
        else:
            upcoming_shows.append({
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": show.start_time,
            })

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)


#  Create, Edit & Delete Venues
#  -----------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # [DONE] TODO: insert form data as a new Venue record in the db, instead
    # [DONE] TODO: modify data to be the data object returned from db insertion

    data = request.values
    try:
        venue = Venue(
            name=data["name"],
            city=data["city"],
            state=data["state"],
            phone=data["phone"],
            genres=request.form.getlist("genres"),
            address=data["address"],
            facebook_link=data["facebook_link"],
            image_link=data["image_link"],
            website=data["website_link"],
            seeking_talent=bool(data.get("seeking_talent", False)),
            seeking_description=data["seeking_description"]
        )
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash(f'Venue {request.form["name"]} was successfully listed!')
        return redirect(url_for('venues'))
    except Exception as e:
        db.session.rollback()
        print(e)
        # [DONE] TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        flash(f'An error occurred. Venue  {data.name} could not be listed.')
        return redirect(url_for('create_venue_submission'))
    finally:
        db.session.close()


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(
        id=venue.id,
        name=venue.name,
        genres=venue.genres,
        address=venue.address,
        city=venue.city,
        state=venue.state,
        phone=venue.phone,
        website_link=venue.website,
        facebook_link=venue.facebook_link,
        seeking_talent=venue.seeking_talent,
        seeking_description=venue.seeking_description,
        image_link=venue.image_link
    )
    # [DONE] TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # [DONE] TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    data = request.values
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        venue.name = data["name"]
        venue.city = data["city"]
        venue.state = data["state"]
        venue.phone = data["phone"]
        venue.address = data["address"]
        venue.genres = request.form.getlist("genres")
        venue.facebook_link = data["facebook_link"]
        venue.image_link = data["image_link"]
        venue.website = data["website_link"]
        venue.seeking_talent = bool(data.get("seeking_talent", False))
        venue.seeking_description = data["seeking_description"]
        db.session.add(venue)
        db.session.commit()
        flash('Venue was updated successfully!')
        return redirect(url_for('show_venue', venue_id=venue_id))
    except Exception as e:
        db.session.rollback()
        print(e)
        flash('Updating the venue failed.')
        return redirect(url_for('edit_artist_submission', venue_id=venue_id))
    finally:
        db.session.close()


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # [DONE] TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        db.session.delete(venue)
        db.session.commit()
        flash(f'The venue {venue.name} has been removed.')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        print(e)
        flash('Failed to delete this venue.')
        return redirect(url_for('show_venue', venue_id))
    finally:
        db.session.close()

    # [DONE] BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage


#  View Artists
#  -----------------------------------
@app.route('/artists')
def artists():
    # [DONE] TODO: replace with real data returned from querying the database
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # [DONE] TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    artists = Artist.query.filter(Artist.name.ilike(
        f"%{request.form.get('search_term')}%")).all()
    response = {
        "count": len(artists),
        "data": [artist.serialize_artist_with_upcoming_shows for artist in artists]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # [DONE] TODO: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.filter(Artist.id == artist_id).first()

    all_shows = Show.query.with_entities(Show.venue_id, Show.start_time, Venue.image_link.label("venue_image_link"), Venue.name.label("venue_name"))\
        .filter(Show.artist_id == artist.id)\
        .join(Venue, Venue.id == Show.venue_id)\
        .all()

    past_shows = []
    upcoming_shows = []

    for show in all_shows:
        if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') < datetime.now():
            past_shows.append({
                "venue_id": show.venue_id,
                "venue_name": show.venue_name,
                "venue_image_link": show.venue_image_link,
                "start_time": show.start_time,
            })
        else:
            upcoming_shows.append({
                "venue_id": show.venue_id,
                "venue_name": show.venue_name,
                "venue_image_link": show.venue_image_link,
                "start_time": show.start_time,
            })

    data = {
        "id": artist.id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "genres": artist.genres,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "website": artist.website,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "past_shows": past_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)


#  Create & Edit Artists
#  -----------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # [DONE] TODO: insert form data as a new Venue record in the db, instead - New Venue record? But this is supposed to create an artist?
    # [DONE] TODO: modify data to be the data object returned from db insertion - This TODO is unclear

    data = request.values
    try:
        artist = Artist(
            name=data["name"],
            city=data["city"],
            state=data["state"],
            phone=data["phone"],
            genres=request.form.getlist("genres"),
            facebook_link=data["facebook_link"],
            image_link=data["image_link"],
            website=data["website_link"],
            seeking_venue=bool(data.get("seeking_venue", False)),
            seeking_description=data["seeking_description"]
        )
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash(f'Artist {request.form["name"]} was successfully listed!')
        return redirect(url_for('artists'))
    except Exception as e:
        db.session.rollback()
        print(e)
        # [DONE] TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        flash(f'An error occurred. Artist {data.name} could not be listed.')
        return redirect(url_for('create_artist_submission'))
    finally:
        db.session.close()


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    form = ArtistForm(
        name=artist.name,
        city=artist.city,
        state=artist.state,
        phone=artist.phone,
        genres=artist.genres,
        facebook_link=artist.facebook_link,
        image_link=artist.image_link,
        website_link=artist.website,
        seeking_venue=artist.seeking_venue,
        seeking_description=artist.seeking_description
    )

    # [DONE] TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # [DONE] TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    data = request.values
    try:
        artist = Artist.query.filter_by(id=artist_id).first()
        artist.name = data["name"]
        artist.city = data["city"]
        artist.state = data["state"]
        artist.phone = data["phone"]
        artist.genres = request.form.getlist("genres")
        artist.facebook_link = data["facebook_link"]
        artist.image_link = data["image_link"]
        artist.website = data["website_link"]
        artist.seeking_venue = bool(data.get("seeking_venue", False))
        artist.seeking_description = data["seeking_description"]
        db.session.add(artist)
        db.session.commit()
        flash('Artist was updated successfully!')
        return redirect(url_for('show_artist', artist_id=artist_id))
    except Exception as e:
        db.session.rollback()
        print(e)
        flash('Updating the artist failed.')
        return redirect(url_for('edit_artist_submission', artist_id=artist_id))
    finally:
        db.session.close()


#  View & Create Shows
#  -----------------------------------
@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # [DONE] TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue. - I don't see an implementation for num_shows anywhere??

    data = Show.query.with_entities(Show.venue_id, Show.artist_id, Show.start_time, Artist.name.label("artist_name"), Artist.image_link.label(
        "artist_image_link"), Venue.name.label("venue_name"))\
        .join(Artist, Artist.id == Show.artist_id)\
        .join(Venue, Venue.id == Show.venue_id)\
        .all()

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # [DONE] TODO: insert form data as a new Show record in the db, instead

    data = request.values

    try:
        show = Show(
            venue_id=data['venue_id'],
            artist_id=data['artist_id'],
            start_time=data['start_time']
        )
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
        return render_template('pages/home.html')
    except Exception as e:
        print(e)
        db.session.rollback()
        # [DONE] TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('Show could not be added as one or more fields were not completed.')
        return redirect(url_for('create_show_submission'))
    finally:
        db.session.close()


#  Home & Error Pages
#  -----------------------------------
@app.route('/')
def index():
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
