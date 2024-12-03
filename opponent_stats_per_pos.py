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
WORKSHEET_NAME_OPPONENT_STATS = 'Opponent Stats Per1Poss'

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
        sheet = spreadsheet.add_worksheet(title=worksheet_name, rows=100, cols=26)  # Adjust rows/cols as needed
        print(f"Worksheet '{worksheet_name}' created.")
    return sheet

# Function to fetch opponent stats for the 2024-25 NBA season
def fetch_opponent_stats():
    # Fetching opponent stats from the NBA API (Per 100 possessions)
    opponent_stats = leaguedashteamstats.LeagueDashTeamStats(
        per_mode_detailed='Per100Possessions',
        season='2024-25',
        season_type_all_star='Regular Season',
        measure_type_detailed_defense='Opponent'
    )
    
    # Convert the data into a pandas DataFrame
    stats_df = opponent_stats.get_data_frames()[0]
    
    # Columns that match the desired output
    desired_columns = [
        'TEAM_NAME', 'OPP_FGA', 'OPP_FG_PCT', 'OPP_FG3A', 'OPP_FG3_PCT', 
        'OPP_FTA', 'OPP_FT_PCT', 'OPP_OREB', 'OPP_DREB', 'OPP_AST', 
        'OPP_STL', 'OPP_BLK', 'OPP_PTS'
    ]
    
    # Ensure only desired columns are included
    team_stats_df = stats_df[desired_columns]
    
    # Apply adjustments to specific statistics
    team_stats_df.loc[:, 'OPP_FGA'] = team_stats_df['OPP_FGA'] / 100  # Adjust OREB by dividing by 100
    team_stats_df.loc[:, 'OPP_FG_PCT'] = team_stats_df['OPP_FG_PCT'] * 100  # Convert FG% to percentage
    team_stats_df.loc[:, 'OPP_FTA'] = team_stats_df['OPP_FTA'] / 100  # Adjust FTA by dividing by 100
    team_stats_df.loc[:, 'OPP_OREB'] = team_stats_df['OPP_OREB'] / 100  # Adjust OREB by dividing by 100
    team_stats_df.loc[:, 'OPP_PTS'] = team_stats_df['OPP_PTS'] / 100  # Adjust PTS by dividing by 100
    team_stats_df.loc[:, 'OPP_AST'] = team_stats_df['OPP_AST'] / 100  # Adjust AST by dividing by 100
    team_stats_df.loc[:, 'OPP_STL'] = team_stats_df['OPP_STL'] / 100  # Adjust STL by dividing by 100
    team_stats_df.loc[:, 'OPP_BLK'] = team_stats_df['OPP_BLK'] / 100  # Adjust BLK by dividing by 100
    team_stats_df.loc[:, 'OPP_FG3A'] = team_stats_df['OPP_FG3A'] / 100  # Adjust 3PA by dividing by 100
    team_stats_df.loc[:, 'OPP_DREB'] = team_stats_df['OPP_DREB'] / 100  # Adjust DREB by dividing by 100
    team_stats_df.loc[:, 'OPP_FG3_PCT'] = team_stats_df['OPP_FG3_PCT'] * 100  # Convert 3P% to percentage
    team_stats_df.loc[:, 'OPP_FT_PCT'] = team_stats_df['OPP_FT_PCT'] * 100  # Convert FT% to percentage
    
    return team_stats_df

# Function to clear the content of the sheet
def clear_sheet(sheet):
    sheet.clear()

# Function to upload opponent stats to the Google Sheets
def upload_opponent_stats_to_sheet():
    # Fetch opponent stats from the NBA API
    opponent_stats_df = fetch_opponent_stats()
    
    # Prepare the header row for Google Sheets
    stats_rows = [opponent_stats_df.columns.tolist()]  # Use the DataFrame's columns as headers
    
    # Append the data rows
    stats_rows.extend(opponent_stats_df.values.tolist())
    
    # Access the worksheet, creating it if necessary
    sheet_opponent_stats = get_or_create_worksheet(SPREADSHEET_ID, WORKSHEET_NAME_OPPONENT_STATS)
    
    # Clear the existing content in the sheet before uploading new data
    clear_sheet(sheet_opponent_stats)
    
    # Upload the data to the worksheet starting from cell A1
    sheet_opponent_stats.update(values=stats_rows, range_name='A1')
    
    # Format the header row to be bold
    header_format = CellFormat(textFormat=TextFormat(bold=True))
    format_cell_range(sheet_opponent_stats, 'A1:Z1', header_format)
    
    # Format the numerical columns (from B to Z) to be right-aligned
    format_cell_range(sheet_opponent_stats, 'B2:Z' + str(len(stats_rows)), CellFormat(horizontalAlignment='RIGHT'))
    
    print("Opponent stats have been successfully uploaded to 'Opponent Stats Per100Poss' sheet.")

# Main function to run the script
def main():
    upload_opponent_stats_to_sheet()

# Run the script if it is executed directly
if __name__ == "__main__":
    main()
