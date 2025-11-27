from fastapi import APIRouter, HTTPException
from typing import List
import logging

from schemas import RhymeRequest, RhymeResponse, ChordSuggestionRequest, ChordSuggestionResponse
from schemas import LyricSuggestionRequest, LyricSuggestionResponse
from services.ai_service import RhymeService, ChordService, LyricService, MelodyService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ai", tags=["AI suggestions"])

@router.post("/rhymes", response_model=RhymeResponse)
def get_rhymes(request: RhymeRequest):
    """Get rhyming words for a given word"""
    try:
        rhymes = RhymeService.find_rhymes(request.word, request.count)
        return RhymeResponse(word=request.word, rhymes=rhymes)
    except Exception as e:
        logger.error(f"Error getting rhymes: {str(e)}")
        raise HTTPException(status_code=500, detail="Error finding rhymes")

@router.post("/chord-suggestions", response_model=ChordSuggestionResponse)
def suggest_chords(request: ChordSuggestionRequest):
    """Get chord progression suggestions based on key and mood"""
    try:
        mood = request.mood or "happy"
        suggestions = ChordService.suggest_chords(request.key, mood)
        return ChordSuggestionResponse(
            suggestions=suggestions,
            explanation=f"Based on {request.key} key and {mood} mood"
        )
    except Exception as e:
        logger.error(f"Error suggesting chords: {str(e)}")
        raise HTTPException(status_code=500, detail="Error suggesting chords")

@router.post("/lyric-suggestions", response_model=LyricSuggestionResponse)
def suggest_lyrics(request: LyricSuggestionRequest):
    """Get lyric suggestions based on topic and mood"""
    try:
        suggestions = LyricService.generate_lyric_suggestions(
            request.topic,
            request.mood,
            request.line_count
        )
        analysis = LyricService.analyze_rhyme_scheme("\n".join(suggestions[:2]))
        return LyricSuggestionResponse(
            suggestions=suggestions,
            analysis=analysis
        )
    except Exception as e:
        logger.error(f"Error suggesting lyrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error suggesting lyrics")

@router.get("/scale/{key}")
def get_scale_notes(key: str):
    """Get all notes in a scale for a given key"""
    try:
        notes = ChordService.get_scale_notes(key)
        if not notes:
            raise HTTPException(status_code=400, detail=f"Unknown key: {key}")
        return {"key": key, "notes": notes}
    except Exception as e:
        logger.error(f"Error getting scale: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting scale notes")

@router.get("/melody-suggestions/{key}")
def suggest_melody(key: str):
    """Get suggested melody notes for a key"""
    try:
        notes = MelodyService.suggest_melody_notes(key)
        return {
            "key": key,
            "suggested_notes": notes,
            "characteristics": ["singable", "memorable", "follows harmonic structure"]
        }
    except Exception as e:
        logger.error(f"Error suggesting melody: {str(e)}")
        raise HTTPException(status_code=500, detail="Error suggesting melody")

@router.post("/analyze-lyrics")
def analyze_lyrics(lyrics: str):
    """Analyze lyrics for structure, rhyme scheme, and other characteristics"""
    try:
        analysis = LyricService.analyze_rhyme_scheme(lyrics)
        return {
            "lyrics": lyrics,
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error analyzing lyrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing lyrics")

@router.post("/analyze-melody")
def analyze_melody(notes: List[str]):
    """Analyze melody notes for contour and characteristics"""
    try:
        analysis = MelodyService.analyze_melody(notes)
        return {
            "notes": notes,
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error analyzing melody: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing melody")
