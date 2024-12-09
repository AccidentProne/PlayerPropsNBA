import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME = 'nba_odds'

def main():
    # Authenticate and connect to Google Sheets
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

    # Load the data from Google Sheets into a Pandas DataFrame
    data = pd.DataFrame(sheet.get_all_records())

    # Ensure required columns exist
    required_columns = {'TEAM_NAME', 'Home Team', 'Away Team'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Missing one or more required columns: {required_columns - set(data.columns)}")

    # Function to determine the opponent
    def get_opponent(row):
        if row['TEAM_NAME'] == row['Home Team']:
            return row['Away Team']
        else:
            return row['Home Team']

    # Add the "Opponent" column to the DataFrame
    data['Opponent'] = data.apply(get_opponent, axis=1)

    # Reorder the columns to place "Opponent" in column C
    columns = list(data.columns)
    columns.insert(2, columns.pop(columns.index('Opponent')))  # Move "Opponent" to column C
    data = data[columns]

    # Clear "Home Team" and "Away Team" columns
    data = data.drop(columns=['Home Team', 'Away Team'])

    # Update the Google Sheet with the updated DataFrame
    sheet.clear()
    sheet.update([data.columns.values.tolist()] + data.values.tolist())

    print("Opponent Team stats have been successfully uploaded to 'nba_odds' sheet.")

if __name__ == "__main__":
    main()
