"""Transparent, content-based music recommendation helpers."""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Union


@dataclass
class Song:
    """A catalog track and its descriptive audio features."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """A listener's target preferences for this simple simulation."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool = False


def _number(value: object, field: str, row_number: int) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {field!r} value on CSV row {row_number}: {value!r}") from exc


def load_songs(csv_path: Union[str, Path]) -> List[Dict]:
    """Load song rows from CSV and convert feature columns to numeric values."""
    path = Path(csv_path)
    numeric_fields = {"id": int, "energy": float, "tempo_bpm": float,
                      "valence": float, "danceability": float, "acousticness": float}
    songs: List[Dict] = []
    with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        required = {"id", "title", "artist", "genre", "mood", "energy",
                    "tempo_bpm", "valence", "danceability", "acousticness"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
        for row_number, row in enumerate(reader, start=2):
            song: Dict = {}
            for key, value in row.items():
                if key in numeric_fields:
                    parsed = _number(value, key, row_number)
                    song[key] = int(parsed) if numeric_fields[key] is int else parsed
                else:
                    song[key] = (value or "").strip()
            songs.append(song)
    return songs


def _preference(user_prefs: Union[Dict, UserProfile], key: str, alias: str = None, default=None):
    if isinstance(user_prefs, dict):
        return user_prefs.get(key, user_prefs.get(alias, default) if alias else default)
    return getattr(user_prefs, key, getattr(user_prefs, alias, default) if alias else default)


def _value(song: Union[Dict, Song], key: str, default=None):
    return song.get(key, default) if isinstance(song, dict) else getattr(song, key, default)


def _explain_score(user_prefs: Union[Dict, UserProfile], song: Union[Dict, Song]) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []

    genre = _preference(user_prefs, "favorite_genre", "genre")
    mood = _preference(user_prefs, "favorite_mood", "mood")
    target_energy = _preference(user_prefs, "target_energy", "energy")

    if genre and str(_value(song, "genre", "")).strip().casefold() == str(genre).strip().casefold():
        score += 2.0
        reasons.append("genre match (+2.00)")
    if mood and str(_value(song, "mood", "")).strip().casefold() == str(mood).strip().casefold():
        score += 1.0
        reasons.append("mood match (+1.00)")
    if target_energy is not None and _value(song, "energy") is not None:
        try:
            target = max(0.0, min(1.0, float(target_energy)))
            energy = max(0.0, min(1.0, float(_value(song, "energy"))))
            similarity = 1.0 - abs(energy - target)
            score += similarity
            reasons.append(f"energy similarity (+{similarity:.2f})")
        except (TypeError, ValueError):
            reasons.append("energy skipped (invalid numeric value)")

    likes_acoustic = _preference(user_prefs, "likes_acoustic")
    acousticness = _value(song, "acousticness")
    if likes_acoustic is not None and acousticness is not None:
        try:
            is_acoustic = float(acousticness) >= 0.60
            if bool(likes_acoustic) == is_acoustic:
                score += 0.5
                reasons.append("acoustic preference match (+0.50)")
        except (TypeError, ValueError):
            pass

    if not reasons:
        reasons.append("no preference matched; ranked by a neutral score")
    return score, reasons


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a weighted relevance score and the reasons that produced it."""
    return _explain_score(user_prefs, song)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score the catalog and return up to k songs in descending score order."""
    if k <= 0:
        return []
    ranked = []
    for index, song in enumerate(songs):
        score, reasons = score_song(user_prefs, song)
        ranked.append((song, score, "; ".join(reasons), index))
    ranked.sort(key=lambda item: (-item[1], item[3]))
    return [(song, score, explanation) for song, score, explanation, _ in ranked[:k]]


class Recommender:
    """Object-oriented wrapper around the same transparent scoring rules."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        if k <= 0:
            return []
        return sorted(self.songs, key=lambda song: -_explain_score(user, song)[0])[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain a track's genre, mood, energy, and optional acoustic matches."""
        score, reasons = _explain_score(user, song)
        return f"Score {score:.2f}: " + "; ".join(reasons)
