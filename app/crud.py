from typing import List
from sqlalchemy.orm import Session

from . import models, schemas


def get_track(db: Session, track_id: str):
    return db.query(models.Track).filter(models.Track.id == track_id).first()


def create_track(db: Session, id: str, title: str):
    db_track = models.Track(id=id, title=title)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track


def add_artist_to_track(db: Session, artist: schemas.Artist, track: schemas.Track):
    track.artists.append(artist)
    db.commit()
    db.refresh(track)
    return track


def get_suggestions(db: Session, track_id: str, skip: int = 0, limit: int = 10):
    return db.query(models.Track).filter(models.Suggestion.track_id == track_id).all()


def create_suggestion(db: Session, track_id: str, rank: int):
    db_suggestion = models.Suggestion(track_id=track_id, rank=rank)
    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion


def add_suggestion_to_track(db: Session, suggestion: schemas.Suggestion, track: schemas.Track):
    track.suggestions.append(suggestion)
    db.commit()
    db.refresh(track)
    return track


def get_artist(db: Session, name: str):
    return db.query(models.Artist).filter(models.Artist.name == name).first()


def create_artist(db: Session, name: str):
    db_artist = models.Artist(name=name)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist
