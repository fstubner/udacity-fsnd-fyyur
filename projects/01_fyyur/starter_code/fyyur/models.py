#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from fyyur import db


#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    phone = Column(String(120))
    genres = Column(String(120), nullable=False)
    facebook_link = Column(String(120))
    image_link = Column(String(500))
    website_link = Column(String(120))
    looking_for_talent = Column(Boolean, nullable=False, default=False)
    seeking_description = Column(String(500))
    shows = relationship(
        'artists',
        backref='venue',
        secondary='shows',
        cascade='all, delete-orphan',
        lazy=True
    )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate - DONE

class Artist(db.Model):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    phone = Column(String(120))
    genres = Column(String(120), nullable=False)
    facebook_link = Column(String(120))
    image_link = Column(String(500))
    website_link = Column(String(120))
    looking_for_venues = Column(Boolean, nullable=False, default=False)
    seeking_description = Column(String(500))
    shows = relationship(
        'venues',
        backref='artist',
        secondary='shows',
        cascade='all, delete-orphan',
        lazy=True
    )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate - DONE

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. - DONE

class Show(db.Model):
    __tablename__ = 'shows'

    venue_id = Column(Integer, ForeignKey('venues.id', ondelete='CASCADE'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.id', ondelete='CASCADE'), primary_key=True)
    start_time = Column(DateTime, nullable=False)