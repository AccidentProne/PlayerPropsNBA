import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from nba_api.stats.endpoints import leaguedashteamstats
from gspread_formatting import *
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Google Sheets credentials and configuration
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_TEAM_STATS = 'Team Stats PerGame'

# Google Sheets client setup
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet_team_stats = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME_TEAM_STATS)

def clear_sheet(sheet):
    """Clears the content of the provided Google Sheets worksheet."""
    sheet.clear()

def fetch_team_stats():
    """Fetch team stats for the 2024-25 NBA season using the NBA API."""
    # Fetch team statistics from the NBA API
    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        per_mode_detailed='PerGame',
        season='2024-25',
        season_type_all_star='Regular Season',
    )

    # Convert the fetched data into a pandas DataFrame
    stats_df = team_stats.get_data_frames()[0]

    # Filter out teams with zero minutes played (if applicable)
    stats_df_filtered = stats_df[stats_df['MIN'] > 0.0]  # Adjust this condition based on available team stats

    # Select relevant columns: team name and example stats (e.g., points scored per game)
    team_stats_df = stats_df_filtered[['TEAM_NAME', 'MIN']]  # Replace 'MIN' with any other stats you want to track

    return team_stats_df

def upload_team_stats_to_sheet():
    """Uploads cleaned team stats to the 'Team Stats PerGame' worksheet in Google Sheets."""
    # Clear the sheet before importing new data
    clear_sheet(sheet_team_stats)
    
    # Fetch team stats from the NBA API
    team_stats_df = fetch_team_stats()
    
    # Prepare the data for upload
    stats_rows = [["Team", "MIN"]]  # Header row (You can add more columns like FG%, etc.)
    
    # Collect the data for each team
    for _, row in team_stats_df.iterrows():
        stats_rows.append([row['TEAM_NAME'], row['MIN']])
    
    # If no data found, exit
    if not stats_rows:
        print("No team stats found.")
        return
    
    # Upload the stats to the Google Sheets worksheet
    sheet_team_stats.update(values=stats_rows, range_name='A1')
    
    # Format the header row to be bold
    header_format = CellFormat(textFormat=TextFormat(bold=True))
    format_cell_range(sheet_team_stats, 'A1:B1', header_format)
    
    # Right-align the 'Points' column
    format_cell_range(sheet_team_stats, 'B2:B' + str(len(stats_rows) + 1), CellFormat(horizontalAlignment='RIGHT'))
    
    print("Team stats have been successfully uploaded to 'Team Stats PerGame' sheet.")

def main():
    """Main function to fetch and upload team stats."""
    upload_team_stats_to_sheet()

# Entry point for the script
if __name__ == "__main__":
    main()
