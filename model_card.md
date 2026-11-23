# 🎧 Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** — a transparent music recommendation simulation.

## 2. Intended Use

VibeFinder is designed for classroom exploration of how a simple content-based recommender ranks a small song catalog. A user supplies preferences for genre, mood, energy, and acoustic sound, and the system suggests tracks with similar attributes. It is not a production streaming service and should not be used to infer a listener's identity or make high-stakes decisions.

## 3. How the Model Works

For every song, the system adds 2 points for a matching genre and 1 point for a matching mood. It adds up to 1 point for energy similarity, based on the distance between the song's energy and the listener's target on a 0–1 scale. A matching acoustic preference adds 0.5 points; tracks with acousticness at least 0.60 count as acoustic in this simulation. The system sorts by total score and returns the highest-ranked songs with a plain-language score explanation.

## 4. Data

The catalog contains 18 synthetic song records in `data/songs.csv`: the original 10 starter tracks plus 8 added tracks. Each record includes title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The recommender currently uses genre, mood, energy, and acousticness; the other numeric features are retained in the data for possible future work. The songs and feature values are illustrative rather than a real-world music dataset.

## 5. Strengths

The score and explanation make each ranking understandable. Profiles for Happy Pop, Chill Lofi, and Intense Rock produce different top results, and the energy calculation rewards closeness to a target rather than simply rewarding high energy. The CSV loader converts numeric fields so they can be compared mathematically.

## 6. Limitations and Bias

Genre receives 2 points, more than mood or energy similarity, so a genre match can dominate another relevant feature. In the high-energy, calm-mood edge case, *Spacewalk Thoughts* ranks first because its ambient genre and chill mood match even though its energy is much lower than the target. This may be reasonable for a listener who prioritizes genre and mood, but not for someone who values energy most. The small synthetic catalog, subjective labels, fixed weights, and acousticness threshold can all shape results unfairly or narrowly. The system does not learn from skips, likes, listening history, or changing context.

## 7. Evaluation

I ran the CLI on four profiles: Happy Pop, Chill Lofi, Intense Rock, and a high-energy profile with a calm mood. I checked whether top tracks and their explanations reflected the inputs. Chill Lofi returned the two lofi/chill tracks at the top, while Intense Rock put *Storm Runner* first. I also compared the default scoring with a weight-shift experiment that halved genre weight and doubled energy similarity; for Happy Pop, *Rooftop Lights* moved above *Gym Hero*. This shows how the ranking changes when energy matters more, without proving that the altered ranking is better for every listener.

## Profile Comparisons

- **Happy Pop vs. Chill Lofi:** Happy Pop ranks *Sunrise City* first because genre, mood, energy, and acoustic preference align. Chill Lofi ranks *Library Rain* first, with *Midnight Coding* close behind; low-energy lofi/chill tracks fit this profile.
- **Happy Pop vs. Intense Rock:** The Happy Pop profile favors the happy pop track *Sunrise City*. Intense Rock puts *Storm Runner* first because both its rock genre and intense mood match, with high energy adding to the score.
- **Happy Pop vs. High-Energy Calm Mood:** The edge case puts *Spacewalk Thoughts* first because its ambient genre and chill mood match, even though its low energy is far from the high-energy target. This shows that the category bonuses outweigh the energy mismatch here.
- **Chill Lofi vs. Intense Rock:** Chill Lofi favors quiet, acoustic tracks, while Intense Rock favors high-energy intense tracks such as *Storm Runner*. Their opposite energy targets produce clearly different top results.
- **Chill Lofi vs. High-Energy Calm Mood:** Both profiles reward chill, acoustic songs. The edge case ranks *Spacewalk Thoughts* first because ambient matches its genre preference, despite the high-energy target; Chill Lofi instead prefers *Library Rain* and *Midnight Coding*.
- **Intense Rock vs. High-Energy Calm Mood:** Both profiles target high energy, but their genre and mood preferences differ. Intense Rock ranks *Storm Runner* first; the edge case ranks *Spacewalk Thoughts* first because exact ambient and chill matches contribute more than energy similarity.

## 8. Future Work

- Add a diversity rule to reduce repeated artists or genres in the top results.
- Add listener feedback, such as likes and skips, and use it to adjust preferences.
- Test a wider catalog and more detailed, consistently defined audio and mood features.

## 9. Personal Reflection

This project showed me that recommendation systems can turn preference data into a ranked list through a sequence of understandable steps. I learned that the score alone is not enough: displaying the reasons helps reveal what the system is rewarding and makes unexpected results easier to discuss.

I was surprised that a simple weighted score can produce results that feel personalized, even though it misses much of what makes musical taste complicated. AI suggestions were useful for exploring possible scoring strategies and implementation structure, but the weights and explanations needed to be checked against the actual catalog. If I kept developing VibeFinder, I would add feedback and diversity so it could suggest relevant songs without repeating the same patterns.
