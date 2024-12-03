import requests
import colorama
from colorama import Fore
import gspread
from google.oauth2.service_account import Credentials
import warnings
from gspread_formatting import *

# Suppress warnings for deprecated features
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize colorama for colored output
colorama.init(autoreset=True)

# API Key for the Odds API
apiKey = '16fdd193e7949e0ca1aced839093368b'

# Google Sheets credentials and details
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'  # Path to your service account credentials file
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'  # Google Sheets ID
WORKSHEET_NAME = 'Lines Import'  # Worksheet name where data will be uploaded

# Google Sheets API scope and authentication
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

# Function to clear the worksheet before uploading new data
def clear_sheet():
    sheet.clear()

# Function to fetch event data from the Odds API
def fetch_event_data():
    # URL to get NBA events for today
    url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/events?apiKey={apiKey}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()  # Return event data in JSON format
    else:
        print(Fore.RED + f"Failed to retrieve event data. Status code: {response.status_code}")
        return []  # Return an empty list if there is an error

# Function to fetch odds for selected events
def fetch_odds_for_selected_events():
    # Fetch events data
    events = fetch_event_data()
    if not events:
        print(Fore.YELLOW + "No events available.")
        return

    # Display the list of events to the user
    print()
    for i, event in enumerate(events, start=1):
        print(f"{i:2}. {event['home_team']} vs {event['away_team']}")

    print("\nEnter the numbers of the events you want to process (comma separated).")
    print("Enter 'all' to process all events.")
    print("Enter 'quit' to quit the program.")
    user_input = input("Selection: ").strip()

    # Exit if user wants to quit
    if user_input.lower() == 'quit':
        print(Fore.YELLOW + "Exiting the program...")
        exit()

    # Select all events if the user types 'all'
    if user_input.lower() == 'all':
        selected_events = [event['id'] for event in events]
    else:
        try:
            # Parse user input to select specific events
            selected_event_indices = [int(x.strip()) - 1 for x in user_input.split(',')]
            selected_events = [events[i]['id'] for i in selected_event_indices]
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid selection.")
            exit()

    print()

    # Prepare a list of headers for the Google Sheet
    odds_rows = [["Player", "BetMGM", "DraftKings", "FanDuel", "PrizePicks", "Underdog"]]

    # Loop through each selected event and fetch odds data
    for event_id in selected_events:
        url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/events/{event_id}/odds?apiKey={apiKey}&regions=us&markets=player_points&dateFormat=iso&oddsFormat=decimal&bookmakers=betmgm,draftkings,fanduel,prizepicks,underdog"
        response = requests.get(url)

        if response.status_code == 200:
            event_data = response.json()
            if 'bookmakers' in event_data and event_data['bookmakers']:
                # Extract event details
                home_team = event_data.get('home_team', 'Unknown Home Team')
                away_team = event_data.get('away_team', 'Unknown Away Team')
                print(Fore.GREEN + f"Odds found for {home_team} vs {away_team}")
                
                # Dictionary to hold player odds for each bookmaker
                player_odds = {}

                # Loop through each bookmaker and collect player points odds
                for bookmaker in event_data['bookmakers']:
                    if bookmaker['key'] in ['betmgm', 'draftkings', 'fanduel', 'prizepicks', 'underdog']:
                        for market in bookmaker.get('markets', []):
                            if market['key'] == 'player_points':  # Focus on player points market
                                for outcome in market['outcomes']:
                                    player = outcome['description']  # Player name
                                    points = outcome['point']  # Points value

                                    # If the player is not in the dictionary, initialize them
                                    if player not in player_odds:
                                        player_odds[player] = {'betmgm': None, 'draftkings': None, 'fanduel': None, 'prizepicks': None, 'underdog': None}

                                    # Store the odds for each bookmaker
                                    player_odds[player][bookmaker['key']] = points

                # Sort player odds alphabetically by last name
                sorted_player_odds = sorted(player_odds.items(), key=lambda x: x[0].split()[-1].lower())

                # Add the sorted player odds to the list
                for player, odds in sorted_player_odds:
                    odds_rows.append([
                        player,
                        odds['betmgm'] if odds['betmgm'] is not None else 'null',
                        odds['draftkings'] if odds['draftkings'] is not None else 'null',
                        odds['fanduel'] if odds['fanduel'] is not None else 'null',
                        odds['prizepicks'] if odds['prizepicks'] is not None else 'null',
                        odds['underdog'] if odds['underdog'] is not None else 'null'
                    ])
            else:
                # If no odds found, notify the user
                home_team = event_data.get('home_team', 'Unknown Home Team')
                away_team = event_data.get('away_team', 'Unknown Away Team')
                print(Fore.YELLOW + f"No odds available for {home_team} vs {away_team}.")
        else:
            # Handle failed API call
            print(Fore.RED + f"Failed to retrieve odds for Event ID: {event_id}. Status code: {response.status_code}")

    # If there are any odds rows to upload, clear the sheet and update it
    if odds_rows:
        clear_sheet()
        sheet.update(values=odds_rows, range_name='A1')
        format_cell_range(sheet, 'B2:F' + str(len(odds_rows) + 1), CellFormat(horizontalAlignment='RIGHT'))

        # Format header row to be bold
        header_format = CellFormat(textFormat=TextFormat(bold=True))
        format_cell_range(sheet, 'A1:F1', header_format)

        print(Fore.GREEN + "\nOdds data has been successfully uploaded to Google Sheets.")
    else:
        print(Fore.YELLOW + "No odds data was found for the selected events.")

# Main entry point of the script
def main():
    fetch_odds_for_selected_events()

# Run the script when executed
if __name__ == "__main__":
    main()
