NBA Odds Script
This script fetches NBA game data and player odds from various sportsbooks (BetMGM, DraftKings, FanDuel, PrizePicks, and Underdog) and stores the information in an SQLite database. It provides an interactive command-line interface that allows users to choose specific events for which they want to retrieve player odds.

Features
Fetch NBA Events: Retrieves a list of NBA events (games) using an API and stores them in a local SQLite database.
Fetch Player Odds: Retrieves player point odds for selected NBA games from BetMGM, DraftKings, FanDuel, PrizePicks, and Underdog.
Database Storage: Data is saved in an SQLite database (NBA.db) for easy querying.
User Interaction: Prompts the user to select events for which they want to retrieve odds and processes them accordingly.
Requirements
Python 3.x
The following Python packages:
requests: To make HTTP requests to the odds API.
sqlite3: To manage the SQLite database.
colorama: To add color to the terminal output.
gspread and google-auth: For integrating with Google Sheets if desired.
gspread_formatting: For formatting cells in Google Sheets.
You can install the necessary packages using the following command:

bash
Copy code
pip install requests colorama gspread google-auth gspread-formatting
Setup
Clone the repository or download the script to your local machine.
Open a terminal/command prompt and navigate to the directory where the script is located.
Ensure that you have a valid API key for the odds API and replace the apiKey value in the script with your own.
Usage
Initialize Database: The script creates two tables in the NBA.db SQLite database: Events (for storing NBA events) and Odds (for storing player odds).

Fetch Events: The script will fetch a list of NBA games and store them in the Events table.

Select Events to Process: After fetching events, the script displays them and prompts the user to select events for processing. You can select events by number (comma separated) or choose to process all events. Type quit to exit the program.

Fetch and Store Player Odds: The script retrieves player odds for the selected events from BetMGM, DraftKings, FanDuel, PrizePicks, and Underdog. The odds are stored in the Odds table.

Database Updates: Data for each game is updated in the database, and the script prints a success message once the data is processed.

Example Run
bash
Copy code
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
Database Schema
Events Table:

id: Unique event identifier.
home_team: Name of the home team.
away_team: Name of the away team.
Odds Table:

player: Player name.
betmgm: Player's point odds at BetMGM.
draftkings: Player's point odds at DraftKings.
fanduel: Player's point odds at FanDuel.
prizepicks: Player's point odds at PrizePicks.
underdog: Player's point odds at Underdog.
