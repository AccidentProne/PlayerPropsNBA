import gspread
from google.oauth2.service_account import Credentials

# Path to Google service account credentials file
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'

# Google Sheets spreadsheet ID and worksheet names
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
NBA_ODDS_WORKSHEET = 'nba_odds'
GAME_IMPORT_WORKSHEET = 'game_import'

# Scope for Google Sheets API
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
# Authenticate and connect to Google Sheets
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)

# Access the worksheets
nba_odds_sheet = client.open_by_key(SPREADSHEET_ID).worksheet(NBA_ODDS_WORKSHEET)
game_import_sheet = client.open_by_key(SPREADSHEET_ID).worksheet(GAME_IMPORT_WORKSHEET)

# Function to read home and away teams from nba_odds and write to game_import
def import_unique_games():
    # Read all data from nba_odds
    nba_odds_data = nba_odds_sheet.get_all_values()
    
    # Check if sheet has data
    if not nba_odds_data or len(nba_odds_data) < 2:
        print("No data found in nba_odds sheet.")
        return

    # Extract headers and data rows
    headers = nba_odds_data[0]
    rows = nba_odds_data[1:]
    
    # Find the index of the home and away team columns
    try:
        home_team_index = headers.index("Home Team")
        away_team_index = headers.index("Away Team")
    except ValueError:
        print("Home Team or Away Team columns not found in nba_odds sheet.")
        return

    # Create a set of unique game pairs (home team, away team)
    unique_games = {(row[home_team_index], row[away_team_index]) for row in rows if row[home_team_index] and row[away_team_index]}

    # Prepare data for game_import sheet
    game_import_data = [["Home Team", "Away Team"]]  # Headers
    game_import_data += [[home, away] for home, away in sorted(unique_games)]

    # Clear game_import sheet and update it with unique games
    game_import_sheet.clear()
    game_import_sheet.update('A1', game_import_data)
    print("Game data successfully imported into game_import sheet.")

# Main function
def main():
    import_unique_games()

# Entry point for the script
if __name__ == "__main__":
    main()
