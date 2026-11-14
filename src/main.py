"""Run several sample listener profiles through the music recommender."""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "Happy Pop": {"genre": "pop", "mood": "happy", "energy": 0.80, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.90, "likes_acoustic": False},
    "High-Energy Calm Mood (edge case)": {"genre": "ambient", "mood": "chill", "energy": 0.90, "likes_acoustic": True},
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for profile_name, user_prefs in PROFILES.items():
        print(f"\n{profile_name}: {user_prefs}")
        print("Top recommendations:")
        for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k=5), 1):
            print(f"  {rank}. {song['title']} — {song['artist']} | {score:.2f}")
            print(f"     Because: {explanation}")


if __name__ == "__main__":
    main()
