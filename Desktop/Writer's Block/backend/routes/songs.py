from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from models import Song, LyricsSection, ChordProgression, MelodyNote
from schemas import SongCreate, SongUpdate, SongResponse, LyricsSectionCreate, ChordProgressionCreate, MelodyNoteCreate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/songs", tags=["songs"])

@router.post("", response_model=SongResponse)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    """Create a new song"""
    try:
        db_song = Song(**song.dict())
        db.add(db_song)
        db.commit()
        db.refresh(db_song)
        return db_song
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating song: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[SongResponse])
def list_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all songs"""
    songs = db.query(Song).offset(skip).limit(limit).all()
    return songs

@router.get("/{song_id}", response_model=SongResponse)
def get_song(song_id: str, db: Session = Depends(get_db)):
    """Get a specific song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@router.put("/{song_id}", response_model=SongResponse)
def update_song(song_id: str, song_update: SongUpdate, db: Session = Depends(get_db)):
    """Update a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    try:
        update_data = song_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(song, key, value)
        db.commit()
        db.refresh(song)
        return song
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating song: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{song_id}")
def delete_song(song_id: str, db: Session = Depends(get_db)):
    """Delete a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    try:
        db.delete(song)
        db.commit()
        return {"message": "Song deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting song: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Lyrics endpoints
@router.post("/{song_id}/lyrics", response_model=dict)
def add_lyrics_section(song_id: str, lyrics: LyricsSectionCreate, db: Session = Depends(get_db)):
    """Add a lyrics section to a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    try:
        lyrics_section = LyricsSection(song_id=song_id, **lyrics.dict())
        db.add(lyrics_section)
        db.commit()
        db.refresh(lyrics_section)
        return lyrics_section
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding lyrics: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{song_id}/lyrics", response_model=List[dict])
def get_lyrics(song_id: str, db: Session = Depends(get_db)):
    """Get all lyrics sections for a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song.lyrics_sections

# Chords endpoints
@router.post("/{song_id}/chords", response_model=dict)
def add_chord_progression(song_id: str, chords: ChordProgressionCreate, db: Session = Depends(get_db)):
    """Add a chord progression to a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    try:
        chord_prog = ChordProgression(song_id=song_id, **chords.dict())
        db.add(chord_prog)
        db.commit()
        db.refresh(chord_prog)
        return chord_prog
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding chords: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{song_id}/chords", response_model=List[dict])
def get_chords(song_id: str, db: Session = Depends(get_db)):
    """Get all chord progressions for a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song.chords

# Melody endpoints
@router.post("/{song_id}/melody", response_model=dict)
def add_melody_note(song_id: str, note: MelodyNoteCreate, db: Session = Depends(get_db)):
    """Add a melody note to a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    try:
        melody = MelodyNote(song_id=song_id, **note.dict())
        db.add(melody)
        db.commit()
        db.refresh(melody)
        return melody
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding melody note: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{song_id}/melody", response_model=List[dict])
def get_melody(song_id: str, db: Session = Depends(get_db)):
    """Get all melody notes for a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song.melody_notes
