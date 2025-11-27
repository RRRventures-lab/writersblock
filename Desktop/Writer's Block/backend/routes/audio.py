from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
import os
from pathlib import Path

from database import get_db
from models import AudioFile
from schemas import AudioUploadResponse
from config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/audio", tags=["audio"])
settings = get_settings()

# Ensure upload directory exists
upload_dir = Path(settings.AUDIO_UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)

@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio(
    file: UploadFile = File(...),
    song_id: str = None,
    db: Session = Depends(get_db)
):
    """Upload an audio file"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Check file extension
        file_ext = Path(file.filename).suffix.lower().lstrip(".")
        if file_ext not in settings.SUPPORTED_AUDIO_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format. Supported formats: {', '.join(settings.SUPPORTED_AUDIO_FORMATS)}"
            )

        # Read file content
        content = await file.read()
        file_size = len(content)

        # Check file size
        if file_size > settings.MAX_AUDIO_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.MAX_AUDIO_FILE_SIZE / (1024*1024):.1f}MB"
            )

        # Save file
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as f:
            f.write(content)

        # Get audio metadata (basic implementation)
        duration = None
        sample_rate = None
        channels = None

        try:
            import librosa
            audio_data, sr = librosa.load(str(file_path), sr=None)
            duration = librosa.get_duration(y=audio_data, sr=sr)
            sample_rate = sr
            channels = 1 if len(audio_data.shape) == 1 else audio_data.shape[0]
        except Exception as e:
            logger.warning(f"Could not extract audio metadata: {str(e)}")

        # Save to database
        audio_file = AudioFile(
            song_id=song_id,
            filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            duration_seconds=duration,
            format=file_ext,
            sample_rate=sample_rate,
            channels=channels
        )
        db.add(audio_file)
        db.commit()
        db.refresh(audio_file)

        return AudioUploadResponse(
            id=audio_file.id,
            filename=audio_file.filename,
            duration_seconds=audio_file.duration_seconds,
            file_size=audio_file.file_size,
            format=audio_file.format
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading audio: {str(e)}")
        raise HTTPException(status_code=500, detail="Error uploading audio file")

@router.get("/files/{file_id}")
def get_audio_file(file_id: str, db: Session = Depends(get_db)):
    """Get audio file metadata"""
    audio_file = db.query(AudioFile).filter(AudioFile.id == file_id).first()
    if not audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return audio_file

@router.get("/song/{song_id}")
def get_song_audio_files(song_id: str, db: Session = Depends(get_db)):
    """Get all audio files for a song"""
    audio_files = db.query(AudioFile).filter(AudioFile.song_id == song_id).all()
    return audio_files

@router.delete("/files/{file_id}")
def delete_audio_file(file_id: str, db: Session = Depends(get_db)):
    """Delete an audio file"""
    audio_file = db.query(AudioFile).filter(AudioFile.id == file_id).first()
    if not audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")

    try:
        # Delete from filesystem
        if os.path.exists(audio_file.file_path):
            os.remove(audio_file.file_path)

        # Delete from database
        db.delete(audio_file)
        db.commit()

        return {"message": "Audio file deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting audio file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting audio file")

@router.post("/analyze/{file_id}")
def analyze_audio(file_id: str, db: Session = Depends(get_db)):
    """Analyze audio file for BPM, key, and other characteristics"""
    audio_file = db.query(AudioFile).filter(AudioFile.id == file_id).first()
    if not audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")

    try:
        # Basic audio analysis
        analysis = {
            "file_id": file_id,
            "duration": audio_file.duration_seconds,
            "sample_rate": audio_file.sample_rate,
            "channels": audio_file.channels,
            "estimated_bpm": 120,  # Placeholder
            "estimated_key": "C",  # Placeholder
            "characteristics": ["has_vocals", "instrumental_elements"]
        }
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing audio: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing audio file")
