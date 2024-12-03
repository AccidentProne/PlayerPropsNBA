# NBA Scripts Collection

This repository contains a collection of Python scripts designed to retrieve and store NBA data, including team stats, player odds, and event data, all while leveraging Google Sheets integration for easy access and analysis.

## Features

### 1. **NBA Team Stats Script (Per Game)**
   - **Fetch Team Stats**: Retrieves team statistics for the 2024-25 NBA season, focusing on per-game stats (e.g., minutes played).
   - **Google Sheets Integration**: Uploads the team stats to a specified Google Sheet, with the option to format the data for easy readability.

### 2. **NBA Team Stats Script (Per 100 Possessions)**
   - **Fetch Stats per 100 Possessions**: Retrieves team stats on a per-100 possessions basis, which provides a better comparison of team efficiency.
   - **Google Sheets Integration**: Uploads the data to Google Sheets, formatting it similarly to the per-game stats.

### 3. **NBA Odds Script**
   - **Fetch NBA Events**: Retrieves NBA events (games) and their associated odds from various sportsbooks (BetMGM, DraftKings, FanDuel, PrizePicks, Underdog).
   - **Fetch Player Odds**: For each selected event, fetches player point odds from the above sportsbooks.
   - **Google Sheets Integration**: Data is stored in a Google Sheet for easy tracking and analysis.

### 4. **Player Props Script (Unspecified)**
   - **Fetch Player Props**: Retrieves player performance data (e.g., points, assists, rebounds) for NBA games and stores them in Google Sheets.
   - **Sportsbook Odds**: Works similarly to the NBA Odds script, fetching player-specific betting odds.

### 5. **NBA Event Data Script (Unspecified)**
   - **Fetch NBA Events**: Retrieves detailed event data such as game time, teams playing, and other relevant information.
   - **Google Sheets Integration**: Uploads the event details to a specified Google Sheet, similar to the NBA Odds script for easy tracking.

---

## Requirements

- Python 3.x
- The following Python packages:
  - `requests`: To make HTTP requests to the odds API.
  - `gspread`: To interact with Google Sheets.
  - `google-auth`: For authenticating with Google APIs.
  - `gspread-formatting`: To format the Google Sheet.
  - `colorama`: For adding color to the terminal output.
  - `nba_api`: For retrieving NBA stats.

Install the necessary packages using the following command:

```bash
pip install requests gspread google-auth gspread-formatting colorama nba_api
```

## Setup

1. **Clone the repository** or download the scripts to your local machine.
2. **Create Google Cloud credentials**: You need a Google service account with access to the Google Sheets API.
   - Follow the [Google Sheets API Quickstart Guide](https://developers.google.com/sheets/api/quickstart/python) to create a service account and download the `credentials` JSON file.
3. **API Key**: Obtain a valid API key from the odds API (like the Odds API or similar providers) for retrieving event and player odds.
4. **Google Spreadsheet**: Ensure you have a Google Spreadsheet with write permissions. Update the `SPREADSHEET_ID` and `WORKSHEET_NAME` variables in the scripts with your specific Google Sheet details.

## Scripts Overview

### 1. **NBA Team Stats Script (Per Game)** (`nba_team_stats_per_game.py`)

This script fetches NBA team stats (per game) for the 2024-25 season and uploads them to Google Sheets.

#### Features:
- **Fetch Team Stats**: Retrieves per-game stats (e.g., minutes played).
- **Google Sheets Integration**: Clears and updates the Google Sheet with the fetched stats.
- **Formatting**: Automatically formats the header row and aligns numerical data.

#### Example Usage:

```bash
python nba_team_stats_per_game.py
```

---

### 2. **NBA Team Stats Script (Per 100 Possessions)** (`nba_team_stats_per_100_possessions.py`)

This script fetches NBA team stats per 100 possessions for more accurate comparisons.

#### Features:
- **Fetch Stats per 100 Possessions**: Retrieves efficiency stats per 100 possessions.
- **Google Sheets Integration**: Uploads the data to Google Sheets, formatted for easy viewing.
- **Data Adjustments**: Adjusts values (e.g., field goal percentage) and rounds to three decimal places.

#### Example Usage:

```bash
python nba_team_stats_per_100_possessions.py
```

---

### 3. **NBA Odds Script** (`nba_odds_script.py`)

This script fetches NBA game data and player odds from multiple sportsbooks and stores it in Google Sheets.

#### Features:
- **Fetch NBA Events**: Retrieves a list of NBA games along with odds.
- **Fetch Player Odds**: Retrieves player point odds for selected games from BetMGM, DraftKings, FanDuel, PrizePicks, and Underdog.
- **User Interaction**: Allows users to choose which games to process.
- **Google Sheets Integration**: Stores the player odds data in a structured format in Google Sheets.

#### Example Usage:

```bash
python nba_odds_script.py
```

---

### 4. **Player Props Script** (`nba_player_props.py`)

This script is designed to retrieve player-specific betting odds (points, assists, etc.) for NBA games and store the data in Google Sheets.

#### Features:
- **Fetch Player Props**: Retrieves player props like points, assists, rebounds, etc.
- **Google Sheets Integration**: Data is uploaded and formatted in Google Sheets.
  
---

### 5. **NBA Event Data Script** (`nba_event_data.py`)

This script retrieves event data such as game schedules and teams playing.

#### Features:
- **Fetch Event Data**: Retrieves basic event information (game time, teams, etc.).
- **Google Sheets Integration**: Updates the Google Sheet with detailed event data.

---

## Google Sheets Format

The NBA scripts will update the Google Sheet in the following formats:

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
| ...      | ...     | ...        | ...      | ...         | ...     | ...        | ...      | ...      | ...     | ...     | ...     | ...     |

### **Player Odds Format**:
| **Player Team** | **Opponent Team** | **Player**       | **BetMGM** | **DraftKings** | **FanDuel** | **PrizePicks** | **Underdog** |
|-----------------|-------------------|------------------|------------|----------------|-------------|----------------|--------------|
| Lakers          | Warriors           | LeBron James     | 25.5       | 26.0           | 25.0        | 24.5           | 26.5         |
| Celtics         | Heat               | Jayson Tatum     | 27.5       | 28.0           | 27.0        | 28.5           | 29.0         |
| ...             | ...               | ...              | ...        | ...            | ...         | ...            | ...          |

---

## Error Handling

- **API Request Failures**: If an API request fails, the script will print an error message with the HTTP status code.
- **No Odds Available**: If no bookmaker data is available for an event, a warning message will be displayed.
- **No Events or Odds Selected**: If no events are selected, or there are no odds data, the script will notify the user.

---

## License

This project is open-source and available under the [MIT License](LICENSE).