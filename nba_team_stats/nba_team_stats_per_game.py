import gspread
from google.oauth2.service_account import Credentials
from nba_api.stats.endpoints import leaguedashteamstats
from gspread_formatting import format_cell_range, CellFormat, TextFormat

# Google Sheets credentials and configuration
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_TEAM_STATS = 'team_min_per_game'

# Authenticate and initialize the Google Sheets client
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet_team_stats = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME_TEAM_STATS)

# Clears all data from the specified worksheet
def clear_sheet(sheet):
    sheet.clear()

# Fetches team stats for the 2024-25 NBA season from the NBA API
def fetch_team_stats():
    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        per_mode_detailed='PerGame',
        season='2024-25',
        season_type_all_star='Regular Season',
    )
    stats_df = team_stats.get_data_frames()[0]  # Extract the primary DataFrame
    stats_df = stats_df[stats_df['MIN'] > 0.0]  # Filter teams with more than 0 minutes played
    return stats_df[['TEAM_NAME', 'MIN']]  # Return relevant columns only

# Uploads the team stats to the specified Google Sheets worksheet
def upload_team_stats_to_sheet():
    clear_sheet(sheet_team_stats)
    team_stats_df = fetch_team_stats()
    stats_rows = [["Team", "MIN"]]  # Header row for Google Sheets
    for _, row in team_stats_df.iterrows():
        stats_rows.append([row['TEAM_NAME'], row['MIN']])
    if len(stats_rows) == 1:  # If only the header row exists
        print("No team stats found.")
        return
    sheet_team_stats.update(values=stats_rows, range_name='A1')
    format_cell_range(sheet_team_stats, 'A1:B1', CellFormat(textFormat=TextFormat(bold=True)))  # Bold header row
    format_cell_range(sheet_team_stats, f'B2:B{len(stats_rows)}', CellFormat(horizontalAlignment='RIGHT'))  # Right-align numerical data
    print("Team stats have been successfully uploaded to 'team_min_per_game' sheet.")

# Main function to run the script
def main():
    upload_team_stats_to_sheet()

# Entry point for the script
if __name__ == "__main__":
    main()
