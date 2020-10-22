import logging
from random import choice
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from pydantic import BaseModel, Field, validator

from app.api.client import client
from app.api.recommend import find_recommended_songs, track_id_in_df, get_radar_plot

log = logging.getLogger(__name__)
router = APIRouter()

from .. import crud, models, schemas
from ..database import SessionLocal, engine

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/predict') # , response_model=List[schemas.Track])
async def predict(track: schemas.TrackCreate, db: Session = Depends(get_db)):
    """
    Suggest a list of recommendations for the specified Track.

    ### Request Body
    - `title`: string
    - `artist`: string

    ### Response
    - `recommendations`: list of objects containing an `artist` and a `title` 
    - `artists`: string
    - `title`: string
    """

    # Find first track id that matches the given title and artist
    track_ids = client.request_track_ids(track.title, track.artist)
    for track_id in track_ids:
      db_track = find_track(db, track_id)
      if db_track: break
    else:
      return {"error": f"{track.title} by {track.artist} not found."}

    if not db_track.suggestions:  
      for rank, suggested_track_id in enumerate(find_recommended_songs(db_track.id)):
        suggested_track = find_track(db, suggested_track_id)

        if suggested_track:
          crud.add_suggestion_to_track(
            db,
            crud.create_suggestion(db, suggested_track.id, rank),
            db_track
          )

    return {
      "recommendations": [
        {
          "title": s.title,
          "artists": [a.name for a in s.artists]
        }
        for s in crud.get_suggestions(db, track_id)
      ]}


def find_track(db, track_id):
  track = crud.get_track(db, track_id)
  if track: return track

  title, artist_names = client.request_track_info(track_id)

  if not title or not artist_names: return None

  track = crud.create_track(db, id=track_id, title=title)
  for artist_name in artist_names:
    artist = crud.get_artist(db, name=artist_name) or \
      crud.create_artist(db, name=artist_name)
    track = crud.add_artist_to_track(db, artist=artist, track=track)

  return track


@router.post('/viz') # , response_model=List[schemas.Track])
async def viz(track: schemas.TrackCreate, db: Session = Depends(get_db)):
    """
    Suggest a list of recommendations for the specified Track.

    ### Request Body
    - `title`: string
    - `artist`: string
    """
    track_ids = client.request_track_ids(track.title, track.artist)
    for track_id in track_ids:
      db_track = find_track(db, track_id)
      if db_track: break
    else:
      return {"error": f"{track.title} by {track.artist} not found."}

    if not db_track.suggestions:  
      for rank, suggested_track_id in enumerate(find_recommended_songs(db_track.id)):
        suggested_track = find_track(db, suggested_track_id)

        if suggested_track:
          crud.add_suggestion_to_track(
            db,
            crud.create_suggestion(db, suggested_track.id, rank),
            db_track
          )

    return get_radar_plot([s.id for s in crud.get_suggestions(db, track_id)])
