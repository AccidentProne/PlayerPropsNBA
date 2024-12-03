import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from nba_api.stats.endpoints import leaguedashteamstats
from gspread_formatting import *
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Google Sheets credentials and setup
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_TEAM_PACE = 'Team Pace'

# Setup the Google Sheets client
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)

# Function to get or create the worksheet
def get_or_create_worksheet(spreadsheet_id, worksheet_name):
    try:
        sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        # Create the worksheet if it does not exist
        spreadsheet = client.open_by_key(spreadsheet_id)
        sheet = spreadsheet.add_worksheet(title=worksheet_name, rows=100, cols=10)  # Adjust rows/cols as needed
        print(f"Worksheet '{worksheet_name}' created.")
    return sheet

# Function to fetch team stats and ensure PACE is retrieved
def fetch_team_pace():
    # Fetching advanced team stats from the NBA API (Per 100 possessions)
    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        per_mode_detailed='Per100Possessions',
        season='2024-25',
        season_type_all_star='Regular Season',
        measure_type_detailed_defense='Advanced'
    )
    
    # Convert the data into a pandas DataFrame
    stats_df = team_stats.get_data_frames()[0]
    
    # Debug: Print available columns
    print("Available columns in the DataFrame:")
    print(stats_df.columns)
    
    # Ensure PACE exists in the response
    if 'PACE' not in stats_df.columns:
        raise KeyError("'PACE' column not found in the returned data. Please verify the API response.")
    
    # Select TEAM_NAME and PACE for the output
    team_pace_df = stats_df[['TEAM_NAME', 'PACE']]
    return team_pace_df

# Function to clear the content of the sheet
def clear_sheet(sheet):
    sheet.clear()

# Function to upload team pace stats to the Google Sheets
def upload_team_pace_to_sheet():
    # Fetch team pace stats from the NBA API
    team_pace_df = fetch_team_pace()
    
    # Prepare the header row for Google Sheets
    pace_rows = [team_pace_df.columns.tolist()]  # Use the DataFrame's columns as headers
    
    # Append the data rows
    pace_rows.extend(team_pace_df.values.tolist())
    
    # Access the worksheet, creating it if necessary
    sheet_team_pace = get_or_create_worksheet(SPREADSHEET_ID, WORKSHEET_NAME_TEAM_PACE)
    
    # Clear the existing content in the sheet before uploading new data
    clear_sheet(sheet_team_pace)
    
    # Upload the data to the worksheet starting from cell A1
    sheet_team_pace.update(values=pace_rows, range_name='A1')
    
    # Format the header row to be bold
    header_format = CellFormat(textFormat=TextFormat(bold=True))
    format_cell_range(sheet_team_pace, 'A1:B1', header_format)
    
    # Format the numerical columns (PACE) to be right-aligned
    format_cell_range(sheet_team_pace, 'B2:B' + str(len(pace_rows)), CellFormat(horizontalAlignment='RIGHT'))
    
    print("Team pace stats have been successfully uploaded to 'Team Pace Per100Poss' sheet.")

# Main function to run the script
def main():
    upload_team_pace_to_sheet()

# Run the script if it is executed directly
if __name__ == "__main__":
    main()
