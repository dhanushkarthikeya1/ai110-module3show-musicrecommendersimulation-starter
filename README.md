# 🎵 VibeFinder: Music Recommender Simulation

## Project Summary

VibeFinder is a small, explainable Python music recommender. It loads a CSV catalog, compares each track with a listener profile, and ranks songs using genre, mood, energy, and an optional acoustic preference. Each result includes a score breakdown so a listener can see why the track appeared. This classroom simulation uses explicit rules; it does not learn from listening history or reproduce the full systems used by streaming platforms.

## How The System Works

A `Song` contains an ID, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. A `UserProfile` contains a favorite genre and mood, a target energy from 0 to 1, and an acoustic preference. The recommender scores every song, sorts the results from highest to lowest score, and returns the requested number of tracks. The functional CLI returns the score and reasons; an object-oriented `Recommender` class uses the same scoring rules.

### Algorithm recipe

- Matching genre: **+2.00 points**.
- Matching mood: **+1.00 point**.
- Energy similarity: **1 − |song energy − target energy|**, for up to **+1.00 point**. Both values are bounded to the 0–1 range.
- Matching the acoustic preference: **+0.50 points**. A track is treated as acoustic when its acousticness is at least 0.60.
- Rank all tracks by total score, highest first. When scores tie, retain the CSV order.

```text
User profile → score every track → sort by score → show top K with reasons
```

Genre has the largest categorical weight, so the system may rank a genre match above a track with a closer energy match. The acousticness cutoff is a simple simulation choice, not a universal definition of acoustic music.

## Getting Started

Run the app from the repository root:

```bash
python -m src.main
```

The project uses Python's standard library for its recommender and CSV loader.

## Sample Recommendation Output

The following is the CLI output for all four profiles, including the edge case:

```text
Loaded songs: 18

Happy Pop: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
Top recommendations:
  1. Sunrise City — Neon Echo | 4.48
     Because: genre match (+2.00); mood match (+1.00); energy similarity (+0.98); acoustic preference match (+0.50)
  2. Gym Hero — Max Pulse | 3.37
     Because: genre match (+2.00); energy similarity (+0.87); acoustic preference match (+0.50)
  3. Rooftop Lights — Indigo Parade | 2.46
     Because: mood match (+1.00); energy similarity (+0.96); acoustic preference match (+0.50)
  4. Golden Hour Run — Daylight Club | 1.46
     Because: energy similarity (+0.96); acoustic preference match (+0.50)
  5. Night Drive Loop — Neon Echo | 1.45
     Because: energy similarity (+0.95); acoustic preference match (+0.50)

Chill Lofi: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
Top recommendations:
  1. Library Rain — Paper Lanterns | 4.50
     Because: genre match (+2.00); mood match (+1.00); energy similarity (+1.00); acoustic preference match (+0.50)
  2. Midnight Coding — LoRoom | 4.43
     Because: genre match (+2.00); mood match (+1.00); energy similarity (+0.93); acoustic preference match (+0.50)
  3. Focus Flow — LoRoom | 3.45
     Because: genre match (+2.00); energy similarity (+0.95); acoustic preference match (+0.50)
  4. Sunday Window — Marina Vale | 2.45
     Because: mood match (+1.00); energy similarity (+0.95); acoustic preference match (+0.50)
  5. Spacewalk Thoughts — Orbit Bloom | 2.43
     Because: mood match (+1.00); energy similarity (+0.93); acoustic preference match (+0.50)

Intense Rock: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}
Top recommendations:
  1. Storm Runner — Voltline | 4.49
     Because: genre match (+2.00); mood match (+1.00); energy similarity (+0.99); acoustic preference match (+0.50)
  2. Gym Hero — Max Pulse | 2.47
     Because: mood match (+1.00); energy similarity (+0.97); acoustic preference match (+0.50)
  3. Heavy Weather — Black Static | 2.44
     Because: mood match (+1.00); energy similarity (+0.94); acoustic preference match (+0.50)
  4. Neon Heartbeat — Glass Arcade | 1.48
     Because: energy similarity (+0.98); acoustic preference match (+0.50)
  5. Golden Hour Run — Daylight Club | 1.44
     Because: energy similarity (+0.94); acoustic preference match (+0.50)

High-Energy Calm Mood (edge case): {'genre': 'ambient', 'mood': 'chill', 'energy': 0.9, 'likes_acoustic': True}
Top recommendations:
  1. Spacewalk Thoughts — Orbit Bloom | 3.88
     Because: genre match (+2.00); mood match (+1.00); energy similarity (+0.38); acoustic preference match (+0.50)
  2. Midnight Coding — LoRoom | 2.02
     Because: mood match (+1.00); energy similarity (+0.52); acoustic preference match (+0.50)
  3. Library Rain — Paper Lanterns | 1.95
     Because: mood match (+1.00); energy similarity (+0.45); acoustic preference match (+0.50)
  4. Sunday Window — Marina Vale | 1.90
     Because: mood match (+1.00); energy similarity (+0.40); acoustic preference match (+0.50)
  5. Focus Flow — LoRoom | 1.00
     Because: energy similarity (+0.50); acoustic preference match (+0.50)
```

## Profiles and Evaluation

The CLI compares four profiles: Happy Pop, Chill Lofi, Intense Rock, and a high-energy listener who also wants a calm mood. The first three produce visibly different top results. The edge-case profile ranks *Spacewalk Thoughts* first because its ambient genre and chill mood each match, even though its low energy is far from the target. This is a useful example of how weighted preferences can resolve conflicting signals in an unexpected way.

### Weight-shift experiment

I compared the baseline weights with an experimental version that halves the genre weight from 2.0 to 1.0 and doubles the energy similarity contribution. For Happy Pop, *Rooftop Lights* moves ahead of *Gym Hero*: the energy bonus matters more, while Gym Hero no longer gets as much advantage from its pop label. The change makes the ranking more sensitive to energy but does not make it universally more accurate; that depends on what the listener values.

## Limitations and Risks

The catalog is small and its tags are simplified, so it cannot capture the range of musical taste. Genre and mood labels can be subjective, and genre receives the largest weight. The system can favor tracks that match a few chosen labels while overlooking lyrics, context, familiarity, or a listener's changing mood. Its fixed scoring rules may also create a narrow listening loop; adding diversity controls and feedback would help.

## Reflection

This project helped me see how a recommendation can come from a clear chain of steps: represent preferences, compare them with item features, calculate scores, and rank the results. Returning reasons alongside scores makes the logic easier to inspect. I also learned that small weight choices can change the order, even when the underlying songs and preferences stay the same.

AI assistance can help brainstorm scoring choices and explain implementation options, but the proposed weights and generated code still need to be checked against the actual data and expected behavior. The surprising part is how a basic weighted sum can already feel personalized, while still missing the nuance that a real listener brings. If I continued the project, I would add user feedback, a diversity rule, and more nuanced audio or mood features.

See [model_card.md](model_card.md) for the model description and evaluation notes.
