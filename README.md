# CKL Tracker Bot

A Discord bot that keeps our CKL team's Mario Kart 8 Deluxe race results and turns them into stats:
who does best on which track, head-to-head comparisons, and which tracks the team should pick.

Placements are converted to points on the standard 12-player scale (1st = 15, 2nd = 12, 3rd = 10, down to
12th = 1), and every track is known by its usual abbreviation, with autocomplete for track and player names.

## Commands

| Command | What it does |
| --- | --- |
| `/add_ckl_race race placements` | Record a race, e.g. `placements: Noah, 1; Gabe, 2`. Asks you to confirm before saving |
| `/ckl_stats user` | A player's average placement and points, with their best and worst tracks |
| `/best user by count` | A player's best tracks, by placement or by points |
| `/worst user by count` | A player's worst tracks |
| `/most_frequent user count` | Tracks a player has raced most |
| `/rarest user count` | Tracks a player has raced least |
| `/compare user1 user2 race` | Two players head to head on one track |
| `/compare_all race` | Every player on one track |
| `/find_best_team_races count` | The team's strongest tracks, averaging points across players and scaling to a 6-person team |
| `/show_raw_race_data user race` | Every placement a player has recorded on a track |
| `/update` | Reload the data from storage |
| `/help` | List the commands in Discord |

## Setup

Results are stored as `data.json` in a Google Cloud Storage bucket (`rit_ckl_stats`, set in `utils.py`),
so every instance of the bot sees the same data.

1. Create a Discord application with a bot user, and invite it to your server with the
   `applications.commands` scope.
2. Create a GCS bucket and a service account that can read and write it.
3. Set these environment variables, or put them in a `.env` file (keep it out of git):

   ```ini
   TOKEN=your-discord-bot-token
   GOOGLE_APPLICATION_CREDENTIALS=base64-encoded service account JSON
   ```

4. Install and run:

   ```sh
   pip install -r requirements.txt
   python main.py
   ```

The `Procfile` runs it as a worker process on Heroku or a similar host.
