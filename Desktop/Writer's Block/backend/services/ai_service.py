import logging
from typing import List, Dict, Optional
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class RhymeService:
    """Service for finding rhyming words"""

    @staticmethod
    def find_rhymes(word: str, count: int = 10) -> List[str]:
        """Find rhyming words for a given word"""
        # Hardcoded rhyme dictionary for demo (replace with proper API/library)
        rhyme_dict = {
            "love": ["above", "dove", "glove", "shove", "thereof", "enough", "rough", "tough", "stuff", "buff"],
            "day": ["way", "say", "play", "stay", "gray", "may", "ray", "pay", "bay", "lay"],
            "night": ["light", "sight", "might", "fight", "right", "flight", "bright", "tight", "height", "weight"],
            "heart": ["start", "part", "art", "apart", "smart", "chart", "dart", "cart", "tart", "depart"],
            "rain": ["pain", "gain", "main", "plain", "chain", "brain", "train", "strain", "domain", "remain"],
            "blue": ["true", "new", "flew", "grew", "knew", "through", "view", "crew", "drew", "clue"],
            "fire": ["desire", "higher", "wire", "tire", "expire", "inspire", "require", "acquire", "liar", "choir"],
            "summer": ["drummer", "bummer", "hummer", "glimmer", "shimmer", "dimmer", "slumber", "number", "cucumber", "remember"],
            "rose": ["those", "close", "prose", "chose", "compose", "suppose", "oppose", "propose", "dispose", "enclose"],
            "moon": ["soon", "june", "tune", "noon", "room", "bloom", "gloom", "doom", "zoom", "broom"],
        }

        word_lower = word.lower()
        return rhyme_dict.get(word_lower, [])[:count]

class ChordService:
    """Service for chord suggestions and analysis"""

    # Music theory chord progressions
    COMMON_PROGRESSIONS = {
        "major": {
            "happy": [["I", "V", "vi", "IV"], ["I", "IV", "V"], ["vi", "IV", "I", "V"]],
            "melancholy": [["vi", "IV", "I", "V"], ["iv", "VII", "III"], ["vi", "ii", "V", "I"]],
            "epic": [["I", "V", "vi", "iii", "IV"], ["I", "IV", "I", "V"]],
        },
        "minor": {
            "dark": [["vi", "III", "VII"], ["i", "VII", "VI"], ["i", "iv", "VII"]],
            "emotional": [["vi", "IV", "I", "V"], ["i", "VI", "III", "VII"]],
            "powerful": [["i", "iv", "i", "VII"], ["i", "V", "VII", "iv"]],
        },
    }

    SCALE_NOTES = {
        "C": ["C", "D", "E", "F", "G", "A", "B"],
        "G": ["G", "A", "B", "C", "D", "E", "F#"],
        "D": ["D", "E", "F#", "G", "A", "B", "C#"],
        "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
        "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
        "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
        "F": ["F", "G", "A", "Bb", "C", "D", "E"],
        "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
        "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    }

    @staticmethod
    def suggest_chords(key: str, mood: str = "happy") -> List[Dict]:
        """Suggest chord progressions based on key and mood"""
        try:
            key_mode = "major" if key.isupper() and len(key) == 1 else "minor"
            progressions = ChordService.COMMON_PROGRESSIONS.get(
                key_mode, {}
            ).get(mood, [["I", "IV", "V"]])

            return [
                {
                    "progression": prog,
                    "explanation": f"Popular {mood} progression in {key_mode}",
                    "voicing": "Use open or close voicing as desired"
                }
                for prog in progressions[:3]
            ]
        except Exception as e:
            logger.error(f"Error suggesting chords: {str(e)}")
            return [{"progression": ["I", "IV", "V"], "explanation": "Default progression"}]

    @staticmethod
    def get_scale_notes(key: str) -> List[str]:
        """Get all notes in a scale for a given key"""
        return ChordService.SCALE_NOTES.get(key, [])


class LyricService:
    """Service for lyric analysis and suggestions"""

    EMOTIONAL_KEYWORDS = {
        "love": ["heart", "soul", "forever", "together", "embrace", "tender"],
        "sadness": ["tears", "alone", "pain", "lost", "broken", "empty"],
        "happiness": ["smile", "bright", "joy", "free", "soar", "dance"],
        "anger": ["fire", "rage", "strong", "fight", "power", "fierce"],
    }

    @staticmethod
    def generate_lyric_suggestions(topic: str, mood: str, count: int = 4) -> List[str]:
        """Generate lyric suggestions based on topic and mood"""
        suggestions = {
            "love": [
                "Your love is all I need",
                "Forever in your eyes I see",
                "My heart beats just for you",
                "In your arms is where I belong",
                "You are my love, my life, my song",
            ],
            "heartbreak": [
                "Tears fall like rain tonight",
                "You left me here alone",
                "My heart is breaking inside",
                "I can't forget your face",
                "Love turned to pain so fast",
            ],
            "growth": [
                "I'm rising from the ashes now",
                "Learning who I am inside",
                "Every day I'm becoming more",
                "Breaking free from all my chains",
                "I'm stronger than before",
            ],
            "happiness": [
                "Life is beautiful and bright",
                "Living in this perfect moment",
                "Nothing can bring me down",
                "I'm dancing in the light",
                "Pure joy fills my soul",
            ],
        }

        key = topic.lower() if topic.lower() in suggestions else "love"
        base_suggestions = suggestions.get(key, suggestions["love"])
        return base_suggestions[:count]

    @staticmethod
    def analyze_rhyme_scheme(lyrics: str) -> Dict:
        """Analyze the rhyme scheme of lyrics"""
        lines = lyrics.strip().split("\n")
        return {
            "total_lines": len(lines),
            "average_syllables": sum(len(line.split()) for line in lines) // len(lines),
            "line_lengths": [len(line.split()) for line in lines],
            "potential_improvements": ["Consider varying line lengths", "Add more internal rhymes"],
        }


class MelodyService:
    """Service for melody analysis and suggestions"""

    @staticmethod
    def suggest_melody_notes(key: str, scale_type: str = "major") -> List[str]:
        """Suggest melody notes based on key"""
        scales = {
            "C_major": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
            "G_major": ["G3", "A3", "B3", "C4", "D4", "E4", "F#4", "G4"],
            "D_major": ["D4", "E4", "F#4", "G4", "A4", "B4", "C#5", "D5"],
        }
        scale_key = f"{key}_{scale_type}"
        return scales.get(scale_key, ["C4", "D4", "E4", "F4", "G4"])

    @staticmethod
    def analyze_melody(notes: List[str]) -> Dict:
        """Analyze melodic contour and characteristics"""
        return {
            "note_count": len(notes),
            "range": f"{notes[0] if notes else 'N/A'} to {notes[-1] if notes else 'N/A'}",
            "contour": "ascending" if len(notes) > 1 and notes[-1] > notes[0] else "descending",
            "characteristics": ["Singable", "Memorable"],
        }
