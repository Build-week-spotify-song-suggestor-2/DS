from typing import List, Optional

from pydantic import BaseModel


class ArtistBase(BaseModel):
    name: str
    tracks: List[str] = []


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    id: int

    class Config:
        orm_mode = True


class TrackBase(BaseModel):
    artists: List[int] = []
    suggestions: List[int] = []


class TrackCreate(TrackBase):
    title: str
    artist: str


class Track(TrackBase):
    id: int

    class Config:
        orm_mode = True


class SuggestionBase(BaseModel):
    rank: int
    track_id: str
    suggested_for: str


class SuggestionCreate(SuggestionBase):
    pass


class Suggestion(SuggestionBase):
    id: int
    track_id: int

    class Config:
        orm_mode = True

