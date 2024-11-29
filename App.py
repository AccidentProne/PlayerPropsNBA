import requests
import colorama
from colorama import Fore
import gspread
from google.oauth2.service_account import Credentials
import warnings
from gspread_formatting import *

warnings.filterwarnings("ignore", category=DeprecationWarning)

colorama.init(autoreset=True)

apiKey = '16fdd193e7949e0ca1aced839093368b'
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME = 'Lines Import'

SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

def clear_sheet():
    sheet.clear()

def fetch_event_data():
    url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/events?apiKey={apiKey}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.RED + f"Failed to retrieve event data. Status code: {response.status_code}")
        return []

def fetch_odds_for_selected_events():
    events = fetch_event_data()
    if not events:
        print(Fore.YELLOW + "No events available.")
        return

    print()
    for i, event in enumerate(events, start=1):
        print(f"{i:2}. Event: {event['home_team']} vs {event['away_team']}")

    print("\nEnter the numbers of the events you want to process (comma separated).")
    print("Enter 'all' to process all events.")
    print("Enter 'quit' to quit the program.")
    user_input = input("Selection: ").strip()

    if user_input.lower() == 'quit':
        print(Fore.YELLOW + "Exiting the program...")
        exit()

    if user_input.lower() == 'all':
        selected_events = [event['id'] for event in events]
    else:
        try:
            selected_event_indices = [int(x.strip()) - 1 for x in user_input.split(',')]
            selected_events = [events[i]['id'] for i in selected_event_indices]
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid selection.")
            exit()

    print()

    odds_rows = [["Player", "BetMGM", "DraftKings", "FanDuel", "PrizePicks", "Underdog"]]

    for event_id in selected_events:
        url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/events/{event_id}/odds?apiKey={apiKey}&regions=us&markets=player_points&dateFormat=iso&oddsFormat=decimal&bookmakers=betmgm,draftkings,fanduel,prizepicks,underdog"
        response = requests.get(url)

        if response.status_code == 200:
            event_data = response.json()
            if 'bookmakers' in event_data and event_data['bookmakers']:
                home_team = event_data.get('home_team', 'Unknown Home Team')
                away_team = event_data.get('away_team', 'Unknown Away Team')
                print(Fore.GREEN + f"Odds found for {home_team} vs {away_team}")
                player_odds = {}

                for bookmaker in event_data['bookmakers']:
                    if bookmaker['key'] in ['betmgm', 'draftkings', 'fanduel', 'prizepicks', 'underdog']:
                        for market in bookmaker.get('markets', []):
                            if market['key'] == 'player_points':
                                for outcome in market['outcomes']:
                                    player = outcome['description']
                                    points = outcome['point']

                                    if player not in player_odds:
                                        player_odds[player] = {'betmgm': None, 'draftkings': None, 'fanduel': None, 'prizepicks': None, 'underdog': None}

                                    player_odds[player][bookmaker['key']] = points

                for player, odds in player_odds.items():
                    odds_rows.append([
                        player,
                        odds['betmgm'] if odds['betmgm'] is not None else 'null',
                        odds['draftkings'] if odds['draftkings'] is not None else 'null',
                        odds['fanduel'] if odds['fanduel'] is not None else 'null',
                        odds['prizepicks'] if odds['prizepicks'] is not None else 'null',
                        odds['underdog'] if odds['underdog'] is not None else 'null'
                    ])
            else:
                home_team = event_data.get('home_team', 'Unknown Home Team')
                away_team = event_data.get('away_team', 'Unknown Away Team')
                print(Fore.YELLOW + f"No odds available for {home_team} vs {away_team}.")
        else:
            print(Fore.RED + f"Failed to retrieve odds for Event ID: {event_id}. Status code: {response.status_code}")

    if odds_rows:
        clear_sheet()
        sheet.update(values=odds_rows, range_name='A1')
        format_cell_range(sheet, 'B2:F' + str(len(odds_rows) + 1), CellFormat(horizontalAlignment='RIGHT'))

        header_format = CellFormat(textFormat=TextFormat(bold=True))
        format_cell_range(sheet, 'A1:F1', header_format)

        print(Fore.GREEN + "\nOdds data has been successfully uploaded to Google Sheets.")
    else:
        print(Fore.YELLOW + "No odds data was found for the selected events.")

def main():
    fetch_odds_for_selected_events()

if __name__ == "__main__":
    main()
