from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class LyricsSectionCreate(BaseModel):
    section_type: str
    content: Optional[str] = Field(None, alias="lyrics")  # Accept both "content" and "lyrics"
    order: int = 0  # Auto-increment, optional
    rhyme_scheme: Optional[str] = None
    syllable_count: Optional[int] = None
    
    class Config:
        populate_by_name = True  # Allow both field name and alias
    
    def __init__(self, **data):
        # If "lyrics" is provided but "content" is not, use "lyrics" as content
        if "lyrics" in data and "content" not in data:
            data["content"] = data.pop("lyrics")
        super().__init__(**data)

class LyricsSectionResponse(BaseModel):
    id: str
    song_id: str
    section_type: str
    order: int
    content: str
    rhyme_scheme: Optional[str] = None
    syllable_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class ChordProgressionCreate(BaseModel):
    section_type: str
    chords: List[str]
    order: int = 0  # Auto-increment, optional
    duration_beats: Optional[int] = None

class ChordProgressionResponse(BaseModel):
    id: str
    song_id: str
    section_type: str
    order: int
    chords: List[str]
    duration_beats: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class MelodyNoteCreate(BaseModel):
    note: str
    duration: float
    velocity: Optional[int] = None
    order: int = 0

class MelodyNoteResponse(MelodyNoteCreate):
    id: str
    song_id: str
    created_at: datetime

class AISuggestionCreate(BaseModel):
    suggestion_type: str
    content: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None

class AISuggestionResponse(AISuggestionCreate):
    id: str
    song_id: str
    applied: bool
    created_at: datetime

class SongCreate(BaseModel):
    title: str
    description: Optional[str] = None
    key: Optional[str] = None
    tempo: Optional[int] = None
    time_signature: Optional[str] = None
    genre: Optional[str] = None
    mood: Optional[str] = None
    structure: Optional[Dict[str, Any]] = None

class SongUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    key: Optional[str] = None
    tempo: Optional[int] = None
    time_signature: Optional[str] = None
    genre: Optional[str] = None
    mood: Optional[str] = None
    structure: Optional[Dict[str, Any]] = None

class SongResponse(SongCreate):
    id: str
    created_at: datetime
    updated_at: datetime
    lyrics_sections: List[LyricsSectionResponse] = []
    chords: List[ChordProgressionResponse] = []
    melody_notes: List[MelodyNoteResponse] = []
    ai_suggestions: List[AISuggestionResponse] = []

class RhymeRequest(BaseModel):
    word: str
    count: int = 10

class RhymeResponse(BaseModel):
    word: str
    rhymes: List[str]

class ChordSuggestionRequest(BaseModel):
    key: str
    mood: Optional[str] = None
    current_chords: Optional[List[str]] = Field(default_factory=list)  # Optional with sensible default

class ChordSuggestionResponse(BaseModel):
    suggestions: List[Dict[str, Any]]
    explanation: Optional[str] = None

class LyricSuggestionRequest(BaseModel):
    topic: str
    mood: str
    rhyme_scheme: Optional[str] = None
    line_count: int = 4

class LyricSuggestionResponse(BaseModel):
    suggestions: List[str]
    analysis: Optional[Dict[str, Any]] = None

class AudioUploadResponse(BaseModel):
    id: str
    filename: str
    duration_seconds: Optional[float]
    file_size: int
    format: str

class AnalysisRequest(BaseModel):
    song_id: str
    analysis_type: str  # "rhyme", "meter", "key", "melody"

class AnalysisResponse(BaseModel):
    song_id: str
    analysis_type: str
    results: Dict[str, Any]
    recommendations: List[str] = []
