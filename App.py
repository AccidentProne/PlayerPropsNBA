import requests
import sqlite3
import colorama
from colorama import Fore

colorama.init(autoreset=True)

sport = 'basketball_nba'
apiKey = '16fdd193e7949e0ca1aced839093368b'

def initialize_database():
    conn = sqlite3.connect('NBA.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Events (
        id TEXT PRIMARY KEY,
        home_team TEXT,
        away_team TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Odds (
        player TEXT,
        betmgm REAL,
        draftkings REAL,
        fanduel REAL
    )""")

    conn.commit()
    conn.close()

def fetch_event_data():
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events?apiKey={apiKey}"
    response = requests.get(url)

    if response.status_code == 200:
        events_data = response.json()

        conn = sqlite3.connect('NBA.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Events")

        for event in events_data:
            cursor.execute("INSERT INTO Events (id, home_team, away_team) VALUES (?, ?, ?)",
                           (event['id'], event['home_team'], event['away_team']))

        conn.commit()
        conn.close()
        print(Fore.GREEN + "Event data has been successfully imported into the database.")
    else:
        print(Fore.RED + f"Failed to retrieve data. Status code: {response.status_code}")

def fetch_odds_for_selected_events():
    conn = sqlite3.connect('NBA.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, home_team, away_team FROM Events")
    events_data = cursor.fetchall()

    print()
    for i, event in enumerate(events_data, start=1):
        event_id, home_team, away_team = event
        event_num = f"{i:2}"
        print(f"{event_num}. Event ID: {event_id} | Home Team: {home_team} | Away Team: {away_team}")

    print("\nEnter the numbers of the events you want to process (comma separated).")
    print("Enter 'all' to process all events.")
    print("Enter 'quit' to quit the program.")
    user_input = input("Selection: ").strip()

    if user_input.lower() == 'quit':
        print(Fore.YELLOW + "Exiting the program...")
        conn.close()
        exit()

    if user_input.lower() == 'all':
        selected_events = [event[0] for event in events_data]
    else:
        try:
            selected_event_indices = [int(x.strip()) - 1 for x in user_input.split(',')]
            selected_events = [events_data[i][0] for i in selected_event_indices]
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid selection.")
            conn.close()
            exit()

    print()

    for event_id in selected_events:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds?apiKey={apiKey}&regions=us&markets=player_points&dateFormat=iso&oddsFormat=decimal&bookMakers=betmgm,draftkings,fanduel"
        response = requests.get(url)

        if response.status_code == 200:
            events_data = response.json()

            player_odds = {}

            if isinstance(events_data, dict):
                if not events_data.get('bookmakers'):
                    if 'home_team' in events_data and 'away_team' in events_data:
                        print(Fore.YELLOW + f"No bookmakers data for {events_data['home_team']} vs {events_data['away_team']}")

                else:
                    home_team = events_data.get('home_team', 'Unknown Home Team')
                    away_team = events_data.get('away_team', 'Unknown Away Team')
                    print(Fore.GREEN + f"Processing odds for {home_team} vs {away_team} (Event ID: {event_id})")

                    for bookmaker in events_data['bookmakers']:
                        if bookmaker['key'] in ['betmgm', 'draftkings', 'fanduel']:
                            if 'markets' in bookmaker and isinstance(bookmaker['markets'], list):
                                for market in bookmaker['markets']:
                                    if market['key'] == 'player_points':
                                        for outcome in market['outcomes']:
                                            player = outcome['description']
                                            points = outcome['point']
                                            odds = outcome['price']

                                            if player not in player_odds:
                                                player_odds[player] = {'betmgm': None, 'draftkings': None, 'fanduel': None}

                                            if bookmaker['key'] == 'betmgm':
                                                player_odds[player]['betmgm'] = points
                                            elif bookmaker['key'] == 'draftkings':
                                                player_odds[player]['draftkings'] = points
                                            elif bookmaker['key'] == 'fanduel':
                                                player_odds[player]['fanduel'] = points

            for player, odds in player_odds.items():
                cursor.execute("""
                INSERT INTO Odds (Player, betmgm, draftkings, fanduel)
                VALUES (?, ?, ?, ?)
                """, (player,
                      odds['betmgm'],
                      odds['draftkings'],
                      odds['fanduel']))

            conn.commit()

        else:
            print(Fore.RED + f"Failed to retrieve data for Event ID: {event_id}. Status code: {response.status_code}")

    conn.close()
    print(Fore.GREEN + "Odds data has been successfully imported into the database.")

def main():
    initialize_database()
    fetch_event_data()
    fetch_odds_for_selected_events()

if __name__ == "__main__":
    main()