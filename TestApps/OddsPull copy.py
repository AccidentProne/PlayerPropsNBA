import requests
import sqlite3

sport = 'basketball_nba'
apiKey = '16fdd193e7949e0ca1aced839093368b'

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

cursor.execute("SELECT id, home_team, away_team FROM Events")
events_data = cursor.fetchall()

print("List of events:")
for i, event in enumerate(events_data, start=1):
    event_id, home_team, away_team = event
    print(f"{i}. Event ID: {event_id} | Home Team: {home_team} | Away Team: {away_team}")

print("\nEnter the numbers of the events you want to process (comma separated).")
print("Enter 'all' to process all events.")
user_input = input("Selection: ").strip()

if user_input.lower() == 'all':
    selected_events = [event[0] for event in events_data]
else:
    try:
        selected_event_indices = [int(x.strip()) - 1 for x in user_input.split(',')]
        selected_events = [events_data[i][0] for i in selected_event_indices]
    except ValueError:
        print("Invalid input. Please enter a valid selection.")
        conn.close()
        exit()

for event_id in selected_events:
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds?apiKey={apiKey}&regions=us&markets=player_points&dateFormat=iso&oddsFormat=decimal&bookMakers=betmgm,draftkings,fanduel"
    response = requests.get(url)

    if response.status_code == 200:
        events_data = response.json()

        player_odds = {}

        if isinstance(events_data, dict):
            if not events_data.get('bookmakers'):
                if 'home_team' in events_data and 'away_team' in events_data:
                    print(f"No bookmakers data for {events_data['home_team']} vs {events_data['away_team']}, skipping event.")
            else:
                home_team = events_data.get('home_team', 'Unknown Home Team')
                away_team = events_data.get('away_team', 'Unknown Away Team')
                print(f"Processing odds for {home_team} vs {away_team} (Event ID: {event_id})")

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
        print(f"Failed to retrieve data for Event ID: {event_id}. Status code: {response.status_code}")

conn.close()

print("Odds data has been successfully imported into the database.")
