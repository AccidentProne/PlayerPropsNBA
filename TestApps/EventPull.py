import requests
import sqlite3

sport = 'basketball_nba'
apiKey = '16fdd193e7949e0ca1aced839093368b'

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
    print("Data has been successfully imported into the database.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
