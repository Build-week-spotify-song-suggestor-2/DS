from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

association_table = Table('TracksAndArtists', Base.metadata,
    Column('track_id', String, ForeignKey('tracks.id')),
    Column('artist_id', Integer, ForeignKey('artists.id'))
)

class Track(Base):
    __tablename__ = "tracks"

    id = Column(String, primary_key=True)
    title = Column(String)
    artists = relationship("Artist", 
                           secondary=association_table, 
                           back_populates="tracks")
    suggestions = relationship("Suggestion", back_populates="suggested_for")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    track_id = Column(String, ForeignKey("tracks.id"))
    rank = Column(Integer)
    suggested_for = relationship("Track", back_populates="suggestions")


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    tracks = relationship("Track",
                          secondary=association_table, 
                          back_populates="artists")
                             