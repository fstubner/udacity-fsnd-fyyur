#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, JSON
from fyyur import db


#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#
# [DONE] TODO: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'shows'

    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey(
        'venues.id', ondelete='CASCADE'), nullable=False)
    artist_id = Column(Integer, ForeignKey(
        'artists.id', ondelete='CASCADE'), nullable=False)
    start_time = Column(String(), nullable=False)


class Venue(db.Model):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    phone = Column(String(120))
    genres = Column(JSON)
    facebook_link = Column(String(120))
    image_link = Column(String(500))
    website = Column(String(120))
    seeking_talent = Column(Boolean, nullable=False, default=False)
    seeking_description = Column(String(500))
    shows = relationship(
        Show,
        backref='venue',
        cascade='all, delete-orphan',
        lazy=True
    )

    @property
    def with_upcoming_shows(self):
        num_upcoming_shows = []
        for show in self.shows:
            if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
                num_upcoming_shows.append(show)

        return {
            "id": self.id,
            "name": self.name,
            "num_upcoming_shows": len(num_upcoming_shows)
        }

    # [DONE] TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    phone = Column(String(120))
    genres = Column(JSON)
    facebook_link = Column(String(120))
    image_link = Column(String(500))
    website = Column(String(120))
    seeking_venue = Column(Boolean, nullable=False, default=False)
    seeking_description = Column(String(500))
    shows = relationship(
        Show,
        backref='artist',
        cascade='all, delete-orphan',
        lazy=True
    )

    @property
    def with_upcoming_shows(self):
        num_upcoming_shows = []
        for show in self.shows:
            if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
                num_upcoming_shows.append(show)

        return {
            "id": self.id,
            "name": self.name,
            "num_upcoming_shows": len(num_upcoming_shows)
        }

    # [DONE] TODO: implement any missing fields, as a database migration using Flask-Migrate
