import requests
from colorama import init, Fore
import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting import format_cell_range, CellFormat, TextFormat

# Initialize colorama for color-coded console output
init(autoreset=True)

# API key for the Odds API
API_KEY = '16fdd193e7949e0ca1aced839093368b'
# Path to Google service account credentials file
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
# Google Sheets spreadsheet ID and worksheet name
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME = 'nba_odds'

# Scope for Google Sheets API
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
# Authenticate and connect to Google Sheets
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

# Clears all data in the Google Sheet
def clear_sheet():
    sheet.clear()

# Fetches NBA event data from the Odds API
def fetch_event_data():
    url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/events?apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Return event data as JSON if request is successful
    print(Fore.RED + f"Failed to retrieve event data. Status code: {response.status_code}")
    return []  # Return empty list on failure

# Fetches and processes odds data for selected events
def fetch_odds_for_selected_events():
    # Get list of events
    events = fetch_event_data()
    if not events:
        print(Fore.YELLOW + "No events available.")
        return

    # Display available events
    for i, event in enumerate(events, start=1):
        print(f"{i:2}. {event['home_team']} vs {event['away_team']}")

    # Prompt the user for event selection
    print("\nEnter the numbers of the events you want to process (comma separated).")
    print("Enter 'all' to process all events.")
    print("Enter 'quit' to quit the program.")
    user_input = input("Selection: ").strip()

    if user_input.lower() == 'quit':
        print(Fore.YELLOW + "Exiting the program...")
        exit()

    selected_events = []
    if user_input.lower() == 'all':
        # Select all events if 'all' is entered
        selected_events = [event['id'] for event in events]
    else:
        try:
            # Parse user input for selected events
            selected_event_indices = [int(x.strip()) - 1 for x in user_input.split(',')]
            selected_events = [events[i]['id'] for i in selected_event_indices]
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid selection.")
            exit()

    # Initialize rows for Google Sheets with column headers
    odds_rows = [["Player", "BetMGM", "DraftKings", "FanDuel", "PrizePicks", "Underdog", "Home Team", "Away Team"]]

    # Fetch odds data for each selected event
    for event_id in selected_events:
        url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/events/{event_id}/odds?apiKey={API_KEY}&regions=us&markets=player_points&dateFormat=iso&oddsFormat=decimal&bookmakers=betmgm,draftkings,fanduel,prizepicks,underdog"
        response = requests.get(url)
        if response.status_code == 200:
            event_data = response.json()
            if 'bookmakers' in event_data and event_data['bookmakers']:
                # Extract event details
                home_team = event_data.get('home_team', 'Unknown Home Team')
                away_team = event_data.get('away_team', 'Unknown Away Team')
                print(Fore.GREEN + f"Odds found for {home_team} vs {away_team}")

                # Process player odds from bookmakers
                player_odds = {}
                for bookmaker in event_data['bookmakers']:
                    for market in bookmaker.get('markets', []):
                        if market['key'] == 'player_points':
                            for outcome in market['outcomes']:
                                player = outcome['description']
                                points = outcome['point']
                                # Initialize player odds dictionary if not already present
                                if player not in player_odds:
                                    player_odds[player] = {'betmgm': None, 'draftkings': None, 'fanduel': None, 'prizepicks': None, 'underdog': None}
                                # Update odds for the player
                                player_odds[player][bookmaker['key']] = points

                # Sort and add player odds to the rows
                for player, odds in sorted(player_odds.items()):
                    odds_rows.append([
                        player,
                        odds['betmgm'] or 'null',
                        odds['draftkings'] or 'null',
                        odds['fanduel'] or 'null',
                        odds['prizepicks'] or 'null',
                        odds['underdog'] or 'null',
                        home_team,
                        away_team
                    ])
            else:
                print(Fore.YELLOW + f"No odds available for {event_data.get('home_team', 'Unknown Home Team')} vs {event_data.get('away_team', 'Unknown Away Team')}.")
        else:
            print(Fore.RED + f"Failed to retrieve odds for Event ID: {event_id}. Status code: {response.status_code}")

    if odds_rows:
        # Clear the Google Sheet and update it with new odds data
        clear_sheet()
        sheet.update(values=odds_rows, range_name='A1')
        format_cell_range(sheet, f'B2:I{len(odds_rows)}', CellFormat(horizontalAlignment='RIGHT'))
        format_cell_range(sheet, 'A1:I1', CellFormat(textFormat=TextFormat(bold=True)))
        print(Fore.GREEN + "Odds data has been successfully uploaded to Google Sheets.")
    else:
        print(Fore.YELLOW + "No odds data was found for the selected events.")

# Main function to start the program
def main():
    fetch_odds_for_selected_events()

# Entry point for the program
if __name__ == "__main__":
    main()
