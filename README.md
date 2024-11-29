# NBA Odds Script

This script fetches NBA game data and player odds from various sportsbooks (BetMGM, DraftKings, FanDuel, PrizePicks, Underdog) and stores the information in a Google Spreadsheet. It provides an interactive command-line interface that allows users to choose specific events for which they want to retrieve player odds.

## Features

- **Fetch NBA Events**: Retrieves a list of NBA games and their associated odds using an API.
- **Fetch Player Odds**: Retrieves player point odds for selected NBA games from BetMGM, DraftKings, FanDuel, PrizePicks, and Underdog.
- **Google Sheets Integration**: Data is saved in a Google Spreadsheet for easy access.
- **User Interaction**: Prompts the user to select events to process and retrieve player odds for.

## Requirements

- Python 3.x
- The following Python packages:
  - `requests`: To make HTTP requests to the odds API.
  - `gspread`: To manage Google Sheets.
  - `google-auth`: For authenticating with Google APIs.
  - `gspread-formatting`: To format the Google Sheet.
  - `colorama`: To add color to the terminal output.

Install the necessary packages using the following command:

```bash
pip install requests gspread google-auth gspread-formatting colorama
```

## Setup

1. **Clone the repository** or download the script to your local machine.
2. **Create Google Cloud credentials**: You need a Google service account with access to Google Sheets API.
   - Follow the [Google Sheets API Quickstart Guide](https://developers.google.com/sheets/api/quickstart/python) to create a service account and download the `credentials` JSON file.
3. **API Key**: You will need a valid API key from the odds API (like the Odds API or any similar provider) for retrieving event and player odds. Replace the `apiKey` variable with your own key in the script.
4. **Google Spreadsheet**: Ensure you have a Google Spreadsheet with write permissions, and update the `SPREADSHEET_ID` and `WORKSHEET_NAME` variables in the script.

## Usage

1. **Initialize Google Sheets**: The script will interact with Google Sheets and update the values. Ensure that the necessary permissions are set on your Google Spreadsheet for the service account.
2. **Fetch Events**: The script fetches NBA events (games) and presents them in the terminal.
3. **Select Events to Process**: After fetching events, the script displays them and prompts the user to select the events for processing. You can select events by number (comma separated) or choose to process all events. Type `quit` to exit the program.
4. **Fetch and Store Player Odds**: The script retrieves player odds for the selected events and stores them in the Google Sheet.
5. **Google Sheets Update**: The script updates the sheet with the player odds and formats the data for easy viewing.

### Example Run

```bash
$ python NBA_Odds_Script.py
Event ID: 1 | Home Team: Lakers | Away Team: Warriors
Event ID: 2 | Home Team: Celtics | Away Team: Heat
...

Enter the numbers of the events you want to process (comma separated).
Enter 'all' to process all events.
Enter 'quit' to quit the program.
Selection: 1,2
Processing odds for Lakers vs Warriors (Event ID: 1)
Processing odds for Celtics vs Heat (Event ID: 2)
...
```

### Google Sheets Format

The script will output the following columns to your Google Sheet:

| **Player Team** | **Opponent Team** | **Player** | **BetMGM** | **DraftKings** | **FanDuel** | **PrizePicks** | **Underdog** |
|-----------------|-------------------|------------|------------|----------------|-------------|----------------|--------------|
| Lakers          | Warriors           | LeBron James | 25.5       | 26.0           | 25.0        | 24.5           | 26.5         |
| Celtics         | Heat               | Jayson Tatum | 27.5       | 28.0           | 27.0        | 28.5           | 29.0         |
| ...             | ...               | ...        | ...        | ...            | ...         | ...            | ...          |

### Database Schema

- **Google Sheets Format**:
  - `Player Team`: The team of the player (either Home Team or Away Team).
  - `Opponent Team`: The opposing team.
  - `Player`: The name of the player.
  - `BetMGM`, `DraftKings`, `FanDuel`, `PrizePicks`, `Underdog`: The odds for the player from each respective bookmaker.

### Script Overview

1. **Clear Sheet**: Clears the existing data in the Google Sheet before updating.
2. **Fetch Event Data**: Fetches a list of NBA events (games) from the API.
3. **Fetch Odds Data**: For each selected event, fetches player point odds from multiple sportsbooks (BetMGM, DraftKings, FanDuel, PrizePicks, and Underdog).
4. **Assign Teams**: Each player's team is assumed to be from the home team (you can update the logic as needed).
5. **Update Google Sheet**: The odds data is updated in a structured format with the columns:
   - **Player Team**
   - **Opponent Team**
   - **Player**
   - **BetMGM**, **DraftKings**, **FanDuel**, **PrizePicks**, **Underdog**.

## Error Handling

- If an API request fails, the script will print an error message with the HTTP status code.
- If no bookmaker data is available for an event, a warning message will be displayed.
- If no events are selected, or there are no odds data, the script will notify the user.

## License

This project is open-source and available under the [MIT License](LICENSE).
