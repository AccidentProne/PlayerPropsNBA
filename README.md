# NBA Data Scripts Collection

This repository contains a collection of Python scripts designed to retrieve and store NBA data. The focus is on team stats, player stats, odds, and event data. The scripts also integrate with Google Sheets, making the data easily accessible and analyzable.

## Features

### 1. **NBA Team Stats (Per Game)**
   - **Functionality**: Retrieves team statistics for the 2024-25 NBA season, focusing on per-game stats (e.g., minutes played).
   - **Google Sheets Integration**: Uploads the team stats to a specified Google Sheet, with formatting options for readability.
   - **Script**: `nba_team_stats_per_game.py`

### 2. **NBA Team Stats (Per 100 Possessions)**
   - **Functionality**: Retrieves team stats on a per-100 possessions basis, offering a better comparison of team efficiency.
   - **Google Sheets Integration**: Uploads the data to Google Sheets, formatted for easy viewing.
   - **Script**: `nba_team_stats_per_possessions.py`

### 3. **NBA Odds**
   - **Functionality**: Retrieves NBA events (games) and their associated odds from various sportsbooks (BetMGM, DraftKings, FanDuel, PrizePicks, Underdog).
   - **Fetch Player Odds**: Allows fetching player-specific odds for selected games.
   - **Google Sheets Integration**: Data is stored in Google Sheets for easy tracking.
   - **Script**: `nba_odds_script.py`

### 4. **Player Stats (Per Game)**
   - **Functionality**: Fetches player stats (e.g., minutes played) for the 2024-25 NBA season.
   - **Google Sheets Integration**: Uploads the data to Google Sheets.
   - **Script**: `nba_player_stats_per_game.py`

### 5. **Player Stats (Per 100 Possessions)**
   - **Functionality**: Retrieves player stats on a per-100 possessions basis, offering a more normalized comparison of player efficiency.
   - **Google Sheets Integration**: Uploads the data to Google Sheets.
   - **Script**: `nba_player_stats_per_possessions.py`

### 6. **Opponent Stats (Per 100 Possessions)**
   - **Functionality**: Fetches opponent team stats, like opponent field goals, points allowed, and defensive metrics, on a per-100 possessions basis.
   - **Google Sheets Integration**: Uploads the opponent stats to Google Sheets.
   - **Script**: `opponent_stats_per_pos.py`

### 7. **Team Pace (Per 100 Possessions)**
   - **Functionality**: Retrieves team pace stats (e.g., possessions per game) for the 2024-25 NBA season.
   - **Google Sheets Integration**: Uploads the pace data to Google Sheets.
   - **Script**: `nba_team_pace_per_pos.py`

---

## Requirements

- Python 3.x
- The following Python packages:
  - `requests`: For making HTTP requests to external APIs.
  - `gspread`: For interacting with Google Sheets.
  - `google-auth`: For authenticating with Google APIs.
  - `gspread-formatting`: For formatting Google Sheets.
  - `colorama`: For colored terminal output.
  - `nba_api`: For retrieving NBA stats from the NBA API.

Install the required dependencies with the following command:

```bash
pip install requests gspread google-auth gspread-formatting colorama nba_api
```

---

## Setup Instructions

