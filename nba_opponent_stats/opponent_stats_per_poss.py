import gspread
from google.oauth2.service_account import Credentials
from nba_api.stats.endpoints import leaguedashteamstats
from gspread_formatting import format_cell_range, CellFormat, TextFormat
import pandas as pd

# Path to the Google service account credentials file
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'

# Google Sheets spreadsheet ID and worksheet name
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_OPPONENT_STATS = 'opponent_stats_per_pos'

# Scope for Google Sheets API access
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate and initialize the Google Sheets client
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)

# Access an existing worksheet or create a new one if it doesn't exist
def get_or_create_worksheet(spreadsheet_id, worksheet_name):
    try:
        return client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        sheet = client.open_by_key(spreadsheet_id).add_worksheet(title=worksheet_name, rows=100, cols=26)
        print(f"Created worksheet: '{worksheet_name}'")
        return sheet

# Fetch opponent stats from the NBA API and format the data
def fetch_opponent_stats():
    opponent_stats = leaguedashteamstats.LeagueDashTeamStats(
        per_mode_detailed='Per100Possessions',
        season='2024-25',
        season_type_all_star='Regular Season',
        measure_type_detailed_defense='Opponent'
    )
    stats_df = opponent_stats.get_data_frames()[0]  # Extract the primary DataFrame from API response
    desired_columns = [
        'TEAM_NAME', 'OPP_FGA', 'OPP_FG_PCT', 'OPP_FG3A', 'OPP_FG3_PCT',
        'OPP_FTA', 'OPP_FT_PCT', 'OPP_OREB', 'OPP_DREB', 'OPP_AST',
        'OPP_STL', 'OPP_BLK', 'OPP_PTS'
    ]
    team_stats_df = stats_df[desired_columns].copy()  # Select only the desired columns and create a copy

    # Define columns that need to be divided or multiplied by 100
    numeric_columns_div_100 = [
        'OPP_FGA', 'OPP_FTA', 'OPP_OREB', 'OPP_DREB', 
        'OPP_AST', 'OPP_STL', 'OPP_BLK', 'OPP_PTS', 'OPP_FG3A'
    ]
    numeric_columns_mul_100 = ['OPP_FG_PCT', 'OPP_FG3_PCT', 'OPP_FT_PCT']

    # Normalize columns by dividing or multiplying by 100
    team_stats_df[numeric_columns_div_100] = team_stats_df[numeric_columns_div_100] / 100
    team_stats_df[numeric_columns_mul_100] = team_stats_df[numeric_columns_mul_100] * 100

    return team_stats_df

# Upload the opponent stats to the Google Sheet
def upload_opponent_stats_to_sheet():
    opponent_stats_df = fetch_opponent_stats()  # Fetch and format the data from the NBA API

    # Prepare the header and data rows for Google Sheets
    stats_rows = [opponent_stats_df.columns.tolist()] + opponent_stats_df.values.tolist()

    # Access or create the worksheet
    sheet_opponent_stats = get_or_create_worksheet(SPREADSHEET_ID, WORKSHEET_NAME_OPPONENT_STATS)

    # Clear existing data in the worksheet
    sheet_opponent_stats.clear()

    # Update the sheet with new data starting from cell A1
    sheet_opponent_stats.update(values=stats_rows, range_name='A1')

    # Format the header row to be bold
    format_cell_range(sheet_opponent_stats, 'A1:Z1', CellFormat(textFormat=TextFormat(bold=True)))

    # Format numerical data columns to be right-aligned
    format_cell_range(sheet_opponent_stats, f'B2:Z{len(stats_rows)}', CellFormat(horizontalAlignment='RIGHT'))

    print(f"Team Opponent stats have been successfully uploaded to 'opponent_stats_per_pos' sheet.\n'")

# Entry point for the script
def main():
    pd.options.mode.chained_assignment = None  # Suppress SettingWithCopyWarning globally
    upload_opponent_stats_to_sheet()

# Run the script if executed directly
if __name__ == "__main__":
    main()
