from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid

class Song(Base):
    __tablename__ = "songs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    key = Column(String(10), nullable=True)  # e.g., "C", "G", "D minor"
    tempo = Column(Integer, nullable=True)
    time_signature = Column(String(5), nullable=True)  # e.g., "4/4", "3/4"
    genre = Column(String(100), nullable=True)
    mood = Column(String(100), nullable=True)
    structure = Column(JSON, nullable=True)  # e.g., {"sections": ["intro", "verse", "chorus", "bridge"]}

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    lyrics_sections = relationship("LyricsSection", back_populates="song", cascade="all, delete-orphan")
    chords = relationship("ChordProgression", back_populates="song", cascade="all, delete-orphan")
    melody_notes = relationship("MelodyNote", back_populates="song", cascade="all, delete-orphan")
    ai_suggestions = relationship("AISuggestion", back_populates="song", cascade="all, delete-orphan")

class LyricsSection(Base):
    __tablename__ = "lyrics_sections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    song_id = Column(String, ForeignKey("songs.id"), nullable=False, index=True)
    section_type = Column(String(50), nullable=False)  # "verse", "chorus", "bridge", etc.
    order = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    rhyme_scheme = Column(String(100), nullable=True)
    syllable_count = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    song = relationship("Song", back_populates="lyrics_sections")

class ChordProgression(Base):
    __tablename__ = "chord_progressions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    song_id = Column(String, ForeignKey("songs.id"), nullable=False, index=True)
    section_type = Column(String(50), nullable=False)
    order = Column(Integer, nullable=False)
    chords = Column(JSON, nullable=False)  # List of chords: ["C", "Am", "F", "G"]
    duration_beats = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    song = relationship("Song", back_populates="chords")

class MelodyNote(Base):
    __tablename__ = "melody_notes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    song_id = Column(String, ForeignKey("songs.id"), nullable=False, index=True)
    note = Column(String(10), nullable=False)  # e.g., "C4", "D#5"
    duration = Column(Float, nullable=False)  # in beats
    velocity = Column(Integer, nullable=True)  # 0-127 for MIDI
    order = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    song = relationship("Song", back_populates="melody_notes")

class AISuggestion(Base):
    __tablename__ = "ai_suggestions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    song_id = Column(String, ForeignKey("songs.id"), nullable=False, index=True)
    suggestion_type = Column(String(50), nullable=False)  # "rhyme", "lyric", "chord", "melody"
    content = Column(JSON, nullable=False)
    context = Column(JSON, nullable=True)
    confidence = Column(Float, nullable=True)  # 0-1
    applied = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    song = relationship("Song", back_populates="ai_suggestions")

class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    song_id = Column(String, ForeignKey("songs.id"), nullable=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    duration_seconds = Column(Float, nullable=True)
    format = Column(String(10), nullable=False)
    sample_rate = Column(Integer, nullable=True)
    channels = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    song = relationship("Song", foreign_keys=[song_id])
