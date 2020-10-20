import logging
from random import choice

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

from app.api.client import client
from app.api.recommend import find_recommended_songs, track_id_in_df

log = logging.getLogger(__name__)
router = APIRouter()


class Track(BaseModel):
    """Use this data model to parse the request body JSON."""

    title: str = Field(..., example="Waka Waka")
    artist: str = Field(..., example="Shakira")

    @validator('title')
    def title_must_be_non_empty(cls, value):
        """Validate that title is a non-empty string."""
        assert value != "", f'title == {value}, must be non-empty string'
        return value

    @validator('artist')
    def artist_must_be_non_empty(cls, value):
        """Validate that artist is a non-empty string."""
        assert value != "", f'artist == {value}, must be non-empty string'
        return value


@router.post('/predict')
async def predict(track: Track):
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

    track_ids = client.request_track_ids(track.title, track.artist)
    for track_id in track_ids:
      if track_id_in_df(track_id): break
    else:
      return {
        "error": f"{track.title} by {track.artist} not found."
      }

    return {
      "recommendations": [
        client.request_track_info(recommended_track_id) 
          for recommended_track_id in find_recommended_songs(track_id)
        ]
      }