1. **Clone the repository** or download the scripts to your local machine.
2. **Create Google Cloud credentials**: You need a Google service account with access to the Google Sheets API.
   - Follow the [Google Sheets API Quickstart Guide](https://developers.google.com/sheets/api/quickstart/python) to create a service account and download the `credentials` JSON file.
3. **Obtain an API key**: Get a valid API key from the odds API (e.g., Odds API) for retrieving event and player odds.
4. **Google Spreadsheet**: Create a Google Spreadsheet with write permissions. Update the `SPREADSHEET_ID` and `WORKSHEET_NAME` variables in each script with the appropriate details for your Google Sheets.
5. **Update file paths**: Ensure the path to your Google service account credentials (`SERVICE_ACCOUNT_FILE`) is correct in each script.

---

## Script Details

### 1. **NBA Team Stats Script (Per Game)** (`nba_team_stats_per_game.py`)

This script retrieves per-game team statistics (e.g., minutes played) for the 2024-25 NBA season and uploads the data to Google Sheets.

#### Example Usage:

```bash
python nba_team_stats_per_game.py
```

---

### 2. **NBA Team Stats Script (Per 100 Possessions)** (`nba_team_stats_per_possessions.py`)

This script retrieves team stats on a per-100 possessions basis, providing a more accurate comparison of team efficiency.

#### Example Usage:

```bash
python nba_team_stats_per_possessions.py
```

---

### 3. **NBA Odds Script** (`nba_odds_script.py`)

This script retrieves NBA event data (games) and associated odds from multiple sportsbooks (BetMGM, DraftKings, FanDuel, PrizePicks, Underdog). It also allows the user to select events and fetch player odds.

#### Example Usage:

```bash
python nba_odds_script.py
```

---

### 4. **Player Stats (Per Game)** (`nba_player_stats_per_game.py`)

This script retrieves player statistics (e.g., minutes played) for the 2024-25 NBA season and uploads them to Google Sheets.

#### Example Usage:

```bash
python nba_player_stats_per_game.py
```

---

### 5. **Player Stats (Per 100 Possessions)** (`nba_player_stats_per_possessions.py`)

This script retrieves player stats on a per-100 possessions basis, normalizing data for better comparison.

#### Example Usage:

```bash
python nba_player_stats_per_possessions.py
```

---

### 6. **Opponent Stats (Per 100 Possessions)** (`opponent_stats_per_pos.py`)

This script retrieves stats related to how NBA teams perform against their opponents (e.g., opponent points per possession, field goal attempts).

#### Example Usage:

```bash
python opponent_stats_per_pos.py
```

---

### 7. **Team Pace (Per 100 Possessions)** (`nba_team_pace_per_pos.py`)

This script retrieves NBA team pace stats (e.g., possessions per game) and uploads the data to Google Sheets.

#### Example Usage:

```bash
python nba_team_pace_per_pos.py
```

---

## Google Sheets Format

Each script uploads data in specific formats for easier analysis. Here are some examples:

### **Team Stats Format (Per Game)**:
| **Team** | **MIN** |
|----------|---------|
| Lakers   | 240     |
| Celtics  | 250     |
| ...      | ...     |

### **Team Stats Format (Per 100 Possessions)**:
| **Team** | **FGA** | **FG_PCT** | **FG3A** | **FG3_PCT** | **FTA** | **FT_PCT** | **OREB** | **DREB** | **AST** | **STL** | **BLK** | **PTS** |
|----------|---------|------------|----------|-------------|---------|------------|----------|----------|---------|---------|---------|---------|
| Lakers   | 80      | 48.5       | 32       | 36.7        | 15      | 77.5       | 10       | 35       | 22      | 8       | 5       | 112     |
| Celtics  | 78      | 45.0       | 28       | 38.5        | 13      | 81.0       | 12       | 34       | 24      | 9       | 6       | 115     |

### **Player Odds Format**:
| **Player Team** | **Opponent Team** | **Player**       | **BetMGM** | **DraftKings** | **FanDuel** | **PrizePicks** | **Underdog** |
|-----------------|-------------------|------------------|------------|----------------|-------------|----------------|--------------|
| Lakers          | Warriors           | LeBron James     | 25.5       | 26.0           | 25.0        | 24.5           | 26.5         |
| Celtics         | Heat               | Jayson Tatum     | 27.5       | 28.0           | 27.0        | 28.5           | 29.0         |

---

## Error Handling

- **API Request Failures**: If an API request fails, the script will print an error message with the HTTP status code.
- **No Odds Available**: If no bookmaker data is available for an event, a warning message will be displayed.
- **No Events or Odds Selected**: If no events are selected, or there are no odds data, the script will notify the user.

---

## License

This project is open-source and available under the [MIT License](LICENSE).