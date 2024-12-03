import gspread
from google.oauth2.service_account import Credentials
from nba_api.stats.endpoints import leaguedashteamstats
from gspread_formatting import format_cell_range, CellFormat, TextFormat

# Google Sheets credentials and configuration
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_TEAM_STATS = 'team_stats_per_pos'

# Authenticate and initialize the Google Sheets client
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet_team_stats = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME_TEAM_STATS)

# Clears all data from the specified worksheet
def clear_sheet(sheet):
    sheet.clear()

# Fetch and process team stats for the 2024-25 NBA season
def fetch_team_stats():
    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        per_mode_detailed='Per100Possessions',
        season='2024-25',
        season_type_all_star='Regular Season',
    )
    stats_df = team_stats.get_data_frames()[0]  # Extract the primary DataFrame
    stats_df = stats_df[stats_df['FGA'] > 0.0]  # Filter teams with valid data
    stats_df['FGA'] /= 100  # Adjust FGA scale
    columns = [
        'TEAM_NAME', 'FGA', 'FG_PCT', 'FG3A', 'FG3_PCT', 'FTA',
        'FT_PCT', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'PTS'
    ]
    stats_df = stats_df[columns]
    stats_df.loc[:, 'FG_PCT'] *= 100
    stats_df.loc[:, 'FG3_PCT'] *= 100
    stats_df.loc[:, 'FT_PCT'] *= 100
    for col in ['FTA', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'PTS', 'FG3A']:
        stats_df.loc[:, col] /= 100
    stats_df.update(stats_df.select_dtypes(include='number').round(3))  # Round numeric values to 3 decimals
    return stats_df

# Upload team stats to the specified Google Sheets worksheet
def upload_team_stats_to_sheet():
    team_stats_df = fetch_team_stats()
    rows = [["Team", "FGA", "FG_PCT", "FG3A", "FG3_PCT", "FTA", "FT_PCT", "OREB", "DREB", "AST", "STL", "BLK", "PTS"]]
    rows.extend(team_stats_df.values.tolist())
    if len(rows) == 1:  # No data to upload
        print("No team stats found.")
        return
    clear_sheet(sheet_team_stats)
    sheet_team_stats.update(values=rows, range_name='A1')
    format_cell_range(sheet_team_stats, 'A1:N1', CellFormat(textFormat=TextFormat(bold=True)))  # Bold header row
    format_cell_range(sheet_team_stats, f'B2:N{len(rows)}', CellFormat(horizontalAlignment='RIGHT'))  # Right-align stats
    print("Team stats have been successfully uploaded to 'team_stats_per_pos' sheet.")

# Main function to run the script
def main():
    upload_team_stats_to_sheet()

# Entry point for the script
if __name__ == "__main__":
    main()
